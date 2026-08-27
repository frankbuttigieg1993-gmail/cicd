#!/usr/bin/env bash
set -euo pipefail

CODE_FINDINGS="${CODE_FINDINGS:-0}"
SUPPLY_CHAIN_FINDINGS="${SUPPLY_CHAIN_FINDINGS:-0}"
SECRETS_FINDINGS="${SECRETS_FINDINGS:-0}"
PLATFORM_TOTAL_FINDINGS="${PLATFORM_TOTAL_FINDINGS:-0}"

if [[ "${SEMGREP_EXIT_CODE:-1}" != "0" ]]; then STATUS="BLOCKED"
elif (( PLATFORM_TOTAL_FINDINGS > 0 )); then STATUS="REVIEW"
else STATUS="PASSED"; fi

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
  if (( CODE_FINDINGS > 0 )) && [[ -n "${CODE_FINDINGS_URL:-}" ]]; then
    echo "| Code | [${CODE_FINDINGS}](${CODE_FINDINGS_URL}) |"
  else
    echo "| Code | ${CODE_FINDINGS} |"
  fi
  if (( SUPPLY_CHAIN_FINDINGS > 0 )) && [[ -n "${SUPPLY_CHAIN_FINDINGS_URL:-}" ]]; then
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
  if [[ -n "${SCAN_URL:-}" ]]; then echo; echo "[Open this Semgrep Scan](${SCAN_URL})"; fi
} >> "$GITHUB_STEP_SUMMARY"
