## Stack: Java / Spring Boot
- Build: `./mvnw -q -DskipTests package` (Gradle: `./gradlew -q assemble`)
- Test, all: `./mvnw -q test` (Gradle: `./gradlew -q test`)
- Test, one: `./mvnw -q test -Dtest='NoteServiceTest#test_AUTH_3*'` (Gradle: `./gradlew test --tests '*AUTH_3*'`)
- JUnit XML (for the RTM) is written by default. RTM glob: `target/surefire-reports/TEST-*.xml` (Gradle: `build/test-results/test/*.xml`)
- Requirement IDs go in the test method name, not only in `@DisplayName` (the XML reports the method name): `void test_AUTH_3_rejectsEmptyTitle()`
