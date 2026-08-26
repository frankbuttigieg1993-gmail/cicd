#!/usr/bin/env bash

set -euo pipefail

: "${TRIVY_CACHE_DIR:?TRIVY_CACHE_DIR is required}"
: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"
: "${GITHUB_SHA:?GITHUB_SHA is required}"

REPORT_DIR="build/reports/trivy"

TRIVY_JSON="${REPORT_DIR}/trivy-dockerimage-report.json"
TRIVY_SARIF="${REPORT_DIR}/trivy-dockerimage-report.sarif"
TRIVY_HTML="${REPORT_DIR}/trivy-dockerimage-report.html"

APPLICATION_SBOM="build/reports/cyclonedx/all-configs-bom.json"

###############################################################################
# Determine image reference
###############################################################################

if [[ -n "${INPUT_IMAGE_REF:-}" ]]; then
  IMAGE_REF="$INPUT_IMAGE_REF"
else
  IMAGE_REF="java-application:${GITHUB_SHA}"
fi

echo "Docker image: ${IMAGE_REF}"

###############################################################################
# Prepare reports
###############################################################################

mkdir -p "$REPORT_DIR"

if [[ ! -f "$APPLICATION_SBOM" ]]; then
  echo "::error::Application SBOM not found: ${APPLICATION_SBOM}"
  exit 1
fi

###############################################################################
# Build Docker image
###############################################################################

echo
echo "Building Docker image..."

docker build \
  --tag "$IMAGE_REF" \
  .

###############################################################################
# Scan Docker image
###############################################################################

echo
echo "Running Trivy Docker image vulnerability and license scan..."

trivy image \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --scanners vuln,license \
  --format json \
  --output "$TRIVY_JSON" \
  --timeout 40m \
  "$IMAGE_REF"

###############################################################################
# Convert JSON to SARIF
###############################################################################

echo
echo "Converting Trivy Docker image results to SARIF..."

trivy convert \
  --format sarif \
  --output "$TRIVY_SARIF" \
  "$TRIVY_JSON"

###############################################################################
# Generate dependency-aware HTML report
###############################################################################

echo
echo "Generating dependency-aware Docker image HTML report..."

python3 "$GITHUB_ACTION_PATH/resources/generate-trivy-html.py" \
  --trivy "$TRIVY_JSON" \
  --sbom "$APPLICATION_SBOM" \
  --output "$TRIVY_HTML"

###############################################################################
# Outputs
###############################################################################

echo "image-ref=${IMAGE_REF}" >> "$GITHUB_OUTPUT"

###############################################################################
# Summary
###############################################################################

echo
echo "Trivy Docker image scan completed successfully."
echo
echo "Image: $IMAGE_REF"
echo "JSON:  $TRIVY_JSON"
echo "SARIF: $TRIVY_SARIF"
echo "HTML:  $TRIVY_HTML"