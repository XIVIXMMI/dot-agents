# Keep after compact (printed by the SessionStart "compact" hook)

If anything below is missing from your summary, restore it. Details live in files; keep pointers, not copies.

## Owner rules
- Reply language and tone: see AGENTS.md (Owner). The owner decides; every proposal states trade-offs.
- `developer` leaves work uncommitted; the orchestrator commits after review and the feature run, pushes, and opens PRs; only the owner merges. Commit format `<type>(<scope>): <summary>`. No emoji anywhere.
- End every agent response with the `Handoff` block (.agents/rules/workflow.md).
- Never weaken a failing test; ask the owner.
- Save tokens: quiet command output, narrow test runs, no re-reading loaded files (.agents/rules/communication.md).

## Where things are
- Brief: .agents/docs/product-brief.md. Decisions: .agents/docs/decision-logs.md (only [Accepted] is binding).
- Specs: .agents/specs/. Reports and bugs: .agents/reports/.
- <Current feature / branch / open decisions: update while working.>
