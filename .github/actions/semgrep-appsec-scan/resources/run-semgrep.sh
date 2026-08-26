#!/usr/bin/env bash

set -uo pipefail

: "${SEMGREP_PROJECT_URL:?SEMGREP_PROJECT_URL is required}"
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

LOG_FILE="build/reports/semgrep/semgrep-ci.log"
SARIF_FILE="build/reports/semgrep/semgrep.sarif"

mkdir -p "$(dirname "$LOG_FILE")"

###############################################################################
# Determine scan mode
###############################################################################

if [[ "${EVENT_NAME:-}" == "pull_request" ]]; then

  if [[ -z "${PR_BASE_SHA:-}" ]]; then
    echo "::error::Pull request event detected but PR base SHA is unavailable."
    exit 1
  fi

  SCAN_MODE="diff-aware"
  BASELINE="$PR_BASE_SHA"

  export SEMGREP_BASELINE_REF="$BASELINE"

else

  SCAN_MODE="full"
  BASELINE=""

  # Ensure a non-PR scan cannot accidentally inherit a baseline.
  unset SEMGREP_BASELINE_REF || true

fi

###############################################################################
# Publish scan-mode outputs
###############################################################################

echo "mode=${SCAN_MODE}" >> "$GITHUB_OUTPUT"
echo "baseline=${BASELINE}" >> "$GITHUB_OUTPUT"

###############################################################################
# Run Semgrep
###############################################################################

echo "========================================"
echo "Starting Semgrep AppSec Platform Scan"
echo "Scan mode: ${SCAN_MODE}"
echo "Baseline: ${BASELINE:-none}"
echo "========================================"

ARGS=(
  ci
  --supply-chain
  --code
  --metrics=off
  --sarif
  --sarif-output="$SARIF_FILE"
  --exclude=".cache/"
  --verbose
  --no-suppress-errors
)

set +e

semgrep "${ARGS[@]}" 2>&1 | tee "$LOG_FILE"
SEMGREP_EXIT_CODE=${PIPESTATUS[0]}

set -e

###############################################################################
# Extract exact Semgrep scan ID
###############################################################################

SCAN_ID="$(
  grep -oE 'scan_id=[0-9]+' "$LOG_FILE" \
    | head -n 1 \
    | cut -d= -f2 \
    || true
)"

###############################################################################
# Publish scan outputs
###############################################################################

echo "exit-code=${SEMGREP_EXIT_CODE}" >> "$GITHUB_OUTPUT"
echo "sarif-file=${SARIF_FILE}" >> "$GITHUB_OUTPUT"

if [[ -n "$SCAN_ID" ]]; then

  SCAN_URL="${SEMGREP_PROJECT_URL%/}/scans/${SCAN_ID}"

  echo "scan-id=${SCAN_ID}" >> "$GITHUB_OUTPUT"
  echo "scan-url=${SCAN_URL}" >> "$GITHUB_OUTPUT"

  echo
  echo "Semgrep scan ID: ${SCAN_ID}"
  echo "Semgrep scan URL: ${SCAN_URL}"

else

  echo "scan-id=" >> "$GITHUB_OUTPUT"
  echo "scan-url=" >> "$GITHUB_OUTPUT"

  echo "::error::Unable to determine the Semgrep AppSec Platform scan ID from this Semgrep execution."

fi

###############################################################################
# Final execution information
###############################################################################

echo
echo "========================================"
echo "Finished Semgrep AppSec Platform Scan"
echo "Scan mode: ${SCAN_MODE}"
echo "Semgrep exit code: ${SEMGREP_EXIT_CODE}"
echo "========================================"

# Do not fail here.
#
# The composite action needs to publish the Step Summary, PR comment and
# reports before the Semgrep policy is ultimately enforced.
exit 0