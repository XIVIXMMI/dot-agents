#!/usr/bin/env python3
"""Behavior evals: does an agent tool follow the dot-agents rules?

    python3 evals/run.py --tool codex [--model M] [--runs 3] [--jobs 2] [case ...]

Each run: a temp project = install.py output + evals/fixture + the case's files/, committed to git.
The agent gets the case prompt, then deterministic checks grade the files and its final message.
Every case also checks the shared rules: a Handoff block at the end, no emoji.
Failing run folders are kept and printed for inspection. Each run costs real tokens (~15-20k).
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EVALS = Path(__file__).resolve().parent
RUNS = EVALS / ".runs"  # gitignored; failing runs stay here
sys.path.insert(0, str(EVALS.parent))
import install  # noqa: E402

HANDOFF = re.compile(
    r"\*\*Handoff\*\*\s*\n- status: (done|blocked)\n- files: [^\n]+\n- decisions_needed: [^\n]+\n"
    r"- assumptions: [^\n]+\n- blockers: [^\n]+\n- tests: [^\n]+"
)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
SHARED_CHECKS = [
    {"name": "Handoff block", "output": HANDOFF.pattern},
    {"name": "no emoji", "output_not": EMOJI.pattern},
]
CHECK_KINDS = {"run", "output", "output_not", "file", "absent"}


def find_bin(name):
    path = shutil.which(name) or os.path.expanduser(f"~/.local/bin/{name}")
    if not os.path.exists(path):
        raise SystemExit(f"{name} not found")
    return path


def agent_command(tool, model, workdir, prompt, out_file):
    if tool == "codex":
        cmd = [find_bin("codex"), "exec", "--ephemeral", "-s", "workspace-write", "-C", str(workdir),
               "-o", str(out_file)]
    else:  # claude: edits allowed in the project; shell limited to tests, git reads and listing
        cmd = [find_bin("claude"), "-p", "--permission-mode", "acceptEdits", "--allowedTools",
               "Bash(python3:*)", "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)", "Bash(ls:*)"]
    if model:
        cmd += ["--model" if tool == "claude" else "-m", model]
    return cmd + [prompt]


def agent_env():
    """Drop variables a parent Claude session sets, so the agent CLI uses its own login."""
    return {k: v for k, v in os.environ.items()
            if not (k.startswith(("CLAUDE", "ANTHROPIC")) and k != "CLAUDE_CONFIG_DIR")}


def make_project(case_dir, tool):
    RUNS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f"{case_dir.name}-", dir=RUNS))
    install.install(work, None, [tool])
    shutil.copytree(EVALS / "fixture", work, dirs_exist_ok=True, ignore=shutil.ignore_patterns("AGENTS.extra.md"))
    with open(work / "AGENTS.md", "a", encoding="utf-8") as f:
        f.write((EVALS / "fixture" / "AGENTS.extra.md").read_text(encoding="utf-8"))
    if (case_dir / "files").exists():
        shutil.copytree(case_dir / "files", work, dirs_exist_ok=True)
    git = ["git", "-C", str(work), "-c", "user.name=eval", "-c", "user.email=eval@localhost"]
    subprocess.run(git + ["init", "-q"], check=True)
    subprocess.run(git + ["add", "-A"], check=True)
    subprocess.run(git + ["commit", "-qm", "fixture"], check=True)
    return work


def grade(workdir, output, checks):
    """Return the names of failed checks."""
    failed = []
    for c in checks:
        if "run" in c:
            ok = subprocess.run(c["run"], shell=True, cwd=workdir, capture_output=True, timeout=120).returncode == 0
        elif "output" in c:
            ok = re.search(c["output"], output) is not None
        elif "output_not" in c:
            ok = re.search(c["output_not"], output) is None
        elif "absent" in c:
            ok = not (Path(workdir) / c["absent"]).exists()
        else:
            files = sorted(glob.glob(str(Path(workdir) / c["file"])))
            text = "\n".join(Path(f).read_text(encoding="utf-8") for f in files)
            ok = bool(files)
            if ok and "matches" in c:
                ok = re.search(c["matches"], text) is not None
            if ok and "not_matches" in c:
                ok = re.search(c["not_matches"], text) is None
        if not ok:
            failed.append(c["name"])
    return failed


def load_case(case_dir):
    case = tomllib.loads((case_dir / "case.toml").read_text(encoding="utf-8"))
    for c in case["check"]:
        if len(CHECK_KINDS & c.keys()) != 1 or "name" not in c:
            raise SystemExit(f"{case_dir.name}: each check needs a name and one of {sorted(CHECK_KINDS)}: {c}")
    return case


def run_once(case_dir, tool, model, timeout):
    case = load_case(case_dir)
    work = make_project(case_dir, tool)
    out_file = work.parent / f"{work.name}.out.txt"
    cmd = agent_command(tool, model, work, case["prompt"], out_file)
    log_file = work.parent / f"{work.name}.log"
    try:
        r = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=timeout,
                           stdin=subprocess.DEVNULL, env=agent_env())
        output = out_file.read_text(encoding="utf-8") if out_file.exists() else r.stdout
        log_file.write_text(f"exit {r.returncode}\n--- stdout\n{r.stdout}\n--- stderr\n{r.stderr}", encoding="utf-8")
    except subprocess.TimeoutExpired:
        output = ""
        failed = ["timeout"]
    else:
        failed = grade(work, output, SHARED_CHECKS + case["check"])
        if r.returncode != 0:
            failed.insert(0, f"agent exited {r.returncode}")
    if failed:
        out_file.write_text(output, encoding="utf-8")
    else:
        shutil.rmtree(work)
        out_file.unlink(missing_ok=True)
        log_file.unlink(missing_ok=True)
    return case_dir.name, failed, work


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cases", nargs="*", help="case names (default: all)")
    ap.add_argument("--tool", choices=["codex", "claude"], required=True)
    ap.add_argument("--model")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=600, help="seconds per run")
    args = ap.parse_args(argv)

    names = args.cases or sorted(p.name for p in (EVALS / "cases").iterdir() if (p / "case.toml").exists())
    jobs = [EVALS / "cases" / n for n in names for _ in range(args.runs)]
    with ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda c: run_once(c, args.tool, args.model, args.timeout), jobs))

    print(f"\n{args.tool} {args.model or '(default model)'} - {args.runs} run(s) per case\n")
    print("| case | passed | failed checks |\n|---|---|---|")
    total = 0
    for n in names:
        mine = [r for r in results if r[0] == n]
        ok = sum(1 for _, f, _ in mine if not f)
        total += ok
        fails = sorted({x for _, f, _ in mine for x in f})
        print(f"| {n} | {ok}/{len(mine)} | {', '.join(fails) or '-'} |")
    print(f"\nTotal: {total}/{len(results)} runs passed.")
    for n, f, work in results:
        if f:
            print(f"kept {n}: {work} (final message: {work}.out.txt)")
    return 0 if total == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
