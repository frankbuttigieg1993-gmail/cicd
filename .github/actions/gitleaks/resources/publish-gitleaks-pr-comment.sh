#!/usr/bin/env bash

set -euo pipefail

: "${EXIT_CODE:?EXIT_CODE is required}"
: "${FINDINGS:?FINDINGS is required}"
: "${GH_TOKEN:?GH_TOKEN is required}"
: "${REPOSITORY:?REPOSITORY is required}"
: "${PR_NUMBER:?PR_NUMBER is required}"

REPORT_DIR="build/reports/gitleaks"
COMMENT_FILE="${REPORT_DIR}/gitleaks-comment.md"
COMMENT_MARKER="<!-- gitleaks-security-report -->"

mkdir -p "$REPORT_DIR"

###############################################################################
# Determine security gate status
###############################################################################

if [[ "$EXIT_CODE" == "1" || "$FINDINGS" -gt 0 ]]; then
  STATUS="BLOCKED"
  MESSAGE="One or more potential secrets were detected in the Git repository history. Investigate and rotate any real credentials before merging."

elif [[ "$EXIT_CODE" != "0" ]]; then
  STATUS="SCAN ERROR"
  MESSAGE="Gitleaks encountered an execution error. The scan must be investigated before treating the repository as clean."

else
  STATUS="PASSED"
  MESSAGE="No secrets were detected by Gitleaks in the scanned Git history."
fi

###############################################################################
# Build PR comment
###############################################################################

echo "Building Gitleaks PR comment..."

cat > "$COMMENT_FILE" <<EOF
${COMMENT_MARKER}

## Gitleaks Secret Security Report

**Scope:** Git repository history

| Control | Findings | Policy |
|---|---:|---|
| Gitleaks | ${FINDINGS} | **BLOCK** if findings are detected |

### Security Gate: ${STATUS}

${MESSAGE}

No secret values are included in this comment. Detailed results are available in GitHub Code Scanning and the Gitleaks report artifact.

_This comment is automatically updated on subsequent scans._
EOF

###############################################################################
# Locate existing sticky comment
###############################################################################

echo "Looking for an existing Gitleaks PR comment..."

COMMENT_ID="$(
  {
    gh api \
      --paginate \
      "/repos/${REPOSITORY}/issues/${PR_NUMBER}/comments?per_page=100" \
      --jq ".[] | select(.body | contains(\"${COMMENT_MARKER}\")) | .id" \
      | head -n 1
  } || true
)"

###############################################################################
# Create or update sticky PR comment
###############################################################################

if [[ -n "$COMMENT_ID" ]]; then

  echo "Updating existing Gitleaks PR comment ${COMMENT_ID}..."

  gh api \
    --method PATCH \
    "/repos/${REPOSITORY}/issues/comments/${COMMENT_ID}" \
    --raw-field body="$(cat "$COMMENT_FILE")"

else

  echo "Creating Gitleaks PR comment..."

  gh api \
    --method POST \
    "/repos/${REPOSITORY}/issues/${PR_NUMBER}/comments" \
    --raw-field body="$(cat "$COMMENT_FILE")"

fi

###############################################################################
# Complete
###############################################################################

echo "Gitleaks PR comment published successfully."