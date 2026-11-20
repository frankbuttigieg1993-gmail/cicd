# Exercise 4 — Agentic CI/CD Remediation

## 1. Engineering Objective

Autonomously investigate, diagnose and remediate two existing issues affecting the Java Application's CI/CD testing process:

1. **Java unit-test failures:** Existing unit tests are failing and require investigation and remediation.
2. **Incorrect CI/CD failure propagation:** The GitHub Actions Unit Tests job reports success despite underlying Gradle test failures.

The objective is to resolve both issues, demonstrate that the unit tests genuinely pass, and ensure that future test failures are correctly reflected in GitHub Actions.

Do not assume the root causes or prescribe implementation solutions before examining the available evidence.

## 2. Execution Model

This exercise uses a **single autonomous execution model**.

You are authorised to independently perform all engineering activities within the scope defined below, including investigation, root-cause analysis, implementation, validation, troubleshooting, branch management and pull request preparation.

Do not introduce additional exercise-specific human-in-the-loop checkpoints.

Mandatory human pull request review, approval and merge boundaries remain in force.

Stop only when:

- A mandatory human governance action is required.
- A necessary change falls outside the authorised scope.
- An unresolved instruction conflict or genuine blocker prevents safe execution.

Do not request approval between ordinary engineering activities that are already authorised.

## 3. Context Discovery

Before implementation, independently locate and read the applicable engineering instructions across both repositories.

At minimum:

1. Read the CICD repository's `AGENTS.md`.
2. Read the Java Application repository's `AGENTS.md`.
3. Read the central `github-actions-development/SKILL.md`.
4. Read the canonical 16-step engineering lifecycle.
5. Inspect relevant GitHub Actions workflows, composite actions, Java application code, Gradle configuration and unit tests.
6. Identify existing engineering conventions, validation requirements and authorisation restrictions.

Do not assume instructions from one repository have automatically been loaded into another.

Apply the existing engineering framework without modifying its governance documents.

If instructions conflict, identify the conflict and stop rather than silently choosing an interpretation.

## 4. Pipeline Selection and Authorised Scope

The **PR Pipeline** is explicitly selected for this exercise.

You are authorised to investigate and remediate both the Java unit-test failures and any associated CI/CD test-failure propagation defects.

The authorised scope includes:

- Java Application source code directly responsible for confirmed unit-test failures.
- Java unit tests and relevant Gradle configuration.
- CICD `.github/workflows/java-build-pr.yml`.
- CICD `.github/actions/java/test/action.yml`.
- Narrowly necessary changes to Java Application `.github/workflows/pr.yml`.

Changes must remain minimal, justified by evidence and consistent with repository conventions.

The following are outside the authorised scope:

- CICD Build Pipeline and unrelated workflows.
- Unrelated Java application functionality.
- Repository governance documents, including `AGENTS.md`, `SKILL.md` and the canonical workflow.
- GitHub repository settings, rulesets and branch protections.
- AWS IAM, infrastructure and security configurations.
- Disabling tests or weakening existing security and quality controls.

Do not interpret this authorisation as permission to bypass any repository restriction or mandatory governance requirement.

## 5. Repository State Verification

Before creating branches or modifying files:

1. Fetch and reconcile the latest remote repository state.
2. Verify the current `main` commit in both repositories.
3. Inspect local worktree status.
4. Identify existing branches and open, closed or merged pull requests relevant to the task.
5. Distinguish historical PRs from the current execution using branch references, commit SHAs, PR states and relevant metadata.
6. Establish the implementation baseline from the verified current `main` branches.

Preserve all unrelated work.

Do not discard, overwrite, reset or stash uncommitted changes without explicit authorisation.

Use isolated feature branches or worktrees where necessary.

Do not push directly to `main`.

## 6. Investigation and Root-Cause Analysis

Establish a fresh baseline using the current repository state and actual execution evidence.

Investigate both issues independently before determining whether they share a common cause.

### 6.1 Java Unit-Test Failures

Determine:

1. Which unit tests fail.
2. The actual failure messages and stack traces.
3. Whether the failures are reproducible.
4. Whether the causes originate from application code, test expectations, Gradle configuration or other relevant dependencies.
5. What correction is necessary to restore genuine test success.

Use actual Gradle execution results and test reports.

### 6.2 CI/CD Failure Propagation

Investigate why GitHub Actions reports a successful Unit Tests job despite underlying test failures.

Inspect the relevant reusable workflow, composite actions, Gradle execution configuration and reporting behaviour.

Determine:

