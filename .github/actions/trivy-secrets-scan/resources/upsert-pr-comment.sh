#!/usr/bin/env bash
set -euo pipefail

COMMENT_ID="$({
  gh api --paginate \
    "/repos/${REPOSITORY}/issues/${PR_NUMBER}/comments?per_page=100" \
    --jq '.[] | select(.body | contains("<!-- trivy-secrets-security-report -->")) | .id' \
    | head -n 1
} || true)"

if [[ -n "$COMMENT_ID" ]]; then
  gh api --method PATCH \
    "/repos/${REPOSITORY}/issues/comments/${COMMENT_ID}" \
    --raw-field body="$(cat build/reports/trivy-secrets/trivy-secrets-comment.md)"
else
  gh api --method POST \
    "/repos/${REPOSITORY}/issues/${PR_NUMBER}/comments" \
    --raw-field body="$(cat build/reports/trivy-secrets/trivy-secrets-comment.md)"
fi
