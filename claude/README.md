# claude

Stack-neutral setup for Claude Code: six subagents, workflow/communication/testing rules, and four skills (`new-feature`, `log-decision`, `grilling`, `review-claude`).

Copy `CLAUDE.md` and `.claude/` into a project (or symlink them), fill the `<placeholders>` in `CLAUDE.md` and `.claude/docs/product-brief.md`, then start with `product-strategist` and `/new-feature`.

```
CLAUDE.md                 # project context, structure, commands
.claude/
├── agents/               # product-strategist, ux-designer, solution-architect, developer, tester, sec-perf-reviewer
├── rules/                # workflow, communication (+ token economy), testing (TDD)
├── skills/               # new-feature, log-decision, grilling, review-claude
├── docs/                 # product brief, decision log + archive, owner feedback, compact-keep
├── specs/  reports/      # _template-*.md files
└── settings.json         # git-safe permissions and the compact hook
```

Flow: the owner decides, agents recommend with trade-offs. `/new-feature` runs scope, UX, architecture, test design, build (TDD), test, review, with owner gates. Every agent ends with a `Handoff` block. Token economy is a rule (`rules/communication.md`).
