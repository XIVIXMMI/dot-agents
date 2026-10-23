---
name: release-checklist
description: Pre-release checklist for submitting Micro-journal to TestFlight or the App Store — tests, privacy manifest, privacy label, usage descriptions, versioning, App Review risks, and the owner's "shipped" criteria. Use when preparing a TestFlight build or App Store submission.
argument-hint: <testflight | appstore>
disable-model-invocation: true
---

Target: $ARGUMENTS (default: testflight)

Go through each section. Give every item one status, with evidence (file:line or command output):

- **Pass:** verified as meeting the requirement.
- **Fail:** checked and does not meet the requirement.
- **Owner action:** needs the owner (for example, App Store Connect, signing, or a judgment call).
- **N/A:** does not apply to this release; state why.

## 1. Quality
- [ ] Run the `build-and-test` skill: build, full suite, lint, and file length all pass.
- [ ] `tester`: regression of the core flows (capture, history, edit, delete, search, export, app lock, reminders) on iPhone 17 / iOS 26 (D-001), plus one smaller iPhone for layout.
- [ ] `sec-perf-reviewer`: full pre-release review with no Critical/High findings open.
- [ ] Schema migration tested by upgrading from the previous build's data (if any build has shipped).

## 2. Privacy & compliance
- [ ] `PrivacyInfo.xcprivacy` is present, and its required-reason APIs match the code.
- [ ] Info.plist usage descriptions (e.g. `NSFaceIDUsageDescription`) are clear and match the actual use.
- [ ] The App Store privacy label is accurate (expected: "Data Not Collected").
- [ ] A privacy policy URL exists (required by App Store Connect).
- [ ] Export-compliance answer is set. If the app uses no non-exempt encryption, set `ITSAppUsesNonExemptEncryption` to `NO`.

## 3. Build settings
- [ ] Version (`MARKETING_VERSION`) and build number (`CURRENT_PROJECT_VERSION`) are bumped.
- [ ] Release configuration; no debug menus, sample data, or test flags.
- [ ] App icon in all required sizes; launch screen OK; correct display name.

## 4. App Review risks
- [ ] App lock has a passcode fallback; the reviewer can use the app without special setup (or notes explain how).
- [ ] No placeholder or "coming soon" content; no broken links.
- [ ] Screenshots and description match the app; no claims about features that aren't there.

## 5. Owner's "shipped" criteria (App Store only)
- [ ] 30 days of the owner's own daily use with no data loss or serious crashes.
- [ ] Feedback from 5–10 external TestFlight testers reviewed, with P0/P1 issues fixed.

## Report
Include:
1. A summary table: section, item, status, evidence.
2. Blockers: every item marked Fail.
3. Owner actions: items that can't be done from here, such as App Store Connect steps, signing, and screenshots.

Don't archive, upload, or submit anything unless the owner asks.
