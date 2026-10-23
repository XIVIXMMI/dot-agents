# Privacy Rules (always apply)

Journal entries are private thoughts. Treat every leak as a P0 bug.

- **No network in v1:** no `URLSession`, analytics, crash-reporting SDKs, remote config, or web views loading remote content, unless an [Accepted] decision allows it.
- **Storage:** entries live only in the on-device SwiftData store, protected with Data Protection. Never put entry content in `UserDefaults`, caches, temp files, logs, or Spotlight.
- **Development:** use only fake sample data in prompts, tests, specs, previews, and simulator screenshots. Never paste real journal entries.
- **Notifications** never include entry content.
- **App lock:** when enabled, hide content in the app switcher and re-lock after backgrounding.
- **Export** only to a destination the user picks; delete temp export files afterwards.
- **Permissions:** request one (Face ID, notifications) only at the moment it's needed, with a clear usage description.
- Keep `PrivacyInfo.xcprivacy` and the App Store privacy label accurate whenever APIs or data handling change.
