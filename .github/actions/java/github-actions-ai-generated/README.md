# github-actions-ai-generated

Builds and tests a Gradle project, runs SonarQube analysis through the project's
Gradle Sonar plugin, waits for the quality gate, uploads generated reports, and
writes the results to the GitHub Actions step summary.

## Usage

```yaml
- uses: frankbuttigieg1993-gmail/cicd/.github/actions/java/github-actions-ai-generated@main
  with:
    java-version: "21"
    sonar-token: ${{ secrets.SONAR_TOKEN }}
    sonar-host-url: ${{ vars.SONAR_HOST_URL }}
```

The calling workflow must check out the project before invoking this action.
The project must include an executable `gradlew` wrapper and configure the
SonarQube Gradle plugin. The action does not check out code or grant workflow
permissions; give the calling job only the permissions it needs.

## Inputs and behavior

- `build-tasks` defaults to `assemble`; `test-tasks` defaults to `test`. Each is
  a whitespace-separated list of Gradle task names.
- `working-directory` defaults to `.` and must contain `gradlew`.
- `java-version` defaults to `21`; `java-distribution` defaults to `temurin`.
- `sonar-token` and `sonar-host-url` are required. Pass the token from a GitHub
  secret; the token is only exposed to the SonarQube step.
- `sonar-project-key` is optional when the project key is already configured
  in Gradle.
- SonarQube analysis sets `sonar.qualitygate.wait=true`, so analysis or a
  failed quality gate fails the action. The wait timeout defaults to 300
  seconds and can be changed with `sonar-quality-gate-timeout`.
- SonarQube can detect pull requests from GitHub Actions automatically when the
  server integration supports it. To specify PR analysis explicitly, provide
  all of `sonar-pull-request-key`, `sonar-pull-request-branch`, and
  `sonar-pull-request-base`. PR decoration additionally depends on the
  SonarQube edition, server setup, and GitHub permissions.
- Build, test, and SonarQube reports are uploaded as one artifact when present.
  Their URL and each check's outcome are available as action outputs; the
  summary links to the report artifact.

Build, test, and analysis steps continue independently when possible so that
the summary and reports are still produced. A final step fails the action if
Java setup, build, tests, analysis/quality-gate enforcement, report upload, or
summary generation failed.
