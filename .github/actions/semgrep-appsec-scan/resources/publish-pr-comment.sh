#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_ACTION_PATH:?GITHUB_ACTION_PATH is required}"
: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GH_REPO:?GH_REPO is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"

COMMENT_FILE="build/reports/semgrep/semgrep-comment.md"

bash "${GITHUB_ACTION_PATH}/resources/build-pr-comment.sh"

if [[ ! -f "$COMMENT_FILE" ]]; then
  echo "::error::Semgrep PR comment file was not generated: ${COMMENT_FILE}"
  exit 1
fi

python3 "${GITHUB_ACTION_PATH}/resources/update-semgrep-pr-comment.py" \
  --repo "$GH_REPO" \
  --pr "$PR_NUMBER" \
  --body-file "$COMMENT_FILE" \
  --token "$GH_TOKEN"