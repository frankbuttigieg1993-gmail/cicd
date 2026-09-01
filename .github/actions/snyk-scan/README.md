Snyk Scan (composite)

This composite action installs the Snyk CLI, authenticates using the provided token, runs `snyk test` and `snyk monitor` against the repository (defaulting to `java_application`).

Usage (in a workflow or reusable workflow):

```yaml
- name: Run Snyk scan
  uses: ./.github/actions/snyk-scan
  with:
    snyk-token: ${{ secrets.SNYK_TOKEN }}
    working-directory: java_application
    java-version: '17'
    severity-threshold: 'high'
    continue-on-error: 'false'
```

Notes:
- Provide the Snyk API token via a repository secret named `SNYK_TOKEN` (or another secret and pass it here).
- This composite action installs the `snyk` CLI globally via `npm` — your runner will need Node.js available. If you prefer the official `snyk/actions/setup` action, you can replace the install step.
- The action runs `snyk monitor` but does not fail the step if monitor fails.
