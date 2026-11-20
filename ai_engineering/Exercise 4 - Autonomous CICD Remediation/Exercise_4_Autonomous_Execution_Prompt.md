# Exercise 4 — Autonomous CI/CD Remediation Execution Prompt

## Objective

Autonomously investigate, diagnose and remediate the Java unit-test failures and any associated CI/CD test-failure reporting defects across the existing `cicd` and `java_application` repositories.

The engineering objective is **genuinely passing tests and accurate CI/CD failure reporting**, not merely a green workflow status. Do not assume the historical Exercise 1 failure pattern remains current, or prescribe a solution before collecting evidence.

## Execution model

Operate as a **single autonomous engineering execution** without additional exercise-specific HITL checkpoints. Continue through all activities permitted by the applicable repository instructions. Respect mandatory human PR review, approval and merge boundaries, and stop at a genuine blocker or missing authorisation.

The earlier read-only context verification is a prerequisite, not blanket permission to override governance. Re-read applicable instructions if workspace state or scope changes.

## Authorised task scope

Investigate and, **where permitted by repository governance**, implement narrowly necessary changes to:

- Java unit tests and directly related application code.
- Gradle test configuration and execution behaviour.
- Java caller workflows and central CICD reusable workflows responsible for test execution or failure propagation.
- Minimal supporting files directly required to validate the correction.

Do not assume a change is authorised merely because it appears in this list. If an applicable `AGENTS.md` or other authoritative instruction requires additional approval, **stop and report the exact boundary**. Do not edit `AGENTS.md`, `SKILL.md`, the canonical workflow, unrelated workflows, repository settings, rulesets, IAM or release protections as part of this exercise.

## Autonomous investigation

1. Reconcile the current local/remote repository state, current and historical PR identities, and relevant workflow revisions without destructive operations.
2. Establish a **fresh baseline**: identify current failing tests, affected workflow/job/step, exact Gradle output, exit status, and GitHub Actions conclusions. If historical failures are no longer reproducible, report that finding rather than manufacturing failures.
3. Determine whether application test failures and CI/CD failure masking are separate defects; trace the actual command and exit-code propagation.
4. Form evidence-backed root-cause hypotheses and validate them before editing. Distinguish confirmed causes, plausible causes and unknowns.
5. Choose the smallest safe remediation consistent with existing repository conventions and the applicable engineering lifecycle.

## Implementation and verification

- Create appropriately scoped feature branches and preserve unrelated work.
- Correct confirmed root causes rather than deleting tests, weakening assertions, suppressing failures, adding `continue-on-error`, or manipulating job conclusions to appear green.
- Run relevant Gradle tests and inspect detailed results; the acceptance criterion is **zero failures in the relevant suite**, not just a successful wrapper step.
- Verify that the pipeline correctly propagates a genuine test failure to a failing check. Use a **safe, reversible negative test** only if authorised and feasible; isolate it from protected branches and production workflows, and remove temporary changes before the final PR state. If not feasible, document the limitation rather than claiming verification.
- Run fresh PR validation on the corrected revision; inspect actual job/step logs and compare expected versus observed behaviour.
- Preserve existing security scans, permissions, checks and governance controls. Record unrelated pre-existing findings separately.

## Pull requests and release handling

Follow the existing `AGENTS.md`, central `SKILL.md` and canonical workflow where applicable. Determine from the actual changes whether one or both repositories require PRs; do not manufacture a CICD change simply to satisfy a cross-repository pattern.

Before creating PRs, reconcile historical/current branches and PRs using refs, SHAs and metadata. Create Draft PRs and cross-link them when both repositories change. Include root cause, diff scope, tests, actual logs, run links, limitations and outstanding findings. Promote to Ready for Review only when permitted and evidence requirements are met.

If a CICD release is required, follow the existing human merge, semantic-version, immutable-release and application-adoption process. Do not manually create or move tags or bypass the release workflow. Do not approve or merge PRs.

## Acceptance criteria

- **AC1 — Diagnosis:** Explain the current root causes with reproducible evidence.
- **AC2 — Test correctness:** Relevant Gradle unit tests genuinely pass with zero failures.
- **AC3 — Failure propagation:** A real test failure causes the appropriate CI/CD check to fail; provide negative-test evidence or explicitly state why it could not safely be demonstrated.
- **AC4 — Safeguards:** No tests, security scans, checks or protections were weakened; unrelated changes are excluded.
- **AC5 — Reviewability:** All required changes are in appropriately scoped PRs with execution evidence and mandatory human review/merge preserved.

Do not claim all acceptance criteria passed if any are unverified.

## Final report and stopping condition

Provide:

1. Initial repository/PR baseline and instruction sources.
2. Observed failure evidence and confirmed root causes.
3. Remediation implemented, by repository and file.
4. Local Gradle test results and actual test counts.
5. Fresh GitHub Actions run links, job/step results and relevant logs.
6. Evidence of correct failure propagation (or an explicit verification gap).
7. PR links, head SHAs, current Draft/Ready status and release dependencies if applicable.
8. Unrelated known findings, unresolved risks and any authorisation blockers.
9. Exact next mandatory human action.

Finish with exactly one status:

**STATUS: READY FOR HUMAN REVIEW** — Required remediation and validation are complete; PRs await mandatory human review/merge.

**STATUS: BLOCKED — AWAITING USER INPUT** — A genuine governance, access or information blocker prevents safe continuation.

**STATUS: FAILED — REMEDIATION NOT VERIFIED** — The attempted remediation does not satisfy the acceptance criteria.

Stop at the next mandatory human governance boundary. **Do not approve or merge PRs.**
