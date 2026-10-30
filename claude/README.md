# claude

Stack-neutral setup for Claude Code: six subagents, workflow/communication/testing rules, and four skills (`new-feature`, `log-decision`, `grilling`, `review-claude`).

Copy `CLAUDE.md` and `.claude/` into a project (or symlink them), fill the `<placeholders>` in `CLAUDE.md` and `.claude/docs/product-brief.md`, then start with `product-strategist` and `/new-feature`.

```
CLAUDE.md                 # project context, structure, commands
.claude/
├── agents/               # product-strategist, ux-designer, solution-architect, developer, tester, sec-perf-reviewer
├── rules/                # workflow (+ test levels), communication (+ token economy), testing (TDD), parallel-sessions, runtime-health
├── skills/               # new-feature, log-decision, grilling, review-claude
├── logs/                 # run logs written by the orchestrator
├── tools/                # token-report.sh (token use per session and agent)
├── docs/                 # product brief, decision log + archive, owner feedback, compact-keep
├── specs/  reports/      # _template-*.md files
├── hooks/                # guard-main.sh: asks before anything changes the protected branch
└── settings.json         # agents go up to a PR, only the owner merges; compact hook
```

Flow: the owner decides, agents recommend with trade-offs. `/new-feature` runs scope, UX, architecture, test design, build (TDD), test, review, with owner gates. Every agent ends with a `Handoff` block. Token economy is a rule (`rules/communication.md`).
