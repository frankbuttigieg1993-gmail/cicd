# Exercise 4 — Read-Only Context Verification Prompt

## Objective

Verify that GitHub Copilot has discovered and correctly understood the applicable engineering instructions, repository state, authorisation boundaries and validation requirements **before** attempting Exercise 4 — Agentic CI/CD Remediation.

This is a **read-only verification task**, not an implementation or remediation task.

## Exercise context

The intended engineering task is to investigate and remediate the existing Java unit-test failures and any associated CI/CD failure-reporting defect, using the existing `cicd` and `java_application` repositories. The agent will later operate autonomously within authorised boundaries, with no additional experimental HITL checkpoints. Mandatory human PR reviews, approvals and merges remain in force.

Do not assume that the previously observed failures still exist or that their causes are known.

## Required discovery

Locate and read, from the actual accessible workspaces:

1. The applicable `AGENTS.md` in **each** repository.
2. The central `github-actions-development/SKILL.md` in the CICD repository.
3. The canonical **16-step CICD engineering, release and application promotion workflow**.
4. Relevant Java/Gradle testing conventions, CI/CD caller and reusable workflow definitions, and other instructions referenced by those documents.

Do not assume that instructions from one repository are automatically loaded or applicable in another. Identify any unavailable documents explicitly.

## Read-only assessment

Using only discovered repository instructions and read-only inspection, report:

1. **Repository responsibilities:** Which repository owns application code/tests, reusable workflows, and caller workflows.
2. **Applicable standards:** Relevant Gradle, testing, GitHub Actions, branch, PR and validation conventions.
3. **Authorisation:** Whether the existing instructions permit investigation and scoped changes to Java tests, application code, Gradle configuration, CICD test-failure propagation, and any cross-repository work. Identify any changes requiring separate approval.
4. **Lifecycle applicability:** How the canonical 16-step workflow applies to a remediation task, and which steps or dependencies may not apply. Do not invent a replacement lifecycle.
5. **Validation expectations:** Requirements for actual Gradle results, GitHub Actions job/step logs, functional evidence, and accurate failure propagation.
6. **Governance boundaries:** Human PR approval/merge requirements; prohibited changes to security checks, rulesets, IAM, release protection, or unrelated files.
7. **Current state:** Read-only observations of relevant branches, open/current/historical PRs, test workflows and available failure evidence; distinguish current observations from historical Exercise 1 findings.
8. **Gaps or conflicts:** Any missing, contradictory, ambiguous or task-inapplicable instructions that would prevent safe autonomous execution.

List **every instruction file accessed** with its repository-relative path and explain the relationship between `AGENTS.md` (WHAT is permitted), `SKILL.md` (HOW to execute), and the canonical workflow (WHEN and in what order).

## Strict restrictions

Do **not** create or switch branches, modify files, run tests or builds, install dependencies, create commits, push, open/update PRs, trigger pipelines, change repository settings, or perform remediation. Read-only commands and queries are allowed only where they do not mutate repository or cloud state.

Do not request exercise-specific approval merely because the future task is autonomous. Report genuine authorisation gaps rather than assuming approval.

## Required output

Provide a concise evidence-based report with the headings **Files Read**, **Context and Scope**, **Authorisation and Governance**, **Lifecycle and Validation**, **Conflicts and Gaps**, and **Decision**.

End with exactly one of:

**STATUS: CONTEXT VERIFIED — READY FOR EXERCISE 4**

**STATUS: BLOCKED — AWAITING USER INPUT**

Only report READY if the required context is accessible, consistent and sufficient for the intended remediation scope. Otherwise explain precisely what is missing or requires authorisation.

**Stop after the report. Do not begin implementation.**
