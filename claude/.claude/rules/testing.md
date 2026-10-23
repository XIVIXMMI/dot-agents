# Testing Rules (always apply)

Stack-neutral. Put the real commands and framework names in `CLAUDE.md` (Commands section).

- Pure logic is built test-first (TDD): one group of related cases per loop. Red, then Green, then Refactor.
- A test counts as Red only when it fails by assertion on the missing behavior, not by a build error, a missing symbol, or a broken setup. Read the failure message.
- A bug fix starts with a test that reproduces the bug and fails. Name it after the correct behavior and keep it after the fix. If the bug cannot be tested, say so in the report.
- Tests are independent: no shared mutable state, no required order.
- Inject the clock, time zone, locale, and randomness; never depend on "now".
- Use fake data only. Never put real user data in tests, specs, or prompts.
- Name tests after the behavior (`rejectsEmptyInput`), not `test1`.
- Never weaken, delete, or skip a failing test to get green. Report it.
- Priorities for defects: P0 data loss, crash, or privacy leak; P1 core flow broken; P2 minor or cosmetic.
