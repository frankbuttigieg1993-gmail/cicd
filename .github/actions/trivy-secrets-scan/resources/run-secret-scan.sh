#!/usr/bin/env bash
set -euo pipefail

SCAN_TYPE="${1:?scan type is required}"
TARGET="${2:?target is required}"
JSON_OUTPUT="${3:?JSON output path is required}"
SARIF_OUTPUT="${4:?SARIF output path is required}"
TRIVY_SECRET_CONFIG="${GITHUB_ACTION_PATH}/resources/trivy-secret.yaml"
shift 4

mkdir -p "$(dirname "$JSON_OUTPUT")" "$(dirname "$SARIF_OUTPUT")"

ERROR_OUTPUT="${JSON_OUTPUT%.json}.error.log"
rm -f "$JSON_OUTPUT" "$SARIF_OUTPUT" "$ERROR_OUTPUT"

if ! command -v trivy >/dev/null 2>&1; then
  echo "::error::Trivy CLI is not available on PATH."
  echo "count=0" >> "$GITHUB_OUTPUT"
  echo "scan-error=1" >> "$GITHUB_OUTPUT"
  echo "command-exit-code=127" >> "$GITHUB_OUTPUT"
  exit 0
fi

set +e
trivy "$SCAN_TYPE" \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --scanners secret \
  --secret-config "$TRIVY_SECRET_CONFIG" \
  --secret-config "${TRIVY_SECRET_CONFIG:?TRIVY_SECRET_CONFIG is required}" \
  "$@" \
  --format json \
  --output "$JSON_OUTPUT" \
  --timeout 20m \
  "$TARGET" \
  2>"$ERROR_OUTPUT"
COMMAND_EXIT=$?
set -e

echo "command-exit-code=${COMMAND_EXIT}" >> "$GITHUB_OUTPUT"

if [[ "$COMMAND_EXIT" -ne 0 || ! -s "$JSON_OUTPUT" ]]; then
  echo "count=0" >> "$GITHUB_OUTPUT"
  echo "scan-error=1" >> "$GITHUB_OUTPUT"
  echo "::error::Trivy ${SCAN_TYPE} secret scan failed with exit code ${COMMAND_EXIT}."

  if [[ -s "$ERROR_OUTPUT" ]]; then
    echo "----- Trivy error output -----"
    cat "$ERROR_OUTPUT"
    echo "------------------------------"
  fi
  exit 0
fi

COUNT="$(python3 - "$JSON_OUTPUT" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)

print(sum(len(result.get("Secrets") or []) for result in data.get("Results") or []))
PY
)"

echo "count=${COUNT}" >> "$GITHUB_OUTPUT"
echo "scan-error=0" >> "$GITHUB_OUTPUT"

set +e
trivy "$SCAN_TYPE" \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --scanners secret \
  --secret-config "$TRIVY_SECRET_CONFIG" \
  --secret-config "${TRIVY_SECRET_CONFIG:?TRIVY_SECRET_CONFIG is required}" \
  "$@" \
  --format sarif \
  --output "$SARIF_OUTPUT" \
  --timeout 20m \
  "$TARGET" \
  2>>"$ERROR_OUTPUT"
SARIF_EXIT=$?
set -e

if [[ "$SARIF_EXIT" -ne 0 || ! -s "$SARIF_OUTPUT" ]]; then
  echo "::warning::Trivy JSON scan succeeded, but SARIF generation failed with exit code ${SARIF_EXIT}."
  rm -f "$SARIF_OUTPUT"
fi
