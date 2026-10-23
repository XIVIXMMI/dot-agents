# Micro-journal (iOS, SwiftUI)

## Context
Micro-journaling app for busy people: one entry in 10–60 seconds, private, gentle.
Goal: learn Swift/iOS by shipping a complete app to the App Store.
Owner: Nguyen, who makes all final decisions — every proposal must state its trade-offs.

## Product Rules
- Minimalism over feature count; speed over complexity.
- Streaks never create pressure — soft, encouraging language only (no "you broke your streak").
- Privacy by default: local-first. Add a backend, AI, or analytics only with owner-approved need.
- Prefer native Apple frameworks (SwiftUI, SwiftData, LocalAuthentication, UserNotifications) over third-party deps; no new dependency without an owner-approved decision.

## Docs
Read the decision index before proposing or building anything.
- `.claude/docs/product-brief.md` — vision, scope, assumptions, risks.
- `.claude/docs/decision-logs.md` — decision index and recent/open entries; older closed ones in `decision-archive.md`. Only **[Accepted]** decisions are binding; [Proposed]/[Hypothesis]/[Open] need owner sign-off before implementing.
- Agents: `.claude/agents/`. Rules: `.claude/rules/` (`workflow`, `swift-style`, `testing`, `copy-tone`, `privacy`). Skills: `.claude/skills/` (start features with `/new-feature`). Third-party skills are vendored with a notice in `.claude/skills/THIRD-PARTY-NOTICES.md`.
- Specs: `.claude/specs/<feature>[-tech|-tests].md`; one-off test reports and audits: `.claude/reports/` (not needed to build a feature). Diagram of the agent pipeline: `.claude/docs/agent-pipeline.svg`.
- When the owner corrects how you work or states a repeated preference, add one line to `.claude/docs/owner-feedback.md` (date, feedback, how to apply). If it should become a lasting rule, propose it for `.claude/rules/` or `/log-decision`.

## Project Structure
Xcode project: `MicroJournal/MicroJournal.xcodeproj` (app, `MicroJournalTests` unit target, `MicroJournalUITests` UI target). App code is in `MicroJournal/MicroJournal/`:
- `App/` entry point, environment wiring, root tabs (Write, Entries, Settings).
- `Core/` shared code: `Persistence` (SwiftData schema, `EntryStore`), `Dates`, `Text`, `Design` (theme), `Notifications`.
- `Features/` one folder per feature: `Capture`, `History`, `Settings`.
Specs for each feature are in `.claude/specs/`. Pure logic lives in small `nonisolated` structs so unit tests need no UI.

## Commands
Run from the repo root. The scheme and project are in the `MicroJournal/` subfolder, so pass `-project`.
- Build: `xcodebuild -quiet -project MicroJournal/MicroJournal.xcodeproj -scheme MicroJournal -destination 'platform=iOS Simulator,name=iPhone 17' build`
- Test, everything (about 25 min, includes accessibility audits): same line with `test`.
- Test, fast loop (skips `AccessibilityUITests`): scheme `MicroJournal-Fast`. It saves only about 2 of 34 minutes because the UI tests dominate (D-030), so while iterating run the unit tests and the related suites with `-only-testing`; the full scheme is the one that counts at the end of a feature.
- Test one suite: add `-only-testing:<target>/<suite>`. Note: `-only-testing` does not override what a scheme skips.
- Always run tests with `-quiet` and read failures with `xcrun xcresulttool get test-results summary`; never load the raw xcodebuild log into context.
- Lint/format: `swift format lint --recursive .` (fix: `swift format --in-place --recursive .`)
- File length: `bash .claude/skills/build-and-test/check-file-length.sh` (Swift files, 200 lines).
- UI tests start the app with DEBUG-only launch arguments (`-uiTesting`, `-uiTestingSeed`, ...). They must never appear in a Release build; `/new-feature` checks this with `strings` at Finish.

## Workflow
**IMPORTANT:** The full test suite (`build-and-test` skill) runs after every feature: `tester` runs it in the last round (fix rounds run only the unit tests and the related suites, D-030), then the orchestrator verifies it by running it again or by reading the tester's unchanged `.xcresult` (D-020). `developer` runs unit tests only. Report the result. Never call a feature done while tests fail.

- Plugin `ponytail` (D-006): when it conflicts with this file or `.claude/rules/`, project rules win. The `Handoff` block replaces ponytail's closing note for agents (D-020, D-029).
