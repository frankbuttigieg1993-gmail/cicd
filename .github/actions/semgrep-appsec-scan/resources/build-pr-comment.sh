#!/usr/bin/env bash
set -euo pipefail

RUN_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"

if [[ "$SEMGREP_EXIT_CODE" != "0" ]]; then
  STATUS="BLOCKED"
  MESSAGE="Semgrep AppSec Platform returned a non-zero result. Review the Semgrep findings and policy configuration."
elif (( ERROR_COUNT > 0 || WARNING_COUNT > 0 || NOTE_COUNT > 0 )); then
  STATUS="REVIEW"
  MESSAGE="No blocking Semgrep policy result was returned, but findings are present and should be reviewed."
else
  STATUS="PASSED"
  MESSAGE="No Semgrep findings were returned for this PR scan."
fi

{
  echo "<!-- semgrep-security-report -->"
  echo
  echo "## Semgrep AppSec Security Report"
  echo
  echo "**Products:** Semgrep Code + Semgrep Supply Chain  "
  echo "**Scan mode:** ${SCAN_MODE}  "
  echo "**Baseline:** ${BASELINE:-N/A}  "
  echo "**Scan ID:** ${SCAN_ID:-Unavailable}"
  echo
  echo "| SARIF level | Findings | Treatment |"
  echo "|---|---:|---|"
  echo "| Error | ${ERROR_COUNT} | Security finding |"
  echo "| Warning | ${WARNING_COUNT} | Review |"
  echo "| Note | ${NOTE_COUNT} | Report |"
  echo "| **Total** | **${TOTAL_FINDINGS}** | |"
  echo
  echo "### Security gate: ${STATUS}"
  echo
  echo "${MESSAGE}"
  echo
  echo "[Open Semgrep AppSec Project](${PROJECT_URL})"
  if [[ -n "${SCAN_URL:-}" ]]; then
    echo
    echo "[Open this Semgrep Scan](${SCAN_URL})"
  else
    echo
    echo "**Exact Semgrep scan link unavailable:** scan ID could not be extracted."
  fi
  echo
  echo "[View GitHub Actions Run](${RUN_URL})"
  echo
  echo "_This comment is automatically updated on subsequent scans._"
} > build/reports/semgrep/semgrep-comment.md
