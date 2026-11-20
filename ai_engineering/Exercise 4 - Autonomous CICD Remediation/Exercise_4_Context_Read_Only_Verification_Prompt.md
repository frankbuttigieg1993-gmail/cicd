# Exercise 4 — Read-Only Context Verification Prompt (Updated)

## Objective

Before any implementation, verify that GitHub Copilot has discovered and correctly understood the applicable engineering instructions, repository state, authorised scope, validation requirements and mandatory governance boundaries for **Exercise 4 — Agentic CI/CD Remediation**.

**This is a read-only context-verification task. Do not begin remediation.**

## Engineering objective and execution model

The subsequent execution will investigate and remediate **both**:

1. Existing Java Application unit-test failures.
2. Incorrect CI/CD failure propagation, where a Unit Tests job may report success despite underlying Gradle test failures.

The operator confirms that unit-test failures are present on the current Java Application branch. Treat that as the operator's reported starting condition, **not as independently verified test evidence**. Establish the actual failures and their root causes during the later execution; do not assume historical Exercise 1 logs prove current behaviour.

The exercise uses **one autonomous engineering execution** with **no additional experimental HITL checkpoints**. Mandatory human pull-request review, approval and merge boundaries remain in force.

## Explicit pipeline selection and task authorisation

The **PR Pipeline** is selected. The following changes are authorised **only where justified by confirmed root-cause evidence and consistent with repository governance**:

- Java Application source code directly responsible for failing unit tests.
- Java unit tests and relevant Gradle configuration.
- CICD `.github/workflows/java-build-pr.yml`.
- CICD `.github/actions/java/test/action.yml`.
- Narrowly necessary Java Application `.github/workflows/pr.yml` changes.

The **Build Pipeline is not selected**. Unrelated workflows, application functionality, governance files (`AGENTS.md`, `SKILL.md`, canonical workflow), repository settings, rulesets, IAM, infrastructure and security controls are not authorised for modification.

The execution prompt does not override stricter repository-specific restrictions. Identify any remaining authorisation conflicts explicitly.

## Required discovery

Locate and read the applicable instructions **from both actual repository workspaces**:

1. CICD `AGENTS.md`.
2. Java Application `AGENTS.md`.
3. CICD `.github/skills/github-actions-development/SKILL.md`.
4. The actual canonical 16-step engineering lifecycle file, using its discovered path rather than assuming a filename.
5. Relevant PR reusable workflow, Java caller workflow, test composite action, Gradle configuration and test conventions.

Do not assume instructions from one repository are automatically loaded into another. Report unavailable or conflicting documents.

## Read-only assessment

Report the following, supported by file paths and read-only observations:

1. **Repository ownership:** Which repository owns reusable workflows/actions and which owns Java source, tests, Gradle and caller workflows.
2. **Engineering standards:** Applicable implementation, testing, PR, release and evidence conventions.
3. **Authorisation:** Confirm the selected PR Pipeline and assess whether the explicitly authorised remediation scope is consistent with both repositories' instructions. Identify any specific residual restrictions.
4. **Repository state:** Read-only verification of local and remote `main` references, active branches, dirty worktrees, current/historical PRs and the operator's reported Java `main` update. Do not assume a push succeeded without checking. Preserve unrelated changes.
5. **Failure evidence:** Identify available current test reports and GitHub Actions logs. Distinguish operator-reported failures, historical findings and independently observed current evidence. **Do not run tests or trigger workflows during this phase.** Lack of freshly executed test evidence is not, by itself, a context-authorisation blocker; it is a baseline task for the execution phase.
6. **Lifecycle applicability:** Explain how the existing canonical 16-step workflow applies, including any conditional steps if only one repository needs modification. Do not invent a replacement lifecycle.
7. **Validation requirements:** State how later execution must establish genuine passing tests, correct Gradle/job failure propagation, controlled negative-test evidence where feasible, and preservation of existing controls.
8. **Governance boundaries:** Identify human review/merge requirements and prohibited actions.
9. **Gaps or conflicts:** Identify only genuine missing instructions, scope conflicts or unsafe repository conditions that prevent starting authorised execution.

List the instruction files accessed by repository-relative path. Explain the three-layer relationship: **`AGENTS.md` = WHAT is permitted; `SKILL.md` = HOW to execute; canonical workflow = WHEN and in WHAT ORDER**.

## Strict read-only restrictions

Do **not** create or switch branches, modify files, run Gradle/tests/builds, install dependencies, create commits, push, open or update PRs, trigger pipelines, alter repository settings or perform remediation. Use only non-mutating inspection commands and queries.

Do not infer that any specific Gradle flag, action setting or test implementation is the root cause until the execution phase establishes evidence.

## Required output

Provide a concise report under these headings:

- **Files Read**
- **Context and Scope**
- **Current Repository State**
- **Authorisation and Governance**
- **Lifecycle and Validation**
- **Conflicts and Gaps**
- **Decision**

End with exactly one of:

**STATUS: CONTEXT VERIFIED — READY FOR EXERCISE 4**

**STATUS: BLOCKED — AWAITING USER INPUT**

Report **READY** when the instructions are accessible and consistent, the stated PR Pipeline authorisation covers the intended investigation, and repository state permits a safe subsequent execution. Do **not** require the root cause or freshly reproduced failures to be known before declaring context ready.

Report **BLOCKED** only for a genuine unresolved authorisation conflict, missing governing instruction or repository-state condition that prevents safe execution. State precisely what is needed.

**Stop after the report. Do not begin implementation.**
