#!/usr/bin/env bash

set -euo pipefail

: "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

REPORT_DIR="build/reports/gitleaks"
SARIF_FILE="${REPORT_DIR}/gitleaks.sarif"

mkdir -p "$REPORT_DIR"

###############################################################################
# Run Gitleaks
###############################################################################

echo "Running Gitleaks against Git repository history..."

set +e

gitleaks git . \
  --redact \
  --report-format sarif \
  --report-path "$SARIF_FILE" \
  --verbose

EXIT_CODE=$?

set -e

###############################################################################
# Ensure a SARIF report always exists
###############################################################################

if [[ ! -f "$SARIF_FILE" ]]; then
  echo "Gitleaks did not produce a SARIF report. Creating an empty SARIF file."

  printf '%s\n' \
    '{"version":"2.1.0","$schema":"https://json.schemastore.org/sarif-2.1.0.json","runs":[{"tool":{"driver":{"name":"Gitleaks"}},"results":[]}]}' \
    > "$SARIF_FILE"
fi

###############################################################################
# Publish composite-action step outputs
###############################################################################

{
  echo "exit-code=${EXIT_CODE}"
  echo "sarif-file=${SARIF_FILE}"
} >> "$GITHUB_OUTPUT"

###############################################################################
# Complete
###############################################################################

echo
echo "Gitleaks scan completed."
echo "Exit code:  ${EXIT_CODE}"
echo "SARIF file: ${SARIF_FILE}"

# Do not enforce the security policy here. The Gitleaks enforcement step
# evaluates this scan's exit code/findings after reporting has completed.
exit 0