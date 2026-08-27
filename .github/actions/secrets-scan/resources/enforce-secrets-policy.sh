#!/usr/bin/env bash
set -euo pipefail

GITLEAKS_FINDINGS="${GITLEAKS_FINDINGS:-0}"
GITLEAKS_SCAN_ERROR="${GITLEAKS_SCAN_ERROR:-0}"

TRIVY_FINDINGS="${TRIVY_FINDINGS:-0}"
TRIVY_SCAN_ERROR="${TRIVY_SCAN_ERROR:-0}"

###############################################################################
# Validate values
###############################################################################

if ! [[ "$GITLEAKS_FINDINGS" =~ ^[0-9]+$ ]]; then
  echo "Invalid Gitleaks finding count: ${GITLEAKS_FINDINGS}"
  exit 1
fi

if ! [[ "$TRIVY_FINDINGS" =~ ^[0-9]+$ ]]; then
  echo "Invalid Trivy finding count: ${TRIVY_FINDINGS}"
  exit 1
fi

###############################################################################
# Scan execution errors take precedence over findings.
###############################################################################

if [[ "$GITLEAKS_SCAN_ERROR" == "1" || "$TRIVY_SCAN_ERROR" == "1" ]]; then

  echo "Secrets scan policy failed because one or more scanners did not complete successfully."
  echo
  echo "Gitleaks scan error: ${GITLEAKS_SCAN_ERROR}"
  echo "Trivy scan error:    ${TRIVY_SCAN_ERROR}"

  exit 1
fi

###############################################################################
# Secret findings
###############################################################################

TOTAL_FINDINGS=$((GITLEAKS_FINDINGS + TRIVY_FINDINGS))

if (( TOTAL_FINDINGS > 0 )); then

  echo "Secrets scan policy failed."
  echo
  echo "Gitleaks findings: ${GITLEAKS_FINDINGS}"
  echo "Trivy findings:    ${TRIVY_FINDINGS}"
  echo "Total findings:    ${TOTAL_FINDINGS}"

  exit 1
fi

###############################################################################
# Passed
###############################################################################

echo "Secrets scan policy passed."
echo
echo "Gitleaks findings: 0"
echo "Trivy findings:    0"

exit 0