#!/usr/bin/env bash
set -euo pipefail

RUN_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"

if [[ "$SEMGREP_EXIT_CODE" != "0" ]]; then
  STATUS="BLOCKED"
elif (( PLATFORM_TOTAL_FINDINGS > 0 )); then
  STATUS="REVIEW"
else
  STATUS="PASSED"
fi

{
  echo "## Semgrep AppSec Platform"
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

  echo "| Code | ${CODE_FINDINGS} |"

  if [[ -n "${SUPPLY_CHAIN_FINDINGS_URL:-}" ]]; then
    echo "| Supply Chain | [${SUPPLY_CHAIN_FINDINGS}](${SUPPLY_CHAIN_FINDINGS_URL}) |"
  else
    echo "| Supply Chain | ${SUPPLY_CHAIN_FINDINGS} |"
  fi
  echo "| Secrets | ${SECRETS_FINDINGS} |"
  echo "| **Total** | **${PLATFORM_TOTAL_FINDINGS}** |"
  echo
  echo "### Security gate: ${STATUS}"
  echo
  echo "[Open Semgrep AppSec Project](${PROJECT_URL})"

  if [[ -n "${SCAN_URL:-}" ]]; then
    echo
    echo "[Open this Semgrep Scan](${SCAN_URL})"
  fi

  echo
  echo "[View GitHub Actions Run](${RUN_URL})"
} >> "$GITHUB_STEP_SUMMARY"
