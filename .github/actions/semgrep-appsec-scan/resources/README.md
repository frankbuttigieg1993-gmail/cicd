# Semgrep AppSec exact scan-link composite action

This revision extracts the exact `scan_id` emitted by `semgrep ci --verbose` for the current execution.

Example observed CLI output:
`Initializing scan (..., scan_id=215991800)`

The action captures the Semgrep output with `tee`, extracts that ID, and constructs:
`<semgrep-project-url>/scans/<scan_id>`

The exact scan URL is included in:
- the GitHub Step Summary;
- the sticky PR comment;
- composite action outputs `semgrep-scan-id` and `semgrep-scan-url`.

There is no fallback that labels the project URL as a scan URL.

All substantial helper logic is under `resources/`.

## Step Summary exact scan link

When the current `semgrep ci --verbose` output yields a scan ID, the GitHub Step Summary now renders:

`Exact scan: Semgrep scan <scan_id>`

as a clickable link to:

`<semgrep-project-url>/scans/<scan_id>`

The project URL is never substituted for the exact scan URL.
