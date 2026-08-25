#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GH_REPO:?GH_REPO is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"
: "${RUN_URL:?RUN_URL is required}"
: "${RUN_NUMBER:?RUN_NUMBER is required}"
: "${RUN_ATTEMPT:?RUN_ATTEMPT is required}"

MARKER="<!-- java-pr-pipeline-summary -->"

BODY=$(cat <<EOF
${MARKER}
## Java PR Pipeline

[View the latest PR pipeline run](${RUN_URL})

**Run:** ${RUN_NUMBER}  
**Attempt:** ${RUN_ATTEMPT}
EOF
)

EXISTING_COMMENT_ID="$(
  gh api \
    --paginate \
    "/repos/${GH_REPO}/issues/${PR_NUMBER}/comments?per_page=100" \
    --jq ".[] | select(.body | contains(\"${MARKER}\")) | .id" \
    | head -n 1
)"

if [[ -n "${EXISTING_COMMENT_ID}" ]]; then
  echo "Updating existing PR pipeline comment ${EXISTING_COMMENT_ID}."
  gh api \
    --method PATCH \
    "/repos/${GH_REPO}/issues/comments/${EXISTING_COMMENT_ID}" \
    -f body="${BODY}"
else
  echo "Creating PR pipeline comment."
  gh pr comment "${PR_NUMBER}" \
    --repo "${GH_REPO}" \
    --body "${BODY}"
fi
