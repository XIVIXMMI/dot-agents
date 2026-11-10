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
| `.agents/skills, agents, tools, ci` | owned by dot-agents | replaced |
| `CLAUDE.md`, `.claude/settings.json`, `.claude/hooks/` | `@AGENTS.md` + Claude notes, permissions, guard-main hook | copied only if missing; an existing `CLAUDE.md` gets the `@AGENTS.md` line at the top |
| `.claude/skills` | symlink to `.agents/skills` | kept |
| `.claude/agents/*.md`, `.codex/agents/*.toml` | rendered from `.agents/agents/` | replaced |

Then fill the `<placeholders>` in `AGENTS.md` and `.agents/docs/product-brief.md`, and start a feature with the `new-feature` skill (`/new-feature` in Claude, `$new-feature` in Codex).

Rules stay as files in `.agents/rules/` so you can edit them per project; rerun `install.py` to copy them into the block in `AGENTS.md`. Every tool then reads the same rules from one file.

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
