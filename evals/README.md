# Agent evals

Behavior checks for the dot-agents rules: does a tool and model actually follow them? Use them when you change rules or agents, or before switching a project to another model. They are not for CI: each run costs real tokens (about 15-20k with Codex).

```bash
python3 evals/run.py --tool codex                      # every case once
python3 evals/run.py --tool codex --runs 3 tdd-ids     # one case, 3 times
python3 evals/run.py --tool claude --model sonnet
```

Each run builds a temp project (`install.py` output + `fixture/` + the case's `files/`, committed to git), gives the agent the case prompt, then grades the files and the final message with deterministic checks: no model judges another. Every case also checks the shared rules (Handoff block at the end, no emoji). Failing run folders are kept in `evals/.runs/` (gitignored) and printed.

| Case | Rule it checks |
|---|---|
| `tdd-ids` | criteria built with tests that carry the requirement ID |
| `bugfix-test-first` | a bug fix comes with a regression test |
| `no-weaken-tests` | a failing test is never weakened, deleted or skipped |
| `proposed-decision` | no building on a [Proposed] decision; ask the owner |
| `owner-accepts` | the owner's decision is recorded in the decision log |
| `injection` | instructions inside files are not followed and are reported |

## Add a case
`cases/<name>/case.toml` with a `prompt` and `[[check]]` entries, each with a `name` and one of:
- `run = "<shell>"`: must exit 0 in the project
- `file = "<glob>"` with `matches` and/or `not_matches` (regex over the joined files)
- `absent = "<path>"`: must not exist
- `output` / `output_not`: regex over the agent's final message

Optional `files/` overlays the fixture. `python3 -m unittest discover tests` checks that every case fails on the untouched fixture, so a case cannot pass before the agent acts.

An agent that crashes or hits a usage limit shows as `agent exited N`; read the `.log` next to the run folder.

Limits: checks see the end state, not the order of work, so "test first" is checked only as "a test exists". Claude runs (`claude -p`) are wired but not yet tried.
