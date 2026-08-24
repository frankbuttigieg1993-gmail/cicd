# Trivy secret scanner YAML fix

This revision:
- replaces YAML block-scalar regexes with simpler plain-scalar regexes;
- writes `trivy-secret.yaml` as UTF-8 without BOM and LF line endings;
- adds a validation step before any Trivy scan;
- checks that the file starts with `rules:` and has a regex for every rule;
- explicitly exports `TRIVY_SECRET_CONFIG`;
- keeps the detailed, redacted HTML report from the previous revision.

The validator intentionally does not print secret values.

If Trivy still rejects the file, the validation step will show the exact config path and first 12 non-secret policy lines before scanning.
