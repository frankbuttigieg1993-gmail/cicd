#!/usr/bin/env bash
set -euo pipefail

FS_ERROR="${FS_ERROR:-0}"
JAR_ERROR="${JAR_ERROR:-0}"
IMAGE_ERROR="${IMAGE_ERROR:-0}"

if (( TOTAL_COUNT > 0 )); then
  STATUS="BLOCKED"
  MESSAGE="One or more potential secrets were detected by Trivy. Investigate and rotate any genuine credentials before merging."
elif [[ "$FS_ERROR" == "1" || "$JAR_ERROR" == "1" || "$IMAGE_ERROR" == "1" ]]; then
  STATUS="SCAN ERROR"
  MESSAGE="One or more enabled Trivy secret scans failed. Do not treat the repository as clean until the scan error is resolved."
else
  STATUS="PASSED"
  MESSAGE="No secrets were detected by the enabled Trivy secret scans."
fi

cat > build/reports/trivy-secrets/trivy-secrets-comment.md <<EOF2
<!-- trivy-secrets-security-report -->

## Trivy Secret Security Report

| Scan stage | Findings | Policy |
|---|---:|---|
| Source filesystem | ${FS_COUNT} | **BLOCK** if findings are detected |
| Packaged JAR | ${JAR_COUNT} | **BLOCK** if findings are detected |
| Container image | ${IMAGE_COUNT} | **BLOCK** if findings are detected |
| **Total** | **${TOTAL_COUNT}** | |

### Secrets Gate: ${STATUS}

${MESSAGE}

No secret values are included in this comment. Detailed findings are available in GitHub Code Scanning and the Trivy secret report artifact.

_This comment is automatically updated on subsequent scans._
EOF2
