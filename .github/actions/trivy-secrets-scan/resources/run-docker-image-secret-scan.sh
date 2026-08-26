#!/usr/bin/env bash

set -euo pipefail

: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"
: "${GITHUB_SHA:?GITHUB_SHA is required}"

IMAGE_REF="java-application:${GITHUB_SHA}"

REPORT_DIR="build/reports/trivy-secrets"
JSON_REPORT="${REPORT_DIR}/trivy-image-secrets.json"
SARIF_REPORT="${REPORT_DIR}/trivy-image-secrets.sarif"

###############################################################################
# Prepare
###############################################################################

mkdir -p "$REPORT_DIR"

###############################################################################
# Build Docker image
###############################################################################

echo "Building Docker image..."
echo "Image: ${IMAGE_REF}"

docker build \
  --tag "$IMAGE_REF" \
  .

###############################################################################
# Scan Docker image for secrets
###############################################################################

echo
echo "Running Trivy Docker image secret scan..."

bash "${GITHUB_ACTION_PATH}/resources/run-secret-scan.sh" \
  image \
  "$IMAGE_REF" \
  "$JSON_REPORT" \
  "$SARIF_REPORT"

###############################################################################
# Summary
###############################################################################

echo
echo "Trivy Docker image secret scan completed."
echo "Image:        ${IMAGE_REF}"
echo "JSON report:  ${JSON_REPORT}"
echo "SARIF report: ${SARIF_REPORT}"