# Parallel Sessions Rules

Applies when the orchestrator starts child sessions (separate Claude sessions on separate branches). Subagents inside one session do not count as child sessions. Set the limit N in `CLAUDE.md` (default 2).

## Roles
- The orchestrator plans, assigns, merges, and talks to the owner. Child sessions build one feature each on their own branch.
- At most N child sessions at once. Each owns its branch and, if the project needs one, its own test environment (database, port, device) so runs never collide.

## Decisions in a child session
- A child settles open questions itself when the answer stays inside the feature's [Accepted] scope (its decisions and approved specs). Reversible implementation details the spec leaves open (names, helper structure, internal layout, test fixtures) are not decisions: choose, write it down, go on.
- A child asks the orchestrator, and keeps working on other parts meanwhile, for anything outside that scope: a change of scope, product behavior, security or privacy, the data model, a new dependency, these rules, or anything an [Accepted] decision covers. It lists every open question under "Open questions" in its report and never ends a turn waiting on the owner.
- A child records each delegated decision in its dev report ("Decisions taken (delegated)": what, options, choice, why) and its bugs in its test report. It does not edit shared logs (`bugs.md`, `decision-logs.md`, `.claude/logs/`), so merges do not conflict there.

## Preflight
Before a child starts, it lists the files it expects to edit and the files it will own. The orchestrator checks the lists for overlap and either serializes the overlapping part or gives one session ownership; the other adds only small, separate pieces to a shared file. A child updates its list before it edits a shared file. Keep a list of "hot files" in `CLAUDE.md` once clashes show up.

## Handoff packet
A child's dev report ends with about 8 lines: base commit, files changed, test command and result file path with the commit or code hash it ran on, delegated decisions, bugs, open questions, what is left. The orchestrator works from it and does not re-read the whole report.

## Merge queue
- The orchestrator owns merging, one branch at a time, and settles or assigns any clash itself. Two children never fix the same shared file.
- Merge early: as soon as a child's unit tests and related suites are green, merge it into the integration branch and run only the unit tests there to catch a broken merge.
- Before its final test run, each other child merges the latest integration branch into its own, so clashes show up on that run and not at the end.
- Before a merge into `main`, run the critical set (see Test levels in `workflow.md`).

## Run log
The orchestrator copies every delegated decision and bug into `.claude/logs/run-log-<date>.md` (layout in `.claude/logs/README.md`), bugs into `.claude/reports/bugs.md`, lasting decisions into `decision-logs.md`, and lists them for the owner in its next report. A new session that continues earlier work reads the newest run log first.

## End of a batch
When the last child reports done, check the owner's deadline. If the full suite cannot finish before it, skip it, log that in the run log, report, and stop. Otherwise run it as usual.
