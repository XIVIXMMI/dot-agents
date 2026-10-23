# agents

A language- and framework-neutral template for working with Claude Code: a team of subagents, the rules for how they talk to the owner and to each other, and a feature pipeline with owner gates. Copy it into a project (or use this repo as a GitHub template) and fill in the placeholders.

```
CLAUDE.md                  # project context, structure, commands (fill in; loaded every session)
.claude/
├── agents/                # product-strategist, ux-designer, solution-architect, developer, tester, sec-perf-reviewer
├── rules/                 # workflow (decisions, Handoff, orchestration, git), communication (+ token economy), testing (TDD)
├── skills/                # new-feature (pipeline), log-decision, grilling, review-claude
├── docs/                  # product brief, decision log + archive, owner feedback, compact-keep
├── specs/                 # per-feature specs; _template-*.md files
├── reports/               # dev / test reports, audits, bugs; _template-*.md files
└── settings.json          # git-safe permissions and the compact hook
```

## How it works

1. The owner decides; agents recommend with trade-offs. Only [Accepted] decisions in `docs/decision-logs.md` are binding.
2. The main session orchestrates. `/new-feature <idea>` runs: scope -> UX -> architecture -> test design -> build (TDD) -> test -> review, stopping at owner gates.
3. Every agent ends with a `Handoff` block; the orchestrator checks it against tool output.
4. Token economy is a rule, not a hope: quiet output, narrow test runs, paths instead of pasted contents, short reports (`rules/communication.md`).

## Use

1. Copy `CLAUDE.md` and `.claude/` into your project (do not copy `.claude/settings.local.json`).
2. Fill the `<placeholders>` in `CLAUDE.md` (stack, structure, commands) and `docs/product-brief.md`.
3. Add stack-specific rules or skills in `.claude/rules/` or `.claude/skills/`; add stack-specific risks to `CLAUDE.md`.
4. Start with `product-strategist` for scope, `solution-architect` for `specs/architecture.md`, then `/new-feature`.

`grilling` is adapted from a third-party skill; see `THIRD-PARTY-NOTICES.md`.
