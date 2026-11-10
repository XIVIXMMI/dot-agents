# Testing Rules (always apply)

Stack-neutral. Put the real commands and framework names in `AGENTS.md` (Commands section).

- Pure logic is built test-first (TDD): one group of related cases per loop. Red, then Green, then Refactor.
- A test counts as Red only when it fails by assertion on the missing behavior, not by a build error, a missing symbol, or a broken setup. Read the failure message.
- A bug fix starts with a test that reproduces the bug and fails. Name it after the correct behavior and keep it after the fix. If the bug cannot be tested, say so in the report.
- Tests are independent: no shared mutable state, no required order.
- Inject the clock, time zone, locale, and randomness; never depend on "now".
- Use fake data only. Never put real user data in tests, specs, or prompts.
- Name tests after the behavior (`rejectsEmptyInput`), not `test1`.
- A test that checks an acceptance criterion carries its ID in the test name: `test_AUTH_3_rejects_empty_title` (case and `-`/`_` do not matter). One test may carry several IDs.
- The traceability matrix (RTM) is generated, never written by hand: after a feature run, `python3 .agents/tools/rtm.py --junit '<JUnit XML glob from Commands or the Stack section>'`. Read only `.agents/reports/rtm-gaps.md`; `rtm.csv` is for the owner.
- Never weaken, delete, or skip a failing test to get green. Report it.
- Priorities for defects: P0 data loss, crash, or privacy leak; P1 core flow broken; P2 minor or cosmetic.
