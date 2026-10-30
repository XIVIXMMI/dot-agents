---
name: new-feature
description: Take a feature from idea to tested code through the agent pipeline (strategy -> UX -> architecture -> test design -> build -> test -> review), pausing for owner decisions. Use when the user asks to build, add, or start a new feature.
argument-hint: <feature idea>
disable-model-invocation: true
---

Feature request: $ARGUMENTS

Before the first feature, `.claude/specs/architecture.md` must exist and be chosen by the owner. If it does not, stop and ask `solution-architect` to propose architecture options from the approved scope in `.claude/docs/product-brief.md`.

Pick a short kebab-case feature name and use it for every file. Each agent ends with a `Handoff` block (see `.claude/rules/workflow.md`); read it before the next step. Stop and ask the owner if `status: blocked`, if `decisions_needed` is not `none`, or if a P0/P1 bug or Critical/High finding is still open after 3 rounds back to `developer`. Otherwise handle `blockers` by the step's own rule. Pass file paths to agents, not contents. Under a delegation (see Delegation in `.claude/rules/workflow.md`) the orchestrator may accept the owner gates inside the accepted scope and records them as "Accepted (delegated)".

## 1. Scope - `product-strategist` (only for features not already accepted in the decision log)
- If the feature is already accepted, say so and pass its decision ID to step 2. If the request changes the agreed scope, run this step.
- Otherwise ask it to evaluate the feature against the brief and decision log and write a [Proposed] decision entry.
- **Stop and show the owner** the recommendation and the decision needed. Continue only after the owner explicitly accepts it, then mark the entry [Accepted] with `log-decision`. If rejected or deferred, record that and end here.

## 2. UX - `ux-designer`
- Pass the accepted decision. Output: `.claude/specs/<name>.md`.
- Show the owner the flow, the step count, and open questions. Resolve them before continuing.

## 3. Architecture - `solution-architect` (only if needed)
- Needed when data models, persistence, structure, frameworks, permissions, or dependencies change. Otherwise say it was skipped and why.
- Output: `.claude/specs/<name>-tech.md`. Lasting choices need owner acceptance, as in step 1.

## 4. Test design first - `tester` (only for pure logic)
- Write a short case list (happy paths and basic cases) in `.claude/specs/<name>-tests.md`, ordered simple to complex, each traced to an acceptance criterion. No test code and no UI tests yet. Skip if the feature has no pure logic, and say so.

## 5. Build - `developer`
- Give it the spec paths and the case list. Pure logic: one group of cases per TDD loop (Red, Green, Refactor). Other code is built normally.
- It writes `.claude/reports/<name>-dev-report.md` with the unit-test result. The full suite runs in step 6.

## 6. Review - `sec-perf-reviewer` (when the change touches data, auth, notifications, export, logging, permissions, or startup)
- Runs right after `developer` and before `tester`: it is fast, and a High finding changes the code the tests would run on. Give it the spec paths and the diff only, not `developer`'s report.
- Send Critical/High findings to `developer` at once; the reviewer then checks the fix diff only, until nothing Critical/High is open (at most 3 rounds, counted apart from test rounds; then stop and ask the owner). Only then start step 7.

## 7. Test - `tester`
- Check the tests against the specs, write the deferred and missing edge cases and UI/end-to-end tests, run the feature run (see Test levels in `.claude/rules/workflow.md`), and write `.claude/reports/<name>-test-report.md`.
- Send P0/P1 bugs back to `developer` and repeat steps 5 and 7 (at most 3 rounds). Round 1 runs the whole feature set; rounds 2 and 3 rerun only failed or touched tests; the last round runs the whole set once more.
- If a fix in this step changes code in the review scope, `sec-perf-reviewer` checks that fix diff before the last test round.

## Finish
Release gate: build, unit tests and the feature's related suites pass, and no Critical/High finding or P0/P1 bug is open. If the gate fails, stop and ask the owner; never relax it.

Don't trust agent-reported facts. Use tool output: read the tester's result file when no source file is newer than it, otherwise run the feature run once yourself. Compare each `files` field with `git status` and tell the owner about any mismatch.

Before a merge into `main`, run the critical set. For several features at once, use `.claude/rules/parallel-sessions.md`.

Open a pull request for the branch; the owner merges.

Summarize for the owner: what was built, the spec files, test results, open findings, every non-`none` `assumptions`, and anything left [Open]. The owner approves, requests changes, or rejects.
