#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${GITHUB_STEP_SUMMARY:-}" ]]; then
  echo "::error::GITHUB_STEP_SUMMARY is not set; unable to publish the action summary."
  exit 1
fi

status_label() {
  case "$1" in
    success) printf '✅ Succeeded' ;;
    failure) printf '❌ Failed (see the step logs)' ;;
    skipped) printf '⏭️ Skipped' ;;
    *) printf '⚠️ %s' "${1:-unknown}" ;;
  esac
}

{
  echo "## Gradle build, tests, and SonarQube"
  echo
  echo "| Check | Result |"
  echo "| --- | --- |"
  printf '| Java setup | %s |\n' "$(status_label "${SETUP_STATUS:-}")"
  printf '| Gradle build | %s |\n' "$(status_label "${BUILD_STATUS:-}")"
  printf '| Unit tests | %s |\n' "$(status_label "${TEST_STATUS:-}")"
  printf '| SonarQube analysis | %s |\n' "$(status_label "${SONAR_STATUS:-}")"
  printf '| Quality gate | %s |\n' "${QUALITY_GATE_STATUS:-NOT_PASSED}"
  echo
  echo "The quality gate is enforced by waiting for the result in the Gradle Sonar task."
  echo "On failure, see the corresponding action step logs for Gradle or SonarQube details."
  echo
  if [[ -n "${REPORT_ARTIFACT_URL:-}" && "$REPORT_ARTIFACT_URL" == https://* && "$REPORT_ARTIFACT_URL" != *[[:space:]\(\)]* ]]; then
    printf '[Download Gradle test and SonarQube reports](%s)\n' "$REPORT_ARTIFACT_URL"
  else
    echo "No report artifact was available."
  fi
} >> "$GITHUB_STEP_SUMMARY"
