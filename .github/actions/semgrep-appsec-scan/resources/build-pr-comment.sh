#!/usr/bin/env bash
set -euo pipefail

RUN_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"

if [[ "$SEMGREP_EXIT_CODE" != "0" ]]; then
  STATUS="BLOCKED"
  MESSAGE="Semgrep AppSec Platform returned a non-zero result. Review the Semgrep findings and policy configuration."
elif (( PLATFORM_TOTAL_FINDINGS > 0 )); then
  STATUS="REVIEW"
  MESSAGE="No blocking Semgrep policy result was returned, but findings are present and should be reviewed."
else
  STATUS="PASSED"
  MESSAGE="No Semgrep findings were returned for this scan."
fi

{
  echo "<!-- semgrep-security-report -->"
  echo
  echo "## Semgrep AppSec Security Report"
  echo
  echo "**Products:** Semgrep Code + Semgrep Supply Chain"
  echo
  echo "**Scan mode:** ${SCAN_MODE:-N/A}"
  echo
  echo "**Branch:** ${SEMGREP_BRANCH:-N/A}"
  echo
  echo "**Baseline:** ${BASELINE:-N/A}"
  echo
  echo "**Scan ID:** ${SCAN_ID:-Unavailable}"
  echo
  echo "| Product | Findings |"
  echo "|---|---:|"

  if [[ -n "${CODE_FINDINGS_URL:-}" ]]; then
    echo "| Code | [${CODE_FINDINGS}](${CODE_FINDINGS_URL}) |"
  else
    echo "| Code | ${CODE_FINDINGS} |"
  fi

  echo "| Supply Chain | ${SUPPLY_CHAIN_FINDINGS} |"
  echo "| Secrets | ${SECRETS_FINDINGS} |"
  echo "| **Total** | **${PLATFORM_TOTAL_FINDINGS}** |"
  echo
  echo "### Security gate: ${STATUS}"
  echo
  echo "${MESSAGE}"
  echo
  echo "[Open Semgrep AppSec Project](${PROJECT_URL})"

  if [[ -n "${SCAN_URL:-}" ]]; then
    echo
    echo "[Open this Semgrep Scan](${SCAN_URL})"
  fi

  if [[ -n "${CODE_FINDINGS_URL:-}" ]]; then
    echo
    echo "[Open Code Findings](${CODE_FINDINGS_URL})"
  fi

  echo
  echo "[View GitHub Actions Run](${RUN_URL})"
  echo
  echo "_This comment is automatically updated on subsequent scans._"
} > build/reports/semgrep/semgrep-comment.md
