---
name: build-and-test
description: Build the Micro-journal Xcode project, run the full test suite on the iOS Simulator, and check the 200-line file limit and formatting. Use after finishing any feature or fix, or when asked to run, build, or test the app.
allowed-tools: Bash(xcodebuild:*), Bash(xcrun:*), Bash(swift format:*), Bash(bash .claude/skills/build-and-test/check-file-length.sh:*)
---

Run from the project root. Run all checks and report every result; don't stop at the first failure.

1. **Simulator:** if the destination in `CLAUDE.md` isn't available, pick an available iPhone from `xcrun simctl list devices available` and say which one you used.
2. **Build and test:**
   ```
   xcodebuild test -quiet -project MicroJournal/MicroJournal.xcodeproj -scheme MicroJournal -destination 'platform=iOS Simulator,name=iPhone 17' -resultBundlePath /tmp/mj-tests.xcresult 2>&1 | tail -60
   ```
   Delete the old `/tmp/mj-tests.xcresult` first. This is the full scheme (about 25 minutes, includes `AccessibilityUITests`); `MicroJournal-Fast` skips those but still takes about 32 minutes, so use `-only-testing` for iterating instead (D-030). For a failure summary, run `xcrun xcresulttool get test-results summary --path /tmp/mj-tests.xcresult`.
3. **Format:** `swift format lint --recursive .`
4. **File length:** `bash .claude/skills/build-and-test/check-file-length.sh`

## Report
```
Build: PASS/FAIL   Tests: <passed>/<total> (<failed> failed, <skipped> skipped)
Lint: PASS/FAIL (<n> issues)   Files > 200 lines: <none | list>
Failures: <test name — first relevant error line — file:line>
New warnings: <concurrency/deprecation warnings, if any>
```
If the project or scheme doesn't exist yet, say so instead of guessing.
