---
paths:
  - "**/*Tests/**"
  - "**/*Tests.swift"
---

# Testing Rules

- Unit tests use Swift Testing (`import Testing`, `@Test`, `#expect`, `#require`); UI tests use XCUITest.
- Persistence tests use an in-memory `ModelContainer`, never the real store.
- Inject a fixed clock, calendar, and time zone for any date or streak logic; never depend on "now".
- UI tests find elements by `accessibilityIdentifier`, not visible text, so localization doesn't break them.
- Each test is independent: no shared mutable state and no required order.
- Name tests after the behavior: `savingEmptyEntryIsRejected`, not `test1`.
- A test counts as Red only when it fails by assertion on the missing behavior, not by a build error or broken setup.
- Name a bug's regression test after the correct behavior, and keep it after the fix.
