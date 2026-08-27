#!/usr/bin/env bash
set -euo pipefail

: "${SEMGREP_APP_TOKEN:?SEMGREP_APP_TOKEN is required}"
: "${SCAN_ID:?SCAN_ID is required}"
: "${SEMGREP_BRANCH:?SEMGREP_BRANCH is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

SEMGREP_DEPLOYMENT_ID="108775"
SEMGREP_ORG="frank_buttigieg_1993_personal_org2"
SEMGREP_ORG_URL="https://semgrep.dev/orgs/${SEMGREP_ORG}"

SCAN_DETAILS="$(
  curl --fail --silent --show-error \
    --header "Authorization: Bearer ${SEMGREP_APP_TOKEN}" \
    "https://semgrep.dev/api/v1/deployments/${SEMGREP_DEPLOYMENT_ID}/scan/${SCAN_ID}"
)"

API_SCAN_ID="$(jq -r '.id // empty' <<< "$SCAN_DETAILS")"
if [[ -z "$API_SCAN_ID" ]]; then
  echo "Semgrep scan-details API did not return a scan id."
  exit 1
fi

CODE_FINDINGS="$(jq -r '(.stats.findings_by_product.code // 0) | floor' <<< "$SCAN_DETAILS")"
SUPPLY_CHAIN_FINDINGS="$(jq -r '(.stats.findings_by_product["supply-chain"] // 0) | floor' <<< "$SCAN_DETAILS")"
SECRETS_FINDINGS="$(jq -r '(.stats.findings_by_product.secrets // 0) | floor' <<< "$SCAN_DETAILS")"
TOTAL_FINDINGS="$(jq -r '(.stats.findings // 0) | floor' <<< "$SCAN_DETAILS")"

REPO_NAME="${GITHUB_REPOSITORY##*/}"
BRANCH="${SEMGREP_BRANCH#refs/heads/}"
REPO_ENCODED="$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$REPO_NAME")"
BRANCH_ENCODED="$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$BRANCH")"

CODE_FINDINGS_URL="${SEMGREP_ORG_URL}/findings?repo=${REPO_ENCODED}&branch=${BRANCH_ENCODED}&id=${API_SCAN_ID}"
SUPPLY_CHAIN_FINDINGS_URL="${SEMGREP_ORG_URL}/supply-chain/vulnerabilities?repo=${REPO_ENCODED}&ref=branch/${BRANCH_ENCODED}"

{
  echo "scan-id=${API_SCAN_ID}"
  echo "code-findings=${CODE_FINDINGS}"
  echo "supply-chain-findings=${SUPPLY_CHAIN_FINDINGS}"
  echo "secrets-findings=${SECRETS_FINDINGS}"
  echo "total-findings=${TOTAL_FINDINGS}"
  echo "code-findings-url=${CODE_FINDINGS_URL}"
  echo "supply-chain-findings-url=${SUPPLY_CHAIN_FINDINGS_URL}"
} >> "$GITHUB_OUTPUT"
