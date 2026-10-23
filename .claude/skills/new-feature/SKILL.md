---
name: new-feature
description: Take a Micro-journal feature from idea to tested code through the agent pipeline (strategy → UX → architecture → implementation → tests → review), pausing for owner decisions. Use when the user asks to build, add, or start a new feature.
argument-hint: <feature idea>
disable-model-invocation: true
---

Feature request: $ARGUMENTS

Before the first feature, `.claude/specs/architecture.md` must exist and be chosen by the owner (D-009). If it does not, stop and ask `solution-architect` to propose architecture options from the approved v1 feature list.

Pick a short kebab-case feature name (e.g. `quick-capture`) and use it for every spec file.
Each agent ends with a `Handoff` block (see `.claude/rules/workflow.md`). Read it before starting the next step. Stop and ask the owner if `status: blocked` or `decisions_needed` is not `none`, or if a P0/P1 bug or Critical/High finding is still open after 3 rounds back to `developer`. Otherwise handle `blockers` by the step's own rule below.

## 1. Scope — `product-strategist` (only for features not in the accepted v1 list, D-010)
- Skip this step for a feature already accepted in D-010 (quick-entry, entry-history, daily-reminder, app-lock, export-entries), say so, and pass D-010 to step 2. If the request changes that feature's agreed scope, run this step.
- Otherwise ask it to evaluate the feature against the brief and decision log, and to write a [Proposed] decision entry.
- **Stop and show the owner** the recommendation and the decision needed. Continue only after the owner explicitly accepts it. Then mark that entry [Accepted] with the date, using the `log-decision` skill.
- If the owner rejects or defers it, record that and end here.

## 2. UX — `ux-ui-designer`
- Pass along the accepted decision. Output: `.claude/specs/<name>.md`.
- Show the owner the flow, the tap count, and any open questions. Resolve the open questions before continuing.

## 3. Architecture — `solution-architect` (only if needed)
- Needed when data models, persistence, app structure, frameworks, permissions, or dependencies change. Otherwise say it was skipped and why.
- Output: `.claude/specs/<name>-tech.md`. Any lasting choice needs owner acceptance, as in step 1.

## 4. Test design first — `tester` (only for pure logic: dates, streaks, formatting, persistence layer)
- Write a short case list (happy paths and basic cases) in `.claude/specs/<name>-tests.md` from the acceptance criteria, ordered simple to complex, each traced to a criterion. No test code and no UI tests yet. Skip this step if the feature has no pure logic, and say so. Edge cases and UI tests come in step 6.

## 5. Build — `developer`
- Other code (views, wiring) is built normally.
- Pure logic: one group of related cases per TDD loop, run quietly (see `developer.md`). Red must fail by assertion on the missing behavior, then Green, then Refactor without changing behavior.
- A bug found later gets a failing test that reproduces it first.
- Give it the spec paths and the case list. It writes `.claude/reports/<name>-dev-report.md` (D-021) with the unit-test result; the full suite runs in step 6.

## 6. Test — `tester`
- Check the tests against the specs (catch tests that only mirror the code), write the deferred and missing edge cases (a failing one is a bug, report it with that test) and UI tests (XCUITest), update the test plan, run the suite, and write the report to `.claude/reports/<name>-test-report.md`. Send any P0/P1 bugs back to `developer` and repeat steps 5–6 until resolved (at most 3 rounds, see the top). In a fix round run `MicroJournal-Fast` plus the related suites (D-020); run the full scheme `MicroJournal` only in the last round, and record its scheme and result bundle path in the report.

## 7. Review — `sec-perf-reviewer` (when the change touches data, auth, notifications, export, logging, permissions, or launch)
- Give it the spec paths and the diff only, not `developer`'s report. Send Critical/High findings back to `developer`, then re-test the unit tests and the related suites (same 3-round limit, D-020, D-030).

## Finish
Release gate: build and the full suite pass, and no Critical/High finding or P0/P1 bug is open. If the gate fails, stop and ask the owner; never relax it.

Release build: run it once here, with the `strings` check (no `uiTesting` or `SampleData` in the binary), not in every fix round. If it fails, fix and retry at most 2 times in total, then stop and ask the owner. Skip it when the diff touches no build settings, previews, `#if DEBUG` code or files outside the app target.

Don't trust agent-reported facts. Use tool output, not the `tests:` values: run the `build-and-test` skill yourself, or read the tester's full-scheme `.xcresult` (path in its report) when no source file is newer than it (`find MicroJournal -name '*.swift' -newer <xcresult>` prints nothing); otherwise run it (D-020). Compare the `files=` fields with `git status`, and tell the owner about any mismatch.

Owner decision: the owner approves, requests changes, or rejects the release. Summarize for the owner: what was built, the spec files, test results, open findings, every non-`none` `assumptions` from the Handoff blocks, and anything left [Open].
