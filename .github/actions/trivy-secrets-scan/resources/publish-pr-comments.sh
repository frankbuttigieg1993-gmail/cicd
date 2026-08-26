#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"
: "${GH_TOKEN:?GH_TOKEN is required}"
: "${REPOSITORY:?REPOSITORY is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"

COMMENT_FILE="build/reports/trivy-secrets/trivy-secrets-pr-comment.md"

echo "Building Trivy secret PR comment..."

bash "${GITHUB_ACTION_PATH}/resources/build-pr-comment.sh"

if [[ ! -f "$COMMENT_FILE" ]]; then
  echo "::error::Trivy secret PR comment was not generated: ${COMMENT_FILE}"
  exit 1
fi

echo "Publishing Trivy secret PR comment..."

bash "${GITHUB_ACTION_PATH}/resources/upsert-pr-comment.sh"

echo "Trivy secret PR comment published successfully."