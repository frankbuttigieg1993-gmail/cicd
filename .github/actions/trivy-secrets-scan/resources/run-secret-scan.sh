#!/usr/bin/env bash
set -euo pipefail

SCAN_TYPE="${1:?scan type is required}"
TARGET="${2:?target is required}"
JSON_OUTPUT="${3:?JSON output path is required}"
SARIF_OUTPUT="${4:?SARIF output path is required}"
shift 4

mkdir -p "$(dirname "$JSON_OUTPUT")"

set +e
trivy "$SCAN_TYPE" \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --scanners secret \
  "$@" \
  --format json \
  --output "$JSON_OUTPUT" \
  --timeout 20m \
  "$TARGET"
COMMAND_EXIT=$?
set -e

if [[ ! -f "$JSON_OUTPUT" ]]; then
  echo "count=0" >> "$GITHUB_OUTPUT"
  echo "scan-error=1" >> "$GITHUB_OUTPUT"
  echo "Trivy ${SCAN_TYPE} secret scan did not produce a report (command exit ${COMMAND_EXIT})."
  exit 0
fi

trivy convert \
  --format sarif \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --output "$SARIF_OUTPUT" \
  "$JSON_OUTPUT"

COUNT=$(jq '[.Results[]?.Secrets[]?] | length' "$JSON_OUTPUT")
echo "count=${COUNT}" >> "$GITHUB_OUTPUT"
echo "scan-error=0" >> "$GITHUB_OUTPUT"
echo "Trivy secret findings: ${COUNT}"
