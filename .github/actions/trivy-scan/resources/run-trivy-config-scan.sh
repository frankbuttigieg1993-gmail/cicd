#!/usr/bin/env bash

set -euo pipefail

: "${TRIVY_CACHE_DIR:?TRIVY_CACHE_DIR is required}"
: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"

REPORT_DIR="build/reports/trivy"

TRIVY_JSON="${REPORT_DIR}/trivy-config-report.json"
TRIVY_HTML="${REPORT_DIR}/trivy-config-report.html"
TRIVY_SARIF="${REPORT_DIR}/trivy-config-report.sarif"

HTML_TEMPLATE="${GITHUB_ACTION_PATH}/resources/trivy-v0.72.0-html-template.tpl"

###############################################################################
# Prepare reports
###############################################################################

mkdir -p "$REPORT_DIR"

if [[ ! -f "$HTML_TEMPLATE" ]]; then
  echo "::error::Trivy HTML template not found: ${HTML_TEMPLATE}"
  exit 1
fi

###############################################################################
# Run Trivy configuration scan
###############################################################################

echo "Running Trivy configuration scan..."

trivy config \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --format json \
  --output "$TRIVY_JSON" \
  --timeout 10m \
  .

###############################################################################
# Convert JSON to HTML
###############################################################################

echo
echo "Generating Trivy configuration HTML report..."

trivy convert \
  --format template \
  --template "@${HTML_TEMPLATE}" \
  --output "$TRIVY_HTML" \
  "$TRIVY_JSON"

###############################################################################
# Convert JSON to SARIF
###############################################################################

echo
echo "Converting Trivy configuration results to SARIF..."

trivy convert \
  --format sarif \
  --output "$TRIVY_SARIF" \
  "$TRIVY_JSON"

###############################################################################
# Summary
###############################################################################

echo
echo "Trivy configuration scan completed successfully."
echo
echo "JSON:  $TRIVY_JSON"
echo "HTML:  $TRIVY_HTML"
echo "SARIF: $TRIVY_SARIF"