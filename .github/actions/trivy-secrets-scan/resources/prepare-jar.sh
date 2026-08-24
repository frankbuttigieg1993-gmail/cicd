#!/usr/bin/env bash
set -euo pipefail

JAR=$(find build/libs -maxdepth 1 -type f -name '*.jar' | head -n 1 || true)
if [[ -z "$JAR" ]]; then
  echo "available=false" >> "$GITHUB_OUTPUT"
  echo "No packaged JAR found under build/libs."
  exit 0
fi

rm -rf build/trivy-secret-jar-rootfs
mkdir -p build/trivy-secret-jar-rootfs
(
  cd build/trivy-secret-jar-rootfs
  jar xf "../libs/$(basename "$JAR")"
)
echo "available=true" >> "$GITHUB_OUTPUT"
