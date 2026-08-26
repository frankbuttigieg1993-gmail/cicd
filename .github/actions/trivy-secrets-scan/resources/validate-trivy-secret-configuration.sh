#!/usr/bin/env bash
set -euo pipefail

CONFIG="${{ github.action_path }}/resources/trivy-secret.yaml"

if [[ ! -s "$CONFIG" ]]; then
    echo "::error::Trivy secret configuration is missing or empty: $CONFIG"
    exit 1
fi

python3 "${{ github.action_path }}/resources/validate-trivy-secret-config.py" "$CONFIG"

echo "Using Trivy secret configuration: $CONFIG"
sed -n '1,12p' "$CONFIG"