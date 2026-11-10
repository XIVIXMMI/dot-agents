## Stack: Swift / iOS
- Build: `xcodebuild -scheme <App> -destination 'platform=iOS Simulator,name=<device>' -quiet build`
- Test, all: `xcodebuild test -scheme <App> -destination '<same>' -quiet`
- Test, one: add `-only-testing:<TestTarget>/<TestClass>/test_AUTH_3_rejectsEmptyTitle`
- JUnit XML (for the RTM): `set -o pipefail && xcodebuild test ... 2>&1 | xcbeautify --report junit --report-path .agents/logs/junit`; Swift packages: `swift test --xunit-output .agents/logs/junit/swift.xml`. RTM glob: `.agents/logs/junit/*.xml`
- Requirement IDs go in the test function name: `func test_AUTH_3_rejectsEmptyTitle()`
- CI needs a macOS runner.
