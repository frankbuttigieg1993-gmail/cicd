#!/usr/bin/env bash

set -euo pipefail

: "${TRIVY_VERSION:?TRIVY_VERSION is required}"
: "${RUNNER_TEMP:?RUNNER_TEMP is required}"
: "${GITHUB_PATH:?GITHUB_PATH is required}"

VERSION="${TRIVY_VERSION#v}"
ARCH="$(uname -m)"

case "$ARCH" in
  x86_64|amd64)
    TRIVY_ARCH="64bit"
    ;;
  aarch64|arm64)
    TRIVY_ARCH="ARM64"
    ;;
  *)
    echo "::error::Unsupported runner architecture: ${ARCH}"
    exit 1
    ;;
esac

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

DOWNLOAD_URL="https://github.com/aquasecurity/trivy/releases/download/v${VERSION}/trivy_${VERSION}_Linux-${TRIVY_ARCH}.tar.gz"
INSTALL_DIR="${RUNNER_TEMP}/trivy-bin"
ARCHIVE="${TMP_DIR}/trivy.tar.gz"

echo "Installing Trivy ${VERSION}"
echo "Architecture: ${ARCH}"
echo "Trivy architecture: ${TRIVY_ARCH}"

curl \
  --fail \
  --silent \
  --show-error \
  --location \
  "$DOWNLOAD_URL" \
  --output "$ARCHIVE"

tar \
  -xzf "$ARCHIVE" \
  -C "$TMP_DIR" \
  trivy

mkdir -p "$INSTALL_DIR"

install \
  -m 0755 \
  "${TMP_DIR}/trivy" \
  "${INSTALL_DIR}/trivy"

echo "$INSTALL_DIR" >> "$GITHUB_PATH"

echo
echo "Trivy installed successfully:"
"${INSTALL_DIR}/trivy" --version