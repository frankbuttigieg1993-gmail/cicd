#!/usr/bin/env bash
set -euo pipefail

: "${CRITICAL_COUNT:?CRITICAL_COUNT is required}"
: "${GRADLE_EXIT_CODE:?GRADLE_EXIT_CODE is required}"
: "${SARIF_GENERATED:?SARIF_GENERATED is required}"

if [[ "$GRADLE_EXIT_CODE" -ne 0 ]]; then
  echo "SpotBugs execution failed with Gradle exit code ${GRADLE_EXIT_CODE}."
  exit 1
fi

if [[ "$SARIF_GENERATED" != "true" ]]; then
  echo "SpotBugs execution failed: SARIF report was not generated."
  exit 1
fi

if [[ "$CRITICAL_COUNT" -gt 0 ]]; then
  echo "SpotBugs / FindSecBugs policy failed: ${CRITICAL_COUNT} critical finding(s)."
  exit 1
fi

echo "SpotBugs / FindSecBugs policy passed: no critical findings."
