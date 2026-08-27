#!/usr/bin/env bash
set -euo pipefail

: "${TRIVY_CACHE_DIR:?TRIVY_CACHE_DIR is required}"
: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"
: "${GITHUB_SHA:?GITHUB_SHA is required}"
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

REPORT_DIR="build/reports/trivy"
REPORT_NAME="trivy-docker-image"
TRIVY_JSON="${REPORT_DIR}/${REPORT_NAME}.json"
TRIVY_SARIF="${REPORT_DIR}/${REPORT_NAME}.sarif"
TRIVY_HTML="${REPORT_DIR}/${REPORT_NAME}.html"
APPLICATION_SBOM="build/reports/cyclonedx/application-sbom.json"

IMAGE_REF="${INPUT_IMAGE_REF:-java-application:${GITHUB_SHA}}"

mkdir -p "$REPORT_DIR"

[[ -f "$APPLICATION_SBOM" ]] || {
  echo "::error::Application SBOM not found: ${APPLICATION_SBOM}"
  exit 1
}

docker build --tag "$IMAGE_REF" .

trivy image \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --scanners vuln,license \
  --format json \
  --output "$TRIVY_JSON" \
  --timeout 40m \
  "$IMAGE_REF"

trivy convert \
  --format sarif \
  --output "$TRIVY_SARIF" \
  "$TRIVY_JSON"

python3 "$GITHUB_ACTION_PATH/resources/generate-trivy-html.py" \
  --trivy "$TRIVY_JSON" \
  --sbom "$APPLICATION_SBOM" \
  --output "$TRIVY_HTML"

echo "image-ref=${IMAGE_REF}" >> "$GITHUB_OUTPUT"

echo "Trivy Docker image scan completed successfully."
echo "Image: $IMAGE_REF"
echo "JSON:  $TRIVY_JSON"
echo "SARIF: $TRIVY_SARIF"
echo "HTML:  $TRIVY_HTML"