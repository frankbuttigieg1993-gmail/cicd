# Trivy dependency-aware HTML report

This bundle modifies only the **Trivy Dependency and License Scan** HTML path. JAR, Docker image, configuration and WebGoat reports continue using the existing Trivy v0.72.0 Go template.

## Files

- `action.yml` — updated composite action.
- `resources/generate-trivy-html.py` — joins Trivy JSON with the CycloneDX dependency graph and renders grouped HTML.
- `resources/trivy-v0.72.0-html-template.tpl` — your existing template, retained for the other Trivy reports.

## Report grouping

The source-code vulnerability HTML is grouped as:

`Maven group -> package/artifact -> vulnerabilities`

Each package receives one of these labels:

- **Direct** — its CycloneDX `bom-ref` is directly in the root application's `dependsOn` list.
- **Transitive** — it is reachable below a direct dependency.
- **Unknown** — the Trivy package could not be mapped unambiguously to the CycloneDX graph.

## Expected action repository layout

```text
<action repository>/
  action.yml
  resources/
    generate-trivy-html.py
    trivy-v0.72.0-html-template.tpl
```

The action runs `./gradlew cyclonedxBom`, searches below `build/` for a valid CycloneDX JSON file, and then creates:

`build/reports/trivy/trivy-srccode-report.html`

The original Trivy JSON and SARIF outputs are preserved.

## Important

The classification depends on the CycloneDX SBOM containing a `dependencies` graph and a root `metadata.component.bom-ref`. If your CycloneDX Gradle configuration omits dependency graph information, packages will show as `Unknown` rather than being guessed.
