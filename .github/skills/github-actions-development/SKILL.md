---
name: github-actions-development
description: Develop, integrate, troubleshoot, validate and deliver GitHub Actions composite actions and reusable workflows across a central cicd repository and consuming Java application repository. Use for new CI/CD functionality, PR or build pipeline integration, cross-repository changes, failed builds, test remediation and evidence-backed Draft-to-Ready pull requests.
---

# GitHub Actions development — execution runbook

## Human quick reference — execution sequence

This is the **procedure**, not an independent policy. Follow the applicable repository `AGENTS.md` for authorisation, boundaries and completion gates.

| Step | Agent action | Observable result |
|---|---|---|
| 1 | Confirm explicit **PR Pipeline** or **Build Pipeline** selection when integrating with an existing workflow; otherwise stop. | Selected workflow or **BLOCKED - AWAITING USER INPUT** |
| 2 | Understand requirements; inspect comparable composite actions, reusable and caller workflows; discover conventions. | Acceptance criteria and convention summary |
| 3 | Plan the minimal authorised diff and cross-repository execution path. | Proposed files, integration point and validation plan |
| 4 | Create feature branches from `main` in both repositories where justified. | Branch names |
| 5 | Implement minimal changes using established inline-command patterns. | Scoped implementation |
| 6 | Run syntax and local tests, then push and open cross-linked **Draft PRs**. | Test evidence and Draft PR URLs |
| 7 | Run required CI and inspect **workflow, job and step status AND actual logs**. | Run URLs/IDs, SHAs and log excerpts |
| 8 | Verify expected functional output; diagnose, correct and retest failures. | Expected vs observed evidence |
| 9 | Promote both applicable PRs to **Ready for Review** only after required checks and functional verification pass. | Ready states |
| 10 | Request review from `frankbuttigieg-93`, report evidence and hand off without merging. | Reviewer request and final report |

**Human reader:** This table answers what happens and in what order. For rules, read `AGENTS.md`; for precise agent operations, use the phases below.

## Phase 1 — Select, discover and plan

1. **Before any repository/tool operations**, if integration into an existing pipeline is requested, check the current request for explicit **PR Pipeline** (`cicd/.github/workflows/java-build-pr.yml`) or **Build Pipeline** (`cicd/.github/workflows/java-build-all.yml`). Selection authorises minimal task-scoped edits to that workflow. If absent/ambiguous, report **BLOCKED - AWAITING USER INPUT**, ask and stop all execution. If both are explicitly requested, clarify both are intended.
2. Read the applicable `AGENTS.md` files in both repositories. Confirm access to the relevant repositories and Skill; do not assume instructions cross repository boundaries.
3. Translate the request into testable acceptance criteria; identify the event, job order, expected output and target directory or other inputs without inventing requirements.
4. Inspect `cicd/.github/actions/` and at least two comparable actions if available. Inspect relevant reusable workflows, `java_application` caller workflows and Gradle/test conventions. Summarise common naming, `run`/shell, inputs, scripts and dependencies; justify deviations.
5. Trace caller trigger -> reusable workflow -> job dependencies -> composite action -> checkout path. Identify exact files to create/edit in each repository and required tests.
6. If any **additional existing workflow**, including a `java_application` caller, requires editing, report **BLOCKED - AWAITING USER APPROVAL**, describe the file and changes and stop until explicitly authorised. The selected `cicd` workflow needs no second approval. If a second repository needs no meaningful change, request direction rather than creating a dummy PR.
7. Present a concise plan and proposed change list before edits; this is informational, not a new approval gate for already-authorised work.

## Phase 2 — Branch, implement and check locally

1. Confirm clean working trees and current `main` in both repositories; create related task-specific feature branches where meaningful changes are required. Never push directly to `main`.
2. Implement the smallest authorised change. Use `.github/actions/<action-name>/action.yml`, `runs.using: composite`, explicit `shell`, minimal inputs and outputs. Prefer simple inline commands and the Gradle wrapper; for 10 or fewer executable lines, separate scripts require explicit approval. Do not modify unrelated workflows, tests, permissions or security checks.
3. Ensure reusable workflows use `workflow_call`, appropriate `needs`, least-privilege permissions and correct checkout of action code. Ensure PR-only requirements do not leak into push/release paths.
4. Validate YAML, action metadata, trigger/ref resolution, job ordering and cross-repository references. Run appropriate local checks. Confirm the implementation follows observed repository conventions.

## Phase 3 — Publish Draft PRs

1. Push task branches and create Draft PRs targeting `main` in each repository where justified. Cross-link the PRs and document temporary feature-branch refs and planned stable refs.
2. Include acceptance criteria, scoped file changes, local validation and pending CI evidence. Keep PRs Draft until all promotion conditions pass.
3. If required CI does not run for Draft PRs, do not weaken triggers or work around restrictions; report the blocker.

## Phase 4 — CI execution, log inspection and functional verification

1. Identify mandatory checks and the specific workflow, job and step that execute the new functionality. Capture run URL/ID and latest relevant head SHA.
2. Trigger/observe the authorised PR validation path; wait for completion. Record workflow, job **and step** status; distinguish success, failure, skipped, cancelled, pending and missing.
3. **Retrieve and inspect actual logs for the relevant executing step** even when all status indicators are green. Confirm the intended operation ran and check warnings/errors.
4. Compare **observed behaviour** with acceptance criteria. For a directory-listing action, confirm the intended directory, expected filenames and hidden files against a known baseline or suitable test artifact. A successful `ls` exit code or plausible listing alone is insufficient.
5. Capture expected-vs-observed results and relevant log excerpts/artifacts in the Draft PRs. If logs cannot prove correctness, use an additional authorised test; if still insufficient, mark **UNVERIFIED** and leave Draft.
6. On failure, classify the cause, inspect relevant logs, make the smallest authorised correction, push to the existing feature branch and repeat required tests. Do not modify additional existing workflows without file-specific approval.
7. Recheck mandatory checks and functional evidence on the **latest relevant commit SHAs** in both repositories; do not treat skipped or absent required checks as passes.

## Phase 5 — Promotion, review request and final report

1. Confirm both applicable PRs contain final changes, meet acceptance criteria, have passing required checks and verified functional results on the latest relevant commits. Confirm cross-repository refs remain valid for review and eventual merge.
2. Only then mark both Draft PRs **Ready for Review**. If either is incomplete, leave both Draft and report the limitation.
3. Request review from `frankbuttigieg-93` on both. If GitHub refuses the request (including self-review restrictions), report the refusal without claiming approval.
4. Report PR URLs, branches, SHAs, changed files, test commands, workflow run URLs/IDs, job and step conclusions, relevant log excerpts, expected-vs-observed verification, reviewer-request status and outstanding risks.
5. **Never approve or merge PRs, change repository rulesets, bypass required checks or claim success without evidence.**
