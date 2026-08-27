#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_STEP_SUMMARY:?GITHUB_STEP_SUMMARY is required}"
: "${GITHUB_ENV:?GITHUB_ENV is required}"
: "${GITHUB_SHA:?GITHUB_SHA is required}"
: "${GITHUB_REF_NAME:?GITHUB_REF_NAME is required}"
: "${GITHUB_EVENT_NAME:?GITHUB_EVENT_NAME is required}"
: "${GITHUB_SERVER_URL:?GITHUB_SERVER_URL is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${WORKFLOW_SHA:?WORKFLOW_SHA is required}"
: "${APP_VERSION:?APP_VERSION is required}"

# On pull_request events GITHUB_REF_NAME is typically "<pr-number>/merge".
# Use the actual PR source branch instead.
if [[ "$GITHUB_EVENT_NAME" == "pull_request" && -n "${GITHUB_HEAD_REF:-}" ]]; then
  DEV_BRANCH="${DEV_BRANCH:-$GITHUB_HEAD_REF}"
else
  DEV_BRANCH="${DEV_BRANCH:-$GITHUB_REF_NAME}"
fi

BRANCH_NAME_ESCAPED="${DEV_BRANCH//\//_}"
echo "BRANCH_NAME_ESCAPED=${BRANCH_NAME_ESCAPED}" >> "$GITHUB_ENV"

COMMIT_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/commit/${GITHUB_SHA}"

CICD_REPOSITORY="frankbuttigieg1993-gmail/cicd"
CICD_COMMIT_URL="${GITHUB_SERVER_URL}/${CICD_REPOSITORY}/commit/${WORKFLOW_SHA}"

if [[ "$GITHUB_EVENT_NAME" == "pull_request" && -n "${PR_NUMBER:-}" ]]; then
  DEV_REF_LABEL="Dev Branch"
  DEV_REF_VALUE="${DEV_BRANCH}"
  DEV_REF_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/pull/${PR_NUMBER}/changes"
else
  DEV_REF_LABEL="Dev Branch"
  DEV_REF_VALUE="${DEV_BRANCH}"
  DEV_REF_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/tree/${DEV_BRANCH}"
fi

{
  echo "### 🚀 Build Overview"
  echo
  echo "<table>"
  echo "  <tr><th>Item</th><th>Description</th></tr>"
  echo "  <tr><td>Git Commit</td><td><a href=\"${COMMIT_URL}\"><code>${GITHUB_SHA:0:7}</code></a></td></tr>"
  echo "  <tr><td>${DEV_REF_LABEL}</td><td><a href=\"${DEV_REF_URL}\">${DEV_REF_VALUE}</a></td></tr>"
  echo "  <tr><td>CICD Commit</td><td><a href=\"${CICD_COMMIT_URL}\"><code>${WORKFLOW_SHA:0:7}</code></a></td></tr>"

  if [[ "$GITHUB_EVENT_NAME" != "pull_request" ]]; then
    echo "  <tr><td>Docker Tag</td><td>${APP_VERSION}.${GITHUB_RUN_NUMBER}</td></tr>"
  fi

  echo "</table>"
} >> "$GITHUB_STEP_SUMMARY"