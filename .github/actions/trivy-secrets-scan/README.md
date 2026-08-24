# Detailed Trivy secret HTML report

Changes:
- The composite action passes filesystem, packaged-JAR and image JSON reports into the HTML generator.
- The HTML lists severity, title, rule ID, category, scan stage, target/file and line range.
- Each finding has an expandable investigation section with remediation guidance.
- Actual secret values and matching source-code excerpts are deliberately omitted from HTML.
- The existing artifact upload already uploads `build/reports/trivy-secrets/`, so the detailed HTML is included automatically.
- JSON and SARIF remain available for machine processing and GitHub Code Scanning.

Security recommendation:
Treat raw Trivy JSON/SARIF artifacts as security-sensitive because scanner-native output can contain matched secret material.
