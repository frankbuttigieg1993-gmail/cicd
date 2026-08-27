#!/usr/bin/env bash
set -euo pipefail

SARIF_DIR="${SARIF_DIR:?SARIF_DIR is required}"

mapfile -t SARIF_FILES < <(find "$SARIF_DIR" -maxdepth 1 -type f -name '*.sarif' -print | sort)

if (( ${#SARIF_FILES[@]} == 0 )); then
  echo "::error::CodeQL security policy failed because no SARIF report was generated."
  exit 1
fi

TOTAL=0
for sarif in "${SARIF_FILES[@]}"; do
  TOTAL=$((TOTAL + $(jq '[.runs[]?.results[]?] | length' "$sarif")))
done

echo "CodeQL findings: ${TOTAL}"

if (( TOTAL > 0 )); then
  echo "::error::CodeQL security policy failed: ${TOTAL} finding(s) detected."
  exit 1
fi

echo "CodeQL security policy passed."
