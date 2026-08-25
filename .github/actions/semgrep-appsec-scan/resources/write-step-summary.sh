#!/usr/bin/env bash
set -euo pipefail

RUN_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"

if [[ "$SEMGREP_EXIT_CODE" != "0" ]]; then
  STATUS="BLOCKED"
elif (( ERROR_COUNT > 0 || WARNING_COUNT > 0 || NOTE_COUNT > 0 )); then
  STATUS="REVIEW"
else
  STATUS="PASSED"
fi

{
  echo "## Semgrep AppSec Platform"
  echo
  echo "**Scan mode:** ${SCAN_MODE}"
  echo
  echo "**Baseline:** ${BASELINE:-N/A}"
  echo
  echo "**Scan ID:** ${SCAN_ID:-Unavailable}"
  echo
  echo "| SARIF level | Findings |"
  echo "|---|---:|"
  echo "| Error | ${ERROR_COUNT} |"
  echo "| Warning | ${WARNING_COUNT} |"
  echo "| Note | ${NOTE_COUNT} |"
  echo "| **Total** | **${TOTAL_FINDINGS}** |"
  echo
  echo "### Security gate: ${STATUS}"
  echo
  echo "[Open Semgrep AppSec Project](${PROJECT_URL})"
  if [[ -n "${SCAN_URL:-}" && -n "${SCAN_ID:-}" ]]; then
    echo
    echo "**Exact scan:** [Semgrep scan ${SCAN_ID}](${SCAN_URL})"
  else
    echo
    echo "**Exact Semgrep scan link unavailable:** scan ID could not be extracted."
  fi
  echo
  echo "[View GitHub Actions Run](${RUN_URL})"
} >> "$GITHUB_STEP_SUMMARY"
