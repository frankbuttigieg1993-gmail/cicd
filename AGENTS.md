# Agent instructions - cicd repository

## Scope and ownership
This repository (`frankbuttigieg1993-gmail/cicd`) owns reusable GitHub Actions workflows and composite actions. `main` is the integration branch. Create a feature branch from `main`, push changes, and open a PR; never merge a PR.

## Non-negotiable change boundaries
- Treat **all existing workflows and composite actions as read-only reference material** unless the current task explicitly names them as editable.
- In particular, do not edit `.github/workflows/java-build-pr.yml` or `.github/workflows/java-build-all.yml`, their jobs, security scans, dependencies, or permissions.
- For the AI-generated lab, only create or modify `.github/workflows/ai-generated.yml` and `.github/actions/ai-generated/action.yml`, plus documentation/tests explicitly authorised in the task. Do not modify this file or repository security configuration.
- Before editing, list planned file paths. If any required edit falls outside the allowlist, stop and request approval. A passing build does not justify expanding scope.
- Never disable checks, expose secrets, change branch protection, change repository settings, or deploy infrastructure.

## Engineering conventions
- Inspect existing `Java/Build` and `Java/Test` composite actions and reusable workflows for naming and patterns, without changing them.
- Keep composite actions simple: minimal inputs/outputs, inline `run` steps for short commands, `action.yml`, `runs.using: composite`, explicit `shell` for every `run` step.
- Reusable workflows must use `workflow_call`, least-privilege `permissions`, correct cross-repository references, and propagate failures. Do not assume `./.github/actions/...` points to `cicd` after checking out the caller's source.
- Use reviewed immutable SHAs for third-party actions where repository policy requires them; do not invent SHA values.

## Validation and evidence
- Validate YAML, action/workflow structure and references; run available tests and relevant GitHub Actions jobs.
- Investigate and fix failures **only inside the authorised paths**. Never weaken an existing check to obtain a pass.
- Record workflow URL, run ID, job conclusions and evidence that the new action executed. Clearly distinguish successful, failed, skipped and not-run checks.
- If manual `workflow_dispatch` cannot run from a feature branch due to GitHub platform constraints, report the blocker and use an authorised PR-triggered validation path if available; do not alter `main` to work around it.

## Pull requests and completion
- Create a PR targeting `main` when requested. Cross-reference the corresponding `java_application` PR and explain temporary feature-branch dependencies.
- Never merge, bypass reviews, or modify repository rulesets.
- Report COMPLETE only when the requested changes are in scope, required tests actually passed, and both requested PRs exist. Otherwise report PARTIALLY COMPLETE, BLOCKED or FAILED with reasons.
