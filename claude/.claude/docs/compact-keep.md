# Keep after compact (printed by the SessionStart "compact" hook)

If anything below is missing from your summary, restore it. Details live in files; keep pointers, not copies.

## Owner rules
- Reply language and tone: see CLAUDE.md (Owner). The owner decides; every proposal states trade-offs.
- Agents commit, push their branch, and open PRs; only the owner merges into main. Commit format `<type>(<scope>): <summary>`. No emoji anywhere.
- End every agent response with the `Handoff` block (.claude/rules/workflow.md).
- Never weaken a failing test; ask the owner.
- Save tokens: quiet command output, narrow test runs, no re-reading loaded files (.claude/rules/communication.md).

## Where things are
- Brief: .claude/docs/product-brief.md. Decisions: .claude/docs/decision-logs.md (only [Accepted] is binding).
- Specs: .claude/specs/. Reports and bugs: .claude/reports/.
- <Current feature / branch / open decisions: update while working.>
