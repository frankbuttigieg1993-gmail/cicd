#!/usr/bin/env bash
set -euo pipefail

: "${TRIVY_CACHE_DIR:?TRIVY_CACHE_DIR is required}"
: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"

REPORT_DIR="build/reports/trivy"
REPORT_NAME="trivy-configuration"
TRIVY_JSON="${REPORT_DIR}/${REPORT_NAME}.json"
TRIVY_HTML="${REPORT_DIR}/${REPORT_NAME}.html"
TRIVY_SARIF="${REPORT_DIR}/${REPORT_NAME}.sarif"

mkdir -p "$REPORT_DIR"

trivy config \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --format json \
  --output "$TRIVY_JSON" \
  --timeout 10m \
  .

python3 "$GITHUB_ACTION_PATH/resources/generate-trivy-config-html.py" \
  --trivy "$TRIVY_JSON" \
  --output "$TRIVY_HTML" \
  --title "Trivy Configuration Security Report"

trivy convert \
  --format sarif \
  --output "$TRIVY_SARIF" \
  "$TRIVY_JSON"

echo "Trivy configuration scan completed successfully."
echo "JSON:  $TRIVY_JSON"
echo "HTML:  $TRIVY_HTML"
echo "SARIF: $TRIVY_SARIF"