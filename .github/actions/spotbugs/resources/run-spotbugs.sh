#!/usr/bin/env bash
set +e
./gradlew --no-daemon spotbugsMain
GRADLE_EXIT_CODE=$?
set -e

echo "gradle-exit-code=${GRADLE_EXIT_CODE}" >> "$GITHUB_OUTPUT"

if [[ "$GRADLE_EXIT_CODE" -ne 0 ]]; then
  echo "::error::SpotBugs execution failed with Gradle exit code ${GRADLE_EXIT_CODE}."
fi

if [[ -f build/reports/spotbugs/main/spotbugs.sarif ]]; then
  echo "sarif-generated=true" >> "$GITHUB_OUTPUT"
else
  echo "::error::SpotBugs SARIF report was not generated."
  echo "sarif-generated=false" >> "$GITHUB_OUTPUT"
fi

exit 0
