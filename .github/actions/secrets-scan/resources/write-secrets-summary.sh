#!/usr/bin/env bash
set -euo pipefail

GITLEAKS_FINDINGS="${GITLEAKS_FINDINGS:-0}"
GITLEAKS_SCAN_ERROR="${GITLEAKS_SCAN_ERROR:-0}"
TRIVY_FINDINGS="${TRIVY_FINDINGS:-0}"
TRIVY_EXIT_CODE="${TRIVY_EXIT_CODE:-2}"

SUMMARY_FILE="${SUMMARY_FILE:-build/reports/secrets-scan/secrets-scan-summary.md}"
mkdir -p "$(dirname "$SUMMARY_FILE")"

TOTAL_FINDINGS=$((GITLEAKS_FINDINGS + TRIVY_FINDINGS))

if [[ "$GITLEAKS_SCAN_ERROR" == "1" || "$TRIVY_EXIT_CODE" == "2" ]]; then
  STATUS="SCAN ERROR"
elif (( TOTAL_FINDINGS > 0 )); then
  STATUS="BLOCKED"
else
  STATUS="PASSED"
fi

{
  echo "<!-- secrets-scan-report -->"
  echo
  echo "## 🔐 Secrets Scan"
  echo
  echo "| Scanner | Findings | Status |"
  echo "|---|---:|---|"

  if [[ "$GITLEAKS_SCAN_ERROR" == "1" ]]; then
    echo "| Gitleaks | ${GITLEAKS_FINDINGS} | ❌ Scan Error |"
  elif (( GITLEAKS_FINDINGS > 0 )); then
    echo "| Gitleaks | ${GITLEAKS_FINDINGS} | ❌ Findings Detected |"
  else
    echo "| Gitleaks | 0 | ✅ Passed |"
  fi

  if [[ "$TRIVY_EXIT_CODE" == "2" ]]; then
    echo "| Trivy Secrets | ${TRIVY_FINDINGS} | ❌ Scan Error |"
  elif (( TRIVY_FINDINGS > 0 )); then
    echo "| Trivy Secrets | ${TRIVY_FINDINGS} | ❌ Findings Detected |"
  else
    echo "| Trivy Secrets | 0 | ✅ Passed |"
  fi

  echo "| **Total** | **${TOTAL_FINDINGS}** | |"
  echo
  echo "### Security gate: ${STATUS}"
  echo

  case "$STATUS" in
    PASSED) echo "No secrets were detected by Gitleaks or Trivy." ;;
    BLOCKED) echo "One or more potential secrets were detected. Review the security reports before merging." ;;
    "SCAN ERROR") echo "One or more secret scanners did not complete successfully. Review the workflow logs before treating the repository as clean." ;;
  esac
} > "$SUMMARY_FILE"

cat "$SUMMARY_FILE" >> "$GITHUB_STEP_SUMMARY"
