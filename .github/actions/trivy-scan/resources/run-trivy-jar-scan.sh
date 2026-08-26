#!/usr/bin/env bash

# Trivy's Documentation recommends extracting the JAR File before performing the scan

set -euo pipefail

: "${TRIVY_CACHE_DIR:?TRIVY_CACHE_DIR is required}"
: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"

JAR_DIR="build/libs"
ROOTFS_DIR="build/jar-rootfs"
REPORT_DIR="build/reports/trivy"

TRIVY_JSON="${REPORT_DIR}/trivy-jar-report.json"
TRIVY_SARIF="${REPORT_DIR}/trivy-jar-report.sarif"
TRIVY_HTML="${REPORT_DIR}/trivy-jar-report.html"

APPLICATION_SBOM="build/reports/cyclonedx/application-sbom.json"

###############################################################################
# Locate packaged JAR
###############################################################################

JAR="$(
  find "$JAR_DIR" \
    -maxdepth 1 \
    -type f \
    -name '*.jar' \
    | head -n 1
)"

if [[ -z "$JAR" ]]; then
  echo "::error::No packaged JAR was found in ${JAR_DIR}."
  exit 1
fi

echo "Scanning packaged JAR:"
echo "$JAR"

###############################################################################
# Extract packaged JAR
###############################################################################

rm -rf "$ROOTFS_DIR"
mkdir -p "$ROOTFS_DIR"
mkdir -p "$REPORT_DIR"

(
  cd "$ROOTFS_DIR"

  jar xf "../../libs/$(basename "$JAR")"
)

###############################################################################
# Validate Application SBOM
###############################################################################

if [[ ! -f "$APPLICATION_SBOM" ]]; then
  echo "::error::Application SBOM not found: ${APPLICATION_SBOM}"
  exit 1
fi

###############################################################################
# Scan extracted JAR with Trivy
###############################################################################

echo "Running Trivy packaged JAR vulnerability and license scan..."

trivy rootfs \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --scanners vuln,license \
  --format json \
  --output "$TRIVY_JSON" \
  --timeout 40m \
  "$ROOTFS_DIR"

###############################################################################
# Convert Trivy JSON to SARIF
###############################################################################

echo "Converting Trivy JAR results to SARIF..."

trivy convert \
  --format sarif \
  --output "$TRIVY_SARIF" \
  "$TRIVY_JSON"

###############################################################################
# Generate dependency-aware HTML report
###############################################################################

echo "Generating dependency-aware Trivy JAR HTML report..."

python3 "$GITHUB_ACTION_PATH/resources/generate-trivy-html.py" \
  --trivy "$TRIVY_JSON" \
  --sbom "$APPLICATION_SBOM" \
  --output "$TRIVY_HTML"

###############################################################################
# Summary
###############################################################################

echo
echo "Trivy packaged JAR scan completed successfully."
echo
echo "JAR:   $JAR"
echo "JSON:  $TRIVY_JSON"
echo "SARIF: $TRIVY_SARIF"
echo "HTML:  $TRIVY_HTML"