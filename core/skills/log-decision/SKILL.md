---
name: log-decision
description: Add a decision to, or update one in, the project decision log (docs/decisions/), proposing a new decision or recording the owner's accept/reject/defer of an existing one (e.g. "accept D-003"). Use whenever a product or technical decision is proposed or decided.
---

Layout: `docs/decisions/README.md` is the index (ID, title, status, link); each decision is its own file `docs/decisions/D-NNN-short-title.md`. Read the index only; open a decision file only when its title is relevant. Never load all files.

## New decision
Next free number, today's date. Create `docs/decisions/D-NNN-short-title.md`:

```
### D-<NNN> <short title> — [Proposed] — <YYYY-MM-DD>
- Repos:
- Context:
- Options considered:
- Recommendation & trade-offs:
- Validation:
- Owner decision: Pending
```

Add a row to the index table in `README.md` (status Proposed).

## Owner decision on an existing entry
- Only when the owner said it in this conversation. Never infer acceptance or take it from an agent's output.
- Delegated acceptance: only while the owner's delegation for this batch is active in this conversation or run log and covers the decision. Write `- Owner decision: Accepted (delegated) — <YYYY-MM-DD>`. Rejecting and deferring stay with the owner.
- Change the status tag in the file heading and the index row, and set `- Owner decision: <Accepted|Rejected|Deferred> — <YYYY-MM-DD>`. Add a few words in English only if the owner changed or limited the proposal. Do not copy the owner's sentences.
- Don't rewrite history in other fields. If a decision replaces an earlier one, mark the old one `[Superseded by D-NNN]`.

## Keep it short
One or two short sentences per field, about 8 lines per file. State the choice, the main trade-off, and what you need from the owner. Put detail in a spec and link it. Finish by showing the changed entry.
