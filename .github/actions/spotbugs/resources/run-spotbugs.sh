#!/usr/bin/env bash
set +e
mkdir -p build/reports/spotbugs/main
./gradlew --no-daemon classes spotbugsMain
GRADLE_EXIT_CODE=$?
set -e

  echo "gradle-exit-code=${GRADLE_EXIT_CODE}" >> "$GITHUB_OUTPUT"

  if [[ -f build/reports/spotbugs/main/spotbugs.sarif ]]; then
    echo "sarif-generated=true" >> "$GITHUB_OUTPUT"
  else
    echo "::error::SpotBugs SARIF report was not generated."
    echo "sarif-generated=false" >> "$GITHUB_OUTPUT"
  fi

  if [[ -f build/reports/spotbugs/main/spotbugs.xml ]]; then
    echo "xml-generated=true" >> "$GITHUB_OUTPUT"
  else
    echo "::error::SpotBugs XML report was not generated."
    echo "xml-generated=false" >> "$GITHUB_OUTPUT"
  fi

  exit 0