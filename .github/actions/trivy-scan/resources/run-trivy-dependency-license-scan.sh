#!/usr/bin/env bash
set -euo pipefail

: "${TRIVY_CACHE_DIR:?TRIVY_CACHE_DIR is required}"
: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"

REPORT_DIR="build/reports/trivy"
TRIVY_JSON="$REPORT_DIR/trivy-dependency-license.json"
TRIVY_SARIF="$REPORT_DIR/trivy-dependency-license.sarif"
TRIVY_HTML="$REPORT_DIR/trivy-dependency-license-report.html"
APPLICATION_SBOM="build/reports/cyclonedx/application-sbom.json"

mkdir -p "$REPORT_DIR"

[[ -f "$APPLICATION_SBOM" ]] || {
  echo "::error::CycloneDX application SBOM not found: $APPLICATION_SBOM"
  exit 1
}

trivy fs \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --scanners vuln,license \
  --format json \
  --output "$TRIVY_JSON" \
  --timeout 40m \
  .

trivy convert \
  --format sarif \
  --output "$TRIVY_SARIF" \
  "$TRIVY_JSON"

python3 "$GITHUB_ACTION_PATH/resources/generate-trivy-html.py" \
  --trivy "$TRIVY_JSON" \
  --sbom "$APPLICATION_SBOM" \
  --output "$TRIVY_HTML"

echo "Trivy dependency and license scan completed successfully."