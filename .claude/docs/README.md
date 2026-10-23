# docs/

Project-level documents that agents read often.

| File | Purpose |
|---|---|
| `product-brief.md` | Vision, goal, scope, assumptions, risks. Tags: [Accepted] [Proposed] [Hypothesis] [Open] |
| `decision-logs.md` | Decision index + recent / open entries (D-NNN). Only [Accepted] is binding. Managed by the `log-decision` skill |
| `decision-archive.md` | Closed decisions moved out of the log, full text unchanged |
| `owner-feedback.md` | One line per owner correction or preference: date — feedback — how to apply |
| `compact-keep.md` | Text printed by the SessionStart "compact" hook so key rules survive context compaction |
| `agent-pipeline.svg` | Diagram of the `new-feature` agent pipeline (draw one per project; not copied here) |

Skeletons are `_template-*.md`.
