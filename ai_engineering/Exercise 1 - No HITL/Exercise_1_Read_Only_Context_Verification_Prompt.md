# Exercise 1 — Final Context and Governance Verification

> **Purpose:** Read-only verification of GitHub Copilot's understanding of the engineering framework before starting Exercise 1 — No HITL.
>
> **Execution:** Submit the prompt below in a new GitHub Copilot Agent session. This prompt does **not** authorise implementation.

---

## Prompt for GitHub Copilot

Before beginning any engineering implementation, independently locate and read the latest applicable engineering instructions across the CICD and Java Application repositories.

Include:

- Repository-specific `AGENTS.md` files.
- The central `github-actions-development/SKILL.md`.
- The canonical 16-step engineering workflow.
- Any supporting engineering documentation necessary to understand the framework.

Do not assume instructions from one repository are automatically available in another.

### Verification Requirements

Using only the instructions discovered in these files, explain your understanding of:

1. **Repository Responsibilities:** The responsibilities and ownership boundaries of the CICD and Java Application repositories.

2. **Engineering Governance:** Applicable engineering standards, authorisation requirements, change restrictions and mandatory controls.

3. **Execution Procedures:** How the central Skill governs engineering implementation, cross-repository coordination, validation and troubleshooting.

4. **Engineering Lifecycle:** The standard end-to-end lifecycle, including development, Draft PRs, semantic-version classification, CICD release, application adoption and final review.

5. **Context Verification and Pipeline Authorisation:** The distinction between preliminary read-only instruction verification and engineering execution requiring explicit pipeline selection.

6. **Operational Engineering vs Framework Maintenance:** The responsibilities and boundaries governing modifications to application code, composite actions, reusable workflows and engineering framework documentation.

7. **Observations and Improvement Handling:** How ambiguities, contradictions, missing instructions and potential framework improvements must be reported and handled.

8. **Historical PR Reconciliation:** How current branches and PRs are distinguished from historical executions.

9. **Historical PR Reconciliation Details:** Explain how current branches and pull requests are distinguished from historical executions, including the use of repository identity, branch references, commit SHAs, PR states and metadata. Explain how previously closed or merged PRs should be handled when branch names are reused.

10. **Validation and Evidence Requirements:** Explain how engineering changes must be validated using actual workflow, job and step execution logs, acceptance criteria, relevant edge cases and expected-versus-observed results.

11. **Release Management and Application Adoption:** Explain the semantic-versioning strategy, release classification requirements, immutable release protections, CICD-first merge sequence and subsequent application adoption process.

12. **Human Governance Boundaries:** Identify which activities Copilot may perform independently, which require human authorisation, and which operations Copilot must never perform.

### Instruction Consistency

Identify any conflicting, ambiguous, outdated or missing instructions.

Distinguish genuine governance contradictions from differences in the responsibilities of `AGENTS.md`, `SKILL.md` and the canonical workflow.

If any issues are identified, report:

- The affected file and relevant instruction.
- The nature of the issue.
- Its potential impact on engineering execution.
- Whether it prevents compliant execution.
- A recommended resolution.

Do not modify the engineering framework to resolve any findings.

### Required Output

Provide a concise, structured report containing:

1. The files accessed and their respective purposes.
2. Your findings against the 12 verification requirements.
3. Any instruction inconsistencies or missing information.
4. Confirmation of the separation between operational engineering execution and engineering framework maintenance.
5. Confirmation of the applicable authorisation and governance boundaries.
6. Your overall readiness assessment.

### Execution Restrictions

**This is strictly a read-only context-verification task.**

Do not:

- Modify any repository files.
- Create or modify branches.
- Create commits or push changes.
- Create, update or merge pull requests.
- Execute implementation or validation commands.
- Trigger GitHub Actions workflows.
- Modify GitHub settings, rulesets, permissions or releases.
- Begin implementing Exercise 1.

If you identify potential improvements to the engineering instructions, report them for separate review. Do not implement them.

### Final Status

If the required engineering context is available, consistent and sufficient for execution, report:

**STATUS: CONTEXT VERIFIED — READY FOR EXERCISE 1**

Otherwise, report:

**STATUS: BLOCKED — AWAITING USER INPUT**

Stop after presenting your findings and wait for the engineering objective.
