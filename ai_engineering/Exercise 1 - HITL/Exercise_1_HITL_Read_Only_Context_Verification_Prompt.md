# Exercise 1 — HITL Context and Governance Verification

> **Purpose:** Historical reconstruction of the read-only context-verification prompt used before the supervised Exercise 1. This is formatted to match the later No-HITL verification document; it is **not claimed to be a verbatim copy** of the original prompt.
>
> **Execution:** Submit before the HITL engineering prompt. This step does **not** authorise implementation.

---

## Prompt for GitHub Copilot

Before beginning any implementation, verify that you can access and read the applicable engineering instructions across the CICD and Java Application repositories.

Locate and read:

- The CICD repository's `AGENTS.md`.
- The Java Application repository's `AGENTS.md`.
- The shared `github-actions-development/SKILL.md`.
- The canonical engineering, release and application-promotion workflow, where available in the workspace.
- Supporting documentation needed to interpret the applicable engineering requirements.

Do not assume that one repository automatically inherits instructions from another.

### Verification Requirements

Using the actual files you can access, summarise:

1. **Repository Responsibilities:** Which repository owns reusable workflows and composite actions, and which owns Java code, tests and caller workflows.
2. **Engineering Standards:** Existing implementation conventions, minimal-change expectations and security requirements.
3. **Authorisation:** Pipeline selection requirements, permitted changes and restrictions.
4. **Engineering Lifecycle:** The standard cross-repository branch, Draft PR, validation, CICD promotion, release, application adoption and review sequence.
5. **Validation and Evidence:** Requirements to inspect actual workflow, job and step execution rather than relying only on green status indicators.
6. **Release Governance:** Semantic-release labels, merged-commit tags, immutable references and application revalidation.
7. **Human Governance:** Which activities require explicit approval and which activities must not be performed by the agent.
8. **Conflicts or Missing Context:** Any inconsistent, ambiguous or inaccessible instructions that could prevent compliant execution.

### Required Output

Identify the files accessed and explain how they relate. Report the applicable engineering boundaries and any blockers. Do not infer missing policies from prior conversations.

### Execution Restrictions

**This is a read-only verification task.** Do not create branches, modify files, execute implementation commands, create or update PRs, trigger pipelines, merge changes or alter repository settings.

### Final Status

If the required context is available and consistent, report:

**STATUS: CONTEXT VERIFIED — READY FOR EXERCISE 1**

Otherwise, report:

**STATUS: BLOCKED — AWAITING USER INPUT**

Stop after providing your findings. Wait for the separate HITL engineering objective.

---

## Historical note

This reconstruction reflects the context-verification phase discussed before the HITL exercise. Some later governance concepts—particularly the refined historical-PR reconciliation and explicit framework-maintenance separation—were developed **after** the original supervised execution and are deliberately not presented here as original requirements.
