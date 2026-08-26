#!/usr/bin/env bash

set -euo pipefail

: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"

ROOTFS_DIR="build/trivy-secret-jar-rootfs"
REPORT_DIR="build/reports/trivy-secrets"

JSON_REPORT="${REPORT_DIR}/trivy-jar-secrets.json"
SARIF_REPORT="${REPORT_DIR}/trivy-jar-secrets.sarif"

###############################################################################
# Extract packaged JAR
###############################################################################

echo "Preparing packaged JAR for secret scanning..."

bash "${GITHUB_ACTION_PATH}/resources/prepare-jar.sh"

if [[ ! -d "$ROOTFS_DIR" ]]; then
  echo "::error::Extracted JAR root filesystem was not created: ${ROOTFS_DIR}"
  exit 1
fi

###############################################################################
# Scan extracted JAR for secrets
###############################################################################

echo
echo "Running Trivy packaged JAR secret scan..."

bash "${GITHUB_ACTION_PATH}/resources/run-secret-scan.sh" \
  rootfs \
  "$ROOTFS_DIR" \
  "$JSON_REPORT" \
  "$SARIF_REPORT" \
  --skip-dirs META-INF/maven

###############################################################################
# Summary
###############################################################################

echo
echo "Trivy packaged JAR secret scan completed."
echo "Root filesystem: ${ROOTFS_DIR}"
echo "JSON report:      ${JSON_REPORT}"
echo "SARIF report:     ${SARIF_REPORT}"