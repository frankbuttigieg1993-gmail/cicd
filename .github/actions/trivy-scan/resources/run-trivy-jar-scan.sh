#!/usr/bin/env bash
set -euo pipefail

: "${TRIVY_CACHE_DIR:?TRIVY_CACHE_DIR is required}"
: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"

JAR_DIR="build/libs"
ROOTFS_DIR="build/jar-rootfs"
REPORT_DIR="build/reports/trivy"
REPORT_NAME="trivy-packaged-jar"
TRIVY_JSON="${REPORT_DIR}/${REPORT_NAME}.json"
TRIVY_SARIF="${REPORT_DIR}/${REPORT_NAME}.sarif"
TRIVY_HTML="${REPORT_DIR}/${REPORT_NAME}.html"
APPLICATION_SBOM="build/reports/cyclonedx/application-sbom.json"

JAR="$(find "$JAR_DIR" -maxdepth 1 -type f -name '*.jar' ! -name '*-plain.jar' | head -n 1)"

if [[ -z "$JAR" ]]; then
  echo "::error::No packaged application JAR was found in ${JAR_DIR}."
  exit 1
fi

rm -rf "$ROOTFS_DIR"
mkdir -p "$ROOTFS_DIR" "$REPORT_DIR"

(
  cd "$ROOTFS_DIR"
  jar xf "../libs/$(basename "$JAR")"
)

[[ -f "$APPLICATION_SBOM" ]] || {
  echo "::error::Application SBOM not found: ${APPLICATION_SBOM}"
  exit 1
}

trivy rootfs \
  --cache-dir "$TRIVY_CACHE_DIR" \
  --scanners vuln,license \
  --format json \
  --output "$TRIVY_JSON" \
  --timeout 40m \
  "$ROOTFS_DIR"

trivy convert \
  --format sarif \
  --output "$TRIVY_SARIF" \
  "$TRIVY_JSON"

python3 "$GITHUB_ACTION_PATH/resources/generate-trivy-html.py" \
  --trivy "$TRIVY_JSON" \
  --sbom "$APPLICATION_SBOM" \
  --output "$TRIVY_HTML" \
  --title "Trivy JAR Vulnerability Report"

echo "Trivy packaged JAR scan completed successfully."
echo "JAR:   $JAR"
echo "JSON:  $TRIVY_JSON"
echo "SARIF: $TRIVY_SARIF"
echo "HTML:  $TRIVY_HTML"