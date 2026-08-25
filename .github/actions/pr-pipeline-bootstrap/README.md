# PR Pipeline Summary composite action

Place this directory in the shared CICD repository at:

`.github/actions/pr-pipeline-summary/`

The action creates one persistent PR comment containing a link to the current workflow run.
Subsequent pipeline runs locate the comment using a hidden marker and PATCH the existing comment
instead of creating duplicates.

The calling job remains responsible for `needs:` because job dependencies cannot be declared
inside a composite action. The caller should use `if: always()` so the summary still runs after
failed pipeline jobs.

Required caller permissions:
- contents: read
- pull-requests: write
- issues: write
