#!/usr/bin/env python3
"""Install or update dot-agents in a project.

    python3 install.py <project dir> [--stack python|java-spring|rust-tauri|swift-ios[,<stack>...]] [--tools claude,codex] [--no-rules-block]

Safe to rerun. Files the project owns (AGENTS.md, CLAUDE.md, rules, docs, specs, reports, logs,
settings, .agents/agents-local) are copied only when missing or never touched. Folders dot-agents owns
(.agents/skills, agents, tools, ci) and generated ones (.claude/agents, .codex/agents) are wiped and
rebuilt, so removed or renamed agents and skills do not linger; do not keep your own files there. The
project's own agents go in .agents/agents-local/. The rules block in AGENTS.md is replaced, or removed with
--no-rules-block for a project that keeps a short AGENTS.md with its own digest of the rules.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE = ROOT / "core"
PROJECT_OWNED = ["rules", "docs", "specs", "reports", "logs"]
TOOL_OWNED = ["skills", "agents", "tools", "ci"]
LOCAL_AGENTS = "agents-local"  # project-owned agents: never wiped, rendered next to the core ones
# Agent tier -> what each tool calls it. Codex keeps the session's model and changes reasoning effort.
TIERS = {
    "claude": {"strong": "opus", "fast": "sonnet"},
    "codex": {"strong": "high", "fast": "medium"},
}
BLOCK = re.compile(r"<!-- dot-agents:rules:start.*?<!-- dot-agents:rules:end -->\n?", re.S)
CODEX_DOC_LIMIT = 32 * 1024  # Codex project_doc_max_bytes default
SKILLS_COPY_MARKER = ".dot-agents-copy"


def copy_missing(src, dst):
    for f in src.rglob("*"):
        target = dst / f.relative_to(src)
        if f.is_file() and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)


def parse_agent(path):
    """Split an agent file into (frontmatter dict, frontmatter lines, body)."""
    text = path.read_text(encoding="utf-8")
    try:
        _, head, body = text.split("---\n", 2)
        meta = dict(line.split(": ", 1) for line in head.strip().splitlines() if line.strip())
    except ValueError:
        raise SystemExit(f"{path}: frontmatter must sit between '---' lines, one 'key: value' per line")
    for key in ("name", "description", "tier"):
        if key not in meta:
            raise SystemExit(f"{path}: frontmatter needs '{key}'")
    if meta["tier"] not in TIERS["claude"]:
        raise SystemExit(f"{path}: tier must be one of {list(TIERS['claude'])}")
    return meta, head, body


def render_claude(meta, head, body):
    head = re.sub(r"^tier: .*$", f"model: {TIERS['claude'][meta['tier']]}", head, count=1, flags=re.M)
    return f"---\n{head}---\n{body}"


def render_codex(meta, head, body):
    if "'''" in body:
        raise SystemExit(f"agent {meta['name']}: body must not contain ''' (TOML literal string)")
    # json.dumps output is a valid TOML basic string.
    return (
        f"name = {json.dumps(meta['name'])}\n"
        f"description = {json.dumps(meta['description'], ensure_ascii=False)}\n"
        f"model_reasoning_effort = {json.dumps(TIERS['codex'][meta['tier']])}\n"
        f"developer_instructions = '''\n{body.strip()}\n'''\n"
    )


def demote_headings(text):
    """Add one '#' to every Markdown heading outside fenced code blocks."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"#+ ", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def sync_rules_block(agents_md, rules_dir):
    parts = []
    for f in sorted(rules_dir.glob("*.md")):
        # Demote headings one level so each rule file sits under the project's own sections.
        parts.append(demote_headings(f.read_text(encoding="utf-8").strip()))
    block = (
        "<!-- dot-agents:rules:start - generated from .agents/rules/ by install.py; edit those files and rerun -->\n"
        + "\n\n".join(parts)
        + "\n<!-- dot-agents:rules:end -->\n"
    )
    text = agents_md.read_text(encoding="utf-8")
    if BLOCK.search(text):
        text = BLOCK.sub(lambda _: block, text)
    else:
        text = text.rstrip("\n") + "\n\n" + block
    agents_md.write_text(text, encoding="utf-8")
    size = len(text.encode("utf-8"))
    if size > CODEX_DOC_LIMIT:
        print(f"warning: AGENTS.md is {size} bytes; Codex reads only the first {CODEX_DOC_LIMIT}", file=sys.stderr)


def remove_rules_block(agents_md):
    text = agents_md.read_text(encoding="utf-8")
    if BLOCK.search(text):
        agents_md.write_text(BLOCK.sub("", text).rstrip("\n") + "\n", encoding="utf-8")


