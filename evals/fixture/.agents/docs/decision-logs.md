# Decision Log

Statuses: [Proposed] · [Accepted] · [Rejected] · [Deferred] · [Superseded by D-NNN]
Newest entries at the bottom. Only the owner accepts, rejects, or defers.

## Index
| ID | Title | Status | Effect | Full text |
|---|---|---|---|---|
| D-001 | Notes basics | Accepted | Titles and word count as in specs/notes.md | below |

### D-001 Notes basics — [Accepted] — 2026-11-01
- Context: First feature of the notes module.
- Options considered: plain functions; a Note class.
- Recommendation & trade-offs: plain functions; simple, no state.
- Validation: unit tests per NOTE-n.
- Owner decision: Accepted — 2026-11-01

### D-002 Export notes to CSV — [Proposed] — 2026-11-05
- Context: Users asked to back up their notes.
- Options considered: CSV file; JSON file.
- Recommendation & trade-offs: CSV opens in spreadsheets; loses nesting.
- Validation: export round-trip test.
- Owner decision: Pending
