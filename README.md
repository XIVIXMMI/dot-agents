# dot-agents

My setup for AI coding agents: one owner-gated, test-first (TDD) workflow that works across tools (Claude Code, Codex, more later) and stacks (Python, Java/Spring, Rust/Tauri, Swift/iOS).

The source of truth uses open formats every tool reads: `AGENTS.md` and Agent Skills (`.agents/skills/<name>/SKILL.md`). Tool-specific files are thin and generated.

```
core/                 # tool- and stack-neutral: the workflow itself
├── AGENTS.md         # project instructions template
├── rules/            # workflow, communication, testing (TDD + RTM), parallel-sessions, runtime-health
├── agents/           # 6 roles; `tier: strong|fast` instead of a model name
├── skills/           # new-feature, log-decision, grilling, review-agents
├── docs/ specs/ reports/ logs/   # templates the project then owns
├── tools/rtm.py      # requirement traceability matrix (RTM) builder
└── ci/rtm.yml        # GitHub Action: tests -> RTM -> Google Sheet
stacks/<stack>/stack.md   # commands, JUnit XML output, test naming per stack
adapters/<tool>/          # only what one tool needs (Claude: CLAUDE.md, settings.json, guard-main hook; Codex: notes)
install.py                # puts it all into a project; safe to rerun
evals/                    # behavior evals: does a tool/model follow the rules? (see evals/README.md)
tests/                    # python3 -m unittest discover tests
```

## Install into a project

```bash
python3 install.py ~/code/my-app --stack python --tools claude,codex
```

The project gets:

| Path | What | On rerun |
|---|---|---|
| `AGENTS.md` | template + stack section + generated rules block | your text kept, rules block refreshed |
| `.agents/rules, docs, specs, reports, logs` | project-owned | copied only if missing |
| `.agents/skills, agents, tools, ci` | owned by dot-agents | wiped and rebuilt (old agents and skills removed) |
| `CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/` | `@AGENTS.md` + Claude notes, permissions, guard-main hook | copied only if missing; an existing `CLAUDE.md` gets the `@AGENTS.md` line at the top |
| `.claude/skills` | symlink to `.agents/skills` (a marked copy where symlinks are not allowed, e.g. Windows without Developer Mode) | kept; a copy is refreshed |
| `.claude/agents/*.md`, `.codex/agents/*.toml` | rendered from `.agents/agents/` | wiped and rebuilt |

Then fill the `<placeholders>` in `AGENTS.md` and `.agents/docs/product-brief.md`, and start a feature with the `new-feature` skill (`/new-feature` in Claude, `$new-feature` in Codex).

Rules stay as files in `.agents/rules/` so you can edit them per project; rerun `install.py` to copy them into the block in `AGENTS.md`. Every tool then reads the same rules from one file.

## Home setup (optional)

After cloning, link the repo to a fixed path and the skills into the folders agents scan in `$HOME`, so the skills work in every project and a `git pull` updates them:

```bash
[ -e ~/.dot-agents ] || ln -s "$PWD" ~/.dot-agents        # run inside the clone
mkdir -p ~/.agents/skills ~/.claude/skills
# Link only where nothing exists yet; never replace a skill, link or folder already there.
for s in ~/.dot-agents/core/skills/*/; do n=$(basename "$s")
  for d in ~/.agents/skills ~/.claude/skills; do
    if [ -e "$d/$n" ] || [ -L "$d/$n" ]; then echo "kept existing $d/$n"; else ln -s "${s%/}" "$d/$n"; fi
  done
done
```

- `~/.agents/skills` is read by Codex and Kimi, `~/.claude/skills` by Claude. Do not make `~/.agents` itself the link: the skills live in `core/skills`, and the folder may hold other tools' files.
- Then install with `python3 ~/.dot-agents/install.py <project> ...`.
- The links follow the branch checked out in the clone; keep it on `main`.
- `new-feature` and `log-decision` still need a project installed with `install.py` (they read its `.agents/` files). A project installed that way also has its own copy, so the same skill shows twice.
- Undo: `rm ~/.dot-agents ~/.agents/skills/{grilling,log-decision,new-feature,review-agents} ~/.claude/skills/{grilling,log-decision,new-feature,review-agents}`

## Traceability (RTM)

Agents never write the matrix. Specs give each acceptance criterion an ID (`AUTH-3: ...`), tests carry it in their name (`test_AUTH_3_rejects_empty_title`), and `rtm.py` joins specs with JUnit XML:

```bash
python3 .agents/tools/rtm.py --junit '.agents/logs/junit/*.xml'
```

- `.agents/reports/rtm.csv`: one row per requirement (status PASS / FAIL / SKIP / NO_TEST, counts, test names). For people.
- `.agents/reports/rtm-gaps.md`: only failing, untested and duplicate items. The only part agents read.
- `--sheet <id>` replaces the `RTM` tab of a Google Sheet. For a private repo, use `.agents/ci/rtm.yml` (setup steps at its top).

## Add a tool or a stack
- Tool: add `adapters/<tool>/`, a tier mapping in `TIERS` and a render step in `install.py`. Tools that read `AGENTS.md` and `.agents/skills` natively (Kimi Code, OpenCode, Gemini CLI) need only agents rendered.
- Stack: add `stacks/<name>/stack.md` with commands, the JUnit XML command and glob, and the test naming rule.

Third-party material is credited in `THIRD-PARTY-NOTICES.md`.