def install(target, stack=None, tools=(), rules_block=True):
    target = Path(target).resolve()
    dot = target / ".agents"
    for d in PROJECT_OWNED:
        copy_missing(CORE / d, dot / d)
    for d in TOOL_OWNED:
        shutil.rmtree(dot / d, ignore_errors=True)
        shutil.copytree(CORE / d, dot / d, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))

    agents_md = target / "AGENTS.md"
    if not agents_md.exists():
        text = (CORE / "AGENTS.md").read_text(encoding="utf-8")
        # A project with several stacks (e.g. a Python tool next to an iOS app) gets one section per stack.
        for name in [s for s in (stack or "").split(",") if s]:
            stack_file = ROOT / "stacks" / name / "stack.md"
            if not stack_file.exists():
                raise SystemExit(f"unknown stack '{name}'; see {ROOT / 'stacks'}")
            text = text.rstrip("\n") + "\n\n" + stack_file.read_text(encoding="utf-8")
        agents_md.write_text(text, encoding="utf-8")
    elif stack:
        print("AGENTS.md exists; stack section not added (edit it by hand)", file=sys.stderr)
    if rules_block:
        sync_rules_block(agents_md, dot / "rules")
    else:
        remove_rules_block(agents_md)

    # A local agent with the name of a core agent replaces it, so a project can adapt one role.
    by_name = {}
    for p in sorted((dot / "agents").glob("*.md")) + sorted((dot / LOCAL_AGENTS).glob("*.md")):
        parsed = parse_agent(p)
        by_name[parsed[0]["name"]] = parsed
    agents = [by_name[n] for n in sorted(by_name)]
    if "claude" in tools:
        adapter = ROOT / "adapters" / "claude"
        (target / ".claude").mkdir(exist_ok=True)
        claude_md = target / "CLAUDE.md"
        if not claude_md.exists():
            shutil.copy2(adapter / "CLAUDE.md", claude_md)
        elif "@AGENTS.md" not in claude_md.read_text(encoding="utf-8").splitlines():
            # Claude reads the rules only through this import; keep the owner's text below it.
            claude_md.write_text("@AGENTS.md\n\n" + claude_md.read_text(encoding="utf-8"), encoding="utf-8")
        copy_missing(adapter / "tools", target / ".claude" / "tools")
        copy_missing(adapter / "hooks", target / ".claude" / "hooks")
        if not (target / ".claude" / "settings.json").exists():
            shutil.copy2(adapter / "settings.json", target / ".claude" / "settings.json")
        link = target / ".claude" / "skills"
        if not link.is_symlink() and (link / SKILLS_COPY_MARKER).exists():
            shutil.rmtree(link)  # our own fallback copy from an earlier run: refresh it
        if not link.exists() and not link.is_symlink():
            try:
                link.symlink_to(Path("..") / ".agents" / "skills", target_is_directory=True)
            except OSError:
                # Windows without Developer Mode or admin cannot create symlinks.
                shutil.copytree(dot / "skills", link)
                (link / SKILLS_COPY_MARKER).write_text(
                    "Copied from .agents/skills by install.py (no symlink rights). Edit .agents/skills and rerun.\n",
                    encoding="utf-8")
                print("could not symlink .claude/skills; copied .agents/skills instead (rerun after skill changes)",
                      file=sys.stderr)
        elif not link.is_symlink():
            print(".claude/skills is a real folder; move its skills to .agents/skills and delete it", file=sys.stderr)
        out = target / ".claude" / "agents"
        shutil.rmtree(out, ignore_errors=True)
        out.mkdir(parents=True)
        for meta, head, body in agents:
            (out / f"{meta['name']}.md").write_text(render_claude(meta, head, body), encoding="utf-8")
    if "codex" in tools:
        out = target / ".codex" / "agents"
        shutil.rmtree(out, ignore_errors=True)
        out.mkdir(parents=True)
        for meta, head, body in agents:
            (out / f"{meta['name']}.toml").write_text(render_codex(meta, head, body), encoding="utf-8")

    gitignore = target / ".gitignore"
    lines = gitignore.read_text(encoding="utf-8").splitlines() if gitignore.exists() else []
    if ".agents/logs/junit/" not in lines:
        gitignore.write_text("\n".join(lines + [".agents/logs/junit/"]) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("target")
    ap.add_argument("--stack", help="one stack, or a comma list for a project with several: python,swift-ios")
    ap.add_argument("--tools", default="", help="comma list: claude,codex")
    ap.add_argument("--no-rules-block", action="store_true",
                    help="do not inline .agents/rules into AGENTS.md; remove the block if present")
    args = ap.parse_args(argv)
    tools = [t for t in args.tools.split(",") if t]
    unknown = set(tools) - set(TIERS)
    if unknown:
        raise SystemExit(f"unknown tools {sorted(unknown)}; supported: {sorted(TIERS)}")
    install(args.target, args.stack, tools, rules_block=not args.no_rules_block)
    print(f"installed into {Path(args.target).resolve()} (tools: {', '.join(tools) or 'none'})")


if __name__ == "__main__":
    main()
