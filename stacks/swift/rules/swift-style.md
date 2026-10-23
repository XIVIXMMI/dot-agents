---
paths:
  - "**/*.swift"
---

# Swift & SwiftUI Rules

Single source for Swift conventions. `developer` and `solution-architect` read this file explicitly; other docs link here instead of repeating it.

## Platform
- Swift 6 language mode, strict concurrency (D-001). Deployment target iOS 26, reference device iPhone 17, so no `#available` checks for older versions.
- UI types are `@MainActor`; keep heavy work off the main actor. No `DispatchQueue.main.sync`.
- Persistence is SwiftData, on-device (D-002).

## Style
- 2-space indentation.
- Files: aim for under 200 lines. Going over is a prompt to check whether the file does too much. Split along a real seam (a different responsibility), never just to shrink a line count.
- Small views; extract subviews before a body grows large. Business logic stays out of views.
- Prefer value types. Keep types `private` or `internal` unless they need to be wider.
- Comments explain why, not what. Add a short doc comment on non-obvious APIs, because the owner is learning.

## State & architecture
- `@Observable` for view models that manage real state or logic, not by default for every type. `ObservableObject` is fine when a framework API requires it.
- No new model, type, protocol, or layer unless it solves a real problem (testability, separating logic from persistence).
- SwiftData: `@Query` in views for simple reads; writes go through a small persistence layer behind a protocol, testable with an in-memory `ModelContainer`.
- Inject dependencies (persistence, auth, notifications, clock) through protocols plus `Environment` or initializers. No singletons.
- No new SPM dependency without an [Accepted] decision.

## Safety
- No `!` force unwraps, `try!`, `as!`, or `fatalError` in production code (tests may use `try #require`). Handle errors with a gentle message to the user.
- Never `print` or log journal content. Use `os.Logger` with `privacy: .private` for user data.
- Log and error text says plainly what failed and what the app did about it. No cryptic codes, vague wording, or messages that could mislead or confuse (owner feedback 2026-10-21).

## UI
- Every important view has a `#Preview` with sample data. Use an in-memory `ModelContainer` only when the view depends on persistence; previews never depend on real data.
- User-facing strings go through the String Catalog (`Localizable.xcstrings`), English first (D-005).
- Icon-only buttons get an `accessibilityLabel`; layouts survive Dynamic Type; elements used in UI tests get an `accessibilityIdentifier`.
