#!/usr/bin/env bash

set -euo pipefail

: "${GITHUB_STEP_SUMMARY:?GITHUB_STEP_SUMMARY is required}"
: "${GITHUB_SHA:?GITHUB_SHA is required}"
: "${GITHUB_REF_NAME:?GITHUB_REF_NAME is required}"
: "${GITHUB_SERVER_URL:?GITHUB_SERVER_URL is required}"
: "${GITHUB_EVENT_NAME:?GITHUB_EVENT_NAME is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${WORKFLOW_SHA:?WORKFLOW_SHA is required}"
: "${GITHUB_RUN_NUMBER:?GITHUB_RUN_NUMBER is required}"
: "${APP_VERSION:?APP_VERSION is required}"

###############################################################################
# Configure branch name
###############################################################################

BRANCH_NAME_ESCAPED="${GITHUB_REF_NAME//\//_}"

echo "BRANCH_NAME_ESCAPED=${BRANCH_NAME_ESCAPED}" >> "$GITHUB_ENV"

###############################################################################
# Build URLs
###############################################################################

COMMIT_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/commit/${GITHUB_SHA}"

###############################################################################
# Generate build summary
###############################################################################

{
  echo "### 🚀 Build Overview"
  echo
  echo "<table>"
  echo "  <tr>"
  echo "    <th>Item</th>"
  echo "    <th>Description</th>"
  echo "  </tr>"

  echo "  <tr>"
  echo "    <td>Git Commit</td>"
  echo "    <td><a href=\"${COMMIT_URL}\"><code>${GITHUB_SHA:0:7}</code></a></td>"
  echo "  </tr>"

  echo "  <tr>"
  echo "    <td>Dev Branch</td>"
  echo "    <td>${GITHUB_REF_NAME}</td>"
  echo "  </tr>"

  echo "  <tr>"
  echo "    <td>CICD Commit</td>"
  echo "    <td>${WORKFLOW_SHA}</td>"
  echo "  </tr>"

  # Docker is only part of the build for non-PR executions.
  if [[ "$GITHUB_EVENT_NAME" != "pull_request" ]]; then
    echo "  <tr>"
    echo "    <td>Docker</td>"
    echo "    <td>${APP_VERSION}.${GITHUB_RUN_NUMBER}</td>"
    echo "  </tr>"
  fi

  echo "</table>"
} >> "$GITHUB_STEP_SUMMARY"