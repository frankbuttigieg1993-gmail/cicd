#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GH_REPO:?GH_REPO is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"

SUMMARY_FILE="${SUMMARY_FILE:-build/reports/secrets-scan/secrets-scan-summary.md}"
MARKER="<!-- secrets-scan-report -->"

if [[ ! -f "$SUMMARY_FILE" ]]; then
  echo "::warning::Secrets Scan summary file does not exist: ${SUMMARY_FILE}"
  exit 0
fi

COMMENT_ID="$(
  gh api --paginate "repos/${GH_REPO}/issues/${PR_NUMBER}/comments" \
    --jq ".[] | select(.body | contains(\"${MARKER}\")) | .id" |
  head -n 1
)"

BODY="$(cat "$SUMMARY_FILE")"

if [[ -n "$COMMENT_ID" ]]; then
  echo "Updating existing Secrets Scan PR comment: ${COMMENT_ID}"
  gh api --method PATCH "repos/${GH_REPO}/issues/comments/${COMMENT_ID}" \
    --raw-field body="$BODY" >/dev/null
else
  echo "Creating Secrets Scan PR comment."
  gh api --method POST "repos/${GH_REPO}/issues/${PR_NUMBER}/comments" \
    --raw-field body="$BODY" >/dev/null
fi
