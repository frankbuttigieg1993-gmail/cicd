# SpotBugs / FindSecBugs sticky PR summary

The PR comment now behaves like the GitHub Step Summary:

- A summary comment is created for every PR run, regardless of findings.
- The same comment is updated on subsequent PR runs using a hidden marker.
- The comment includes the SpotBugs summary markdown produced by `check-spotbugs-critical.py`.
- The comment includes a direct link to the current GitHub Actions run.
- Comment publishing is `continue-on-error: true`, so a missing PR-comment permission cannot mask the actual SpotBugs policy result.
- The existing enforcement step remains unchanged: Gradle/analysis failure or critical findings still fail the action.
- The helper script remains under `resources/`.

Required caller permissions for the PR comment:
  pull-requests: write
  issues: write


## External resource scripts

Long inline shell/PR-comment logic has been moved into `resources/`:

- `run-spotbugs.sh`
- `write-step-summary.sh`
- `update-pr-comment.sh`
- `enforce-policy.sh`
- existing `check-spotbugs-critical.py`

`action.yml` now invokes these files using `${{ github.action_path }}/resources/...`.
