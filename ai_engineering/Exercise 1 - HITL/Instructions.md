# Exercise 1 — AI-Delegated GitHub Engineering (HITL)

## Task

Create a new GitHub Actions composite action named `ai-generated-list-files`.

The composite action must:

1. List all files in a specified directory, including hidden files.
2. Execute after the Build stage completes successfully.
3. Be integrated into the **PR Pipeline** only.

Use the root of the checked-out Java Application repository (`.`) as the target directory.

## Engineering Instructions

Follow the applicable `AGENTS.md` files, the central `github-actions-development` Skill and the authoritative engineering lifecycle documentation discovered during the preceding context-verification exercise.

Apply the documented engineering standards, repository conventions, authorisation requirements, validation procedures, release-management requirements and PR governance rules.

The repository instructions and engineering lifecycle documentation define the standard execution procedure.

## Execution Mode — Human-in-the-Loop

For this execution, follow the standard engineering lifecycle with the additional approval checkpoints defined below.

The checkpoints control execution boundaries only. They do not replace or redefine the standard engineering procedure.

Approval for one checkpoint does not authorise subsequent checkpoints.

### Checkpoint 1 — Planning

Complete the applicable read-only requirements analysis, convention discovery and implementation planning activities.

Present the findings, proposed implementation, affected files, acceptance criteria, dependencies and validation strategy.

**STOP before creating branches or modifying files.**

Report:

**STATUS: AWAITING HUMAN APPROVAL**

### Checkpoint 2 — Implementation

After Checkpoint 1 approval, complete the applicable branch creation, implementation and local validation activities.

Present the implementation summary, changed files, relevant Git diffs and local validation results.

**STOP before committing, pushing or creating pull requests.**

Report:

**STATUS: AWAITING HUMAN APPROVAL**

### Checkpoint 3 — Draft PRs and Integration Validation

After Checkpoint 2 approval, complete the applicable Draft PR creation, release-classification and feature-branch integration-validation activities.

Present the PR references, release classification, execution evidence, validation results and outstanding findings.

**STOP before promoting the CICD PR to Ready for Review.**

Report:

**STATUS: AWAITING HUMAN APPROVAL**

### Checkpoint 4 — CICD PR Promotion

After Checkpoint 3 approval, complete the applicable CICD PR promotion and review-request activities.

Present the PR status, validation evidence and review-request results.

**STOP before any agent-initiated CICD merge or release activity.**

Report:

**STATUS: AWAITING CICD MERGE**

Do not directly merge the CICD PR or bypass repository governance.

Wait for my instruction to resume after the CICD PR has been merged through the authorised GitHub process.

### Checkpoint 5 — CICD Release Verification

When instructed to resume, retrieve the current GitHub state and verify that the CICD merge and applicable release-management activities completed successfully.

Present the published release details, relevant commit SHA and supporting evidence.

**STOP before modifying the Java Application PR to consume the released version.**

Report:

**STATUS: AWAITING HUMAN APPROVAL**

### Checkpoint 6 — Application Release Adoption and Validation

After Checkpoint 5 approval, complete the applicable application release-adoption and final-validation activities.

Present the application changes, execution evidence, validation results and outstanding findings.

**STOP before promoting the Java Application PR to Ready for Review.**

Report:

**STATUS: AWAITING HUMAN APPROVAL**

### Checkpoint 7 — Final Application Promotion

After Checkpoint 6 approval, complete the applicable application PR promotion, review-request and reporting activities.

Present the final engineering report, including completed activities, evidence, outstanding limitations and final status.

Do not merge the Java Application PR.

## Mandatory HITL Behaviour

At every checkpoint:

1. Summarise the completed activities.
2. Present the relevant evidence and outcomes.
3. Identify outstanding risks, blockers or limitations.
4. Report the required execution status.
5. Stop all further agent-initiated operations until explicitly authorised to continue.

Approval at one checkpoint authorises only the activities permitted before the next checkpoint.

Do not introduce additional approval checkpoints unless required by the applicable engineering policies or an unresolved decision.

Do not bypass repository restrictions, required checks, GitHub permissions or release governance.

If execution becomes blocked, report the reason and stop rather than making unsupported assumptions.

Existing GitHub Actions workflows and configured release automation may continue independently while the agent is paused.

## Start Execution

Begin with Checkpoint 1 — Planning.

Do not proceed beyond Checkpoint 1 until I explicitly approve.
