# Java Test composite action

This version separates Gradle execution status from actual JUnit results.

- Gradle runs the unit tests with `-PignoreFailures=true` so reporting can continue.
- JUnit XML is parsed independently to determine whether tests actually failed.
- Failed tests create a GitHub warning annotation.
- Coverage verification is allowed to complete so reports can be published.
- JUnit and JaCoCo reports are published/uploaded even when tests fail.
- The final quality gate fails the composite action if tests failed or coverage verification failed.
