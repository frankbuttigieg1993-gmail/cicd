#!/usr/bin/env bash
set -uo pipefail

LOG_FILE="build/reports/semgrep/semgrep-ci.log"
SARIF_FILE="build/reports/semgrep/semgrep.sarif"

echo "========================================"
echo "Starting Semgrep AppSec Platform Scan"
echo "========================================"

# Capture stderr and stdout because verbose Semgrep emits the scan_id in its
# connection/debug output. tee keeps the complete log visible in GitHub Actions.
set +e
/usr/bin/time -v semgrep ci \
  --supply-chain \
  --code \
  --metrics=off \
  --sarif \
  --sarif-output="$SARIF_FILE" \
  --exclude=".cache/" \
  --verbose \
  --no-suppress-errors \
  2>&1 | tee "$LOG_FILE"

SEMGREP_EXIT_CODE=${PIPESTATUS[0]}
set -e

SCAN_ID="$(
  grep -oE 'scan_id=[0-9]+' "$LOG_FILE" \
    | head -n 1 \
    | cut -d= -f2 \
    || true
)"

echo "exit-code=${SEMGREP_EXIT_CODE}" >> "$GITHUB_OUTPUT"
echo "sarif-file=${SARIF_FILE}" >> "$GITHUB_OUTPUT"

if [[ -z "$SCAN_ID" ]]; then
  echo "scan-id=" >> "$GITHUB_OUTPUT"
  echo "scan-url=" >> "$GITHUB_OUTPUT"
  echo "::error::Unable to determine the Semgrep AppSec Platform scan ID from this semgrep ci execution."
else
  SCAN_URL="${SEMGREP_PROJECT_URL%/}/scans/${SCAN_ID}"
  echo "scan-id=${SCAN_ID}" >> "$GITHUB_OUTPUT"
  echo "scan-url=${SCAN_URL}" >> "$GITHUB_OUTPUT"
  echo "Semgrep scan ID: ${SCAN_ID}"
  echo "Semgrep scan URL: ${SCAN_URL}"
fi

echo "========================================"
echo "Finished Semgrep AppSec Platform Scan"
echo "Semgrep exit code: ${SEMGREP_EXIT_CODE}"
echo "========================================"

# Reporting and policy enforcement occur later.
exit 0
