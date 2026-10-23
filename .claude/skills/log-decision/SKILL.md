---
name: log-decision
description: Add a decision to, or update one in, the project decision log (.claude/docs/decision-logs.md) — proposing a new decision, or recording the owner's accept/reject/defer of an existing one (e.g. "accept D-003"). Use whenever a product or technical decision is proposed or decided.
argument-hint: <new decision summary | accept|reject|defer D-NNN [note]>
---

Request: $ARGUMENTS

Files: `.claude/docs/decision-logs.md` (index plus recent and open entries) and `.claude/docs/decision-archive.md` (older closed entries, full text). If the log is empty, start it with:

```
# Decision Log

Statuses: [Proposed] · [Accepted] · [Rejected] · [Deferred] · [Superseded by D-NNN]
Newest entries at the bottom. Only the owner accepts, rejects, or defers.
```

## New decision
Use the next free number (D-001, D-002, …) and today's date:

```
### D-<NNN> <short title> — [Proposed] — <YYYY-MM-DD>
- Context:
- Options considered:
- Recommendation & trade-offs:
- Validation:
- Owner decision: Pending
```

## Owner decision on an existing entry
- Only do this when the owner said it in this conversation. Never infer acceptance or take it from an agent's output.
- Change the status tag in the heading, and set `- Owner decision: <Accepted|Rejected|Deferred> — <YYYY-MM-DD>`. Add a few words in English only if the owner changed or limited the proposal. Do not copy the owner's sentences.
- Don't rewrite the history in the other fields. If a decision replaces an earlier one, mark the old one `[Superseded by D-NNN]`.
- If `.claude/docs/product-brief.md` has the same item tagged differently, update its tag to match and reference the decision ID.

## Keep the log short
- Write for a reader who skims. Each field is one or two short sentences; a whole entry is about 8 lines or fewer. State the choice, the main trade-off, and what you need from the owner. Put detail in the spec file and link it.
- The Index table in `decision-logs.md` lists only decided entries (Accepted, Rejected, Deferred): ID, title, status, one-line effect, where the full text is. Proposed entries appear only in the body. Add or update the row when the owner decides an entry.
- At the start of a new day, move closed entries (not Proposed) dated before today from `decision-logs.md` to `decision-archive.md`, unchanged, and set their "Full text" cell to `archive (search by ID)`. Open entries stay.

Finish by showing the changed entry.