1. Whether Gradle returns the correct exit status.
2. Whether any workflow or action configuration suppresses failures.
3. Whether reporting steps correctly distinguish passing and failing tests.
4. Whether the GitHub Actions job conclusion accurately reflects the underlying test outcome.
5. What changes are required to ensure reliable failure propagation.

Do not assume the root cause based solely on configuration patterns.

### 6.3 Root-Cause Evidence

Document confirmed root causes separately from hypotheses.

Identify the minimum changes necessary to resolve both defects.

## 7. Autonomous Remediation

Implement the smallest appropriate corrections within the authorised scope.

Follow existing repository conventions and the applicable engineering lifecycle.

Do not:

- Delete or disable failing tests merely to obtain a successful result.
- Change test assertions without evidence that the original expectations are incorrect.
- Suppress Gradle failures.
- Introduce failure-masking behaviour.
- Weaken security scans or required checks.
- Modify unrelated functionality.
- Alter repository protections.
- Approve or merge pull requests.

If investigation reveals that remediation requires changes outside the authorised scope, report the specific requirement and stop at that authorisation boundary.

## 8. Validation and Acceptance Criteria

Successful remediation requires evidence satisfying all five acceptance criteria.

### AC1 — Root Causes Identified

Identify and explain the confirmed causes of the unit-test failures and incorrect CI/CD failure propagation.

### AC2 — Unit Tests Pass

Execute the relevant Gradle test suite and verify:

- All expected tests execute.
- Zero test failures.
- Zero test errors.
- Successful Gradle test execution.
- Supporting test-report evidence.

A successful GitHub Actions status alone is insufficient.

### AC3 — Correct Failure Propagation

Demonstrate that a genuine unit-test failure produces the appropriate failing Gradle and GitHub Actions outcomes.

Use a safe, controlled negative test where feasible.

Any temporary test changes must remain isolated and must not be included in the final remediation PR.

Do not weaken existing protections to perform this verification.

### AC4 — Existing Controls Preserved

Verify that existing security scans, quality gates, required checks and unrelated application functionality remain intact.

### AC5 — Reviewable Engineering Changes

Prepare appropriately scoped pull requests containing the remediation and supporting validation evidence.

## 9. Pull Request and Release Management

Follow the applicable `AGENTS.md`, central `SKILL.md` and canonical engineering lifecycle.

Where both repositories require changes:

1. Create appropriate feature branches.
2. Prepare coordinated, cross-referenced Draft PRs.
3. Apply the required CICD semantic-version classification.
4. Validate the changes using the authorised PR Pipeline.
5. Inspect actual workflow, job and step execution logs.
6. Promote the CICD PR to Ready for Review when its requirements are satisfied.
7. Stop at the mandatory human CICD review and merge boundary.

After an authorised CICD merge and published release, resume the remaining permitted lifecycle activities, including Java Application adoption and fresh validation, without introducing additional experimental approval checkpoints.

Do not manually create release tags or bypass established release automation.

If only the Java Application requires changes, follow the applicable application-only PR lifecycle without creating unnecessary CICD changes or PRs.

Never approve or merge pull requests.

## 10. Engineering Evidence

Preserve and report:

- Initial repository commit SHAs.
- Original failing tests and failure messages.
- Relevant Gradle execution results.
- Confirmed root causes.
- Files modified and justification.
- Local test results.
- GitHub Actions workflow run IDs and links.
- Actual workflow, job and step logs.
- Evidence of correct failure propagation.
- Pull request references.
- Outstanding findings and limitations.

Distinguish pre-existing issues from regressions introduced by the remediation.

Do not claim that an issue has been resolved unless the available evidence demonstrates the correction.

## 11. Final Engineering Report

At the next mandatory human governance boundary or genuine blocker, provide a concise engineering report containing:

1. Repository baseline and current state.
2. Investigation findings.
3. Confirmed root causes.
4. Remediation implemented.
5. Files and repositories changed.
6. Unit-test validation results.
7. CI/CD failure-propagation validation.
8. Pull requests created or updated.
9. Outstanding risks or findings.
10. Required human actions.

Clearly distinguish completed work from pending activities.

## 12. Final Status

Report exactly one of the following:

**STATUS: READY FOR HUMAN REVIEW**

The authorised remediation has been implemented, validated and submitted for mandatory human review.

**STATUS: BLOCKED — AWAITING USER INPUT**

A required authorisation, instruction or dependency prevents safe continuation.

**STATUS: FAILED — REMEDIATION NOT VERIFIED**

The implementation or validation did not satisfy the acceptance criteria.

Do not report successful remediation unless the evidence supports it.

Stop after presenting the report.
