# AI Engineering Framework — Consolidated Architecture and Handover Guide

> **Purpose:** Explain the repository-driven context-engineering framework developed during Exercise 1, with detailed treatment of `AGENTS.md`, `SKILL.md`, and the canonical 16-step workflow.
>
> **Document status:** Explanatory reference, **not** an additional agent instruction or source of authorisation. For operational decisions, consult the latest authoritative files in the repositories.

## 1. Executive summary

This framework uses version-controlled instructions to guide AI-assisted software engineering across a central CICD repository and one or more application repositories. It separates **governance**, **execution procedure**, and **lifecycle orchestration** so an agent can work consistently without requiring every engineering prompt to restate the entire delivery process.

The design was exercised with a new file-listing composite action integrated into the Java application's PR pipeline. The supervised **Exercise 1** reached all seven human-in-the-loop (HITL) checkpoints and promoted the Java application PR to Ready for Review. It did **not** establish that the Java PR was merged or that fully autonomous operation has been validated.

**Operating principle:** `AGENTS.md` defines **what is allowed and required**; `SKILL.md` defines **how to do it**; the canonical workflow defines **when and in what order**.

Exercise 1 developed a reusable approach for delegating GitHub Actions engineering to GitHub Copilot without repeating an entire engineering process in each task prompt. The operator states the required outcome; repository instructions govern permissible work, a shared Skill explains how to execute it, and a canonical workflow determines sequencing and handoffs. Existing code supplies implementation conventions, while GitHub Actions logs and repository metadata provide evidence of what actually happened.

The three distinct instruction layers are:

| Layer | Authoritative artifact | Core question | Role |
|---|---|---|---|
| **Governance and Policy** | CICD and application `AGENTS.md` | **WHAT is permitted, required or prohibited?** | Engineering policy, scope, standards, guardrails and human authority |
| **Reusable Execution Procedure** | Central `github-actions-development/SKILL.md` | **HOW should authorised work be performed and verified?** | Reusable technical runbook, troubleshooting and evidence-gathering procedures |
| **Orchestration and Sequence of Activities** | Canonical 16-step workflow | **WHEN and in WHAT ORDER should work occur?** | Cross-repository dependencies, lifecycle phases, promotion gates and handoffs |

**Recommendation:** Keep the three *authoritative* files separate. Consolidate the three uploaded *explanatory* documents into this single guide. The explanation may discuss all three layers together, but merging their actual operating instructions would blur authority and increase maintenance risk.

## 2. Repository architecture and sources of context

| Source | Responsibility | Examples |
|---|---|---|
| `cicd` repository | Owns shared reusable workflows, composite actions, release automation and the central engineering Skill | `.github/workflows/java-build-pr.yml`, `.github/actions/`, `.github/workflows/promotion-auto-tag.yml` |
| `java_application` repository | Owns application source, Gradle, tests, caller workflows and its local governance | `.github/workflows/pr.yml`, application `AGENTS.md` |
| User prompt | Defines the task, target pipeline, acceptance criteria and any exercise-specific execution mode | List the Java root, including hidden entries, after Build |
| Existing code | Supplies established implementation conventions | Composite-action metadata, explicit shell, Gradle wrapper |
| GitHub and terminal tool output | Supplies current state and validation evidence | Branch SHAs, PR states, job logs, releases and rulesets |
| Copilot agent runtime | Coordinates tool calls and working context | Discovery, inspection, execution, evidence gathering |

The CICD repository publishes **one semantic version for the repository as a whole**. Application repositories independently adopt published versions through their own reviewed caller changes. The application does not automatically inherit the CICD repository's `AGENTS.md` or Skill merely by calling its workflows: the agent must locate the applicable instructions in the actual workspace.

### Authoritative paths

- CICD governance: `cicd/AGENTS.md`
- Application governance: `java_application/AGENTS.md`
- Central runbook: `cicd/.github/skills/github-actions-development/SKILL.md`
- Canonical lifecycle: `cicd/.github/Canoncial Engineering Lifecycle.md`

These are paths described by the supplied explanatory documents; check the current repository before treating a path or rule as operationally current.

## 3. The three-layer instruction architecture

### Layer 1 — `AGENTS.md`: governance and policy

**Question answered: What is permitted and required?**

The CICD and application `AGENTS.md` files establish repository responsibilities, mandatory pipeline selection, scope of authorisation, protected files, minimal-change expectations, PR promotion criteria, review boundaries, evidence requirements, release governance, and handling of known findings.

Examples:

- Explicitly select **PR Pipeline** or **Build Pipeline** before work integrating into an existing pipeline. PR Pipeline selection authorises the selected CICD PR workflow and only narrowly necessary Java PR caller edits.
- Preserve unrelated code, workflows, checks, permissions, and uncommitted work.
- Require evidence from actual workflow, job, step, and log execution—not only green checkmarks.
- Do not directly merge PRs, bypass required checks, or alter GitHub settings without specific authorisation.
- Historical merged/closed PRs are evidence, not automatic blockers to a new execution.

**Precedence:** Repository-specific `AGENTS.md` governs its own change boundaries. Contradictions with the Skill or lifecycle must be reported rather than silently resolved.

### Layer 2 — `SKILL.md`: reusable execution procedure

**Question answered: How should the work be performed?**

The central `github-actions-development` Skill provides the technical runbook for discovering conventions, creating and validating actions/workflows, safely managing branches, coordinating Draft PRs, classifying release labels, inspecting logs, handling failures, and performing post-release application adoption.

It includes the **Historical PR and Feature-Branch Reconciliation** procedure: compare local and remote refs/SHAs, identify PRs using repository, head/base refs, current SHA, state, commits, and metadata, distinguish current work from historical records, and avoid destructive fallback actions. Plausibly transient PR-creation failures may receive at most two bounded retries after read-only investigation.

This shared Skill is intended to be reused across multiple application repositories; a duplicate Java-specific Skill is not required.

### Layer 3 — canonical workflow: lifecycle orchestration

**Question answered: When and in what order?**

The authoritative sequence is:

`.github/Canoncial Engineering Lifecycle.md`

It defines the **16-step** delivery lifecycle, CICD-first merge/release dependencies, application adoption and revalidation, human review gates, and reporting. It is a sequence document, not a replacement for repository policy or the detailed Skill.

### How the layers cooperate

| Situation | `AGENTS.md` | `SKILL.md` | Canonical workflow |
|---|---|---|---|
| Historical PR shares a branch name | Says a matching name is not proof of current execution | Compares refs, SHAs, PR metadata; safely handles failures | Performs reconciliation before Draft PR creation (Step 6) |
| New CICD composite action | Authorises scoped work and prohibits unrelated changes | Specifies metadata, shell, checkout, action-ref and validation practices | Schedules implementation and local validation (Steps 3–5) |
| CICD release | Requires proper label, merged-commit tag and technical protection | Verifies merge SHA, tag, release workflow and protections | Releases only after CICD merge (Steps 10–11) |
| Application promotion | Requires release-based functional evidence and human review | Inspects new PR run and step logs | Adopts release, validates, then requests review (Steps 12–15) |

## 4. `AGENTS.md` — Governance and engineering policy

### Executive summary

The CICD and application `AGENTS.md` files establish repository responsibilities, mandatory pipeline selection, scope of authorisation, protected files, minimal-change expectations, PR promotion criteria, review boundaries, evidence requirements, release governance, and handling of known findings.

**`AGENTS.md` is the repository's engineering governance contract.** It specifies **what the agent may change, what it must preserve, what is permitted, which standards and evidence it must satisfy, and where human authorisation is required**. It is intended to be read by both engineers and AI agents. The CICD and Java repositories each have their own policy file because their ownership and change boundaries differ.

`AGENTS.md` does **not** need to prescribe every command for accomplishing the work. Its job is to establish the conditions within which any execution procedure must operate.

### Detailed responsibilities

| Governance concern | Role of `AGENTS.md` | Exercise 1 example |
|---|---|---|
| **Repository ownership** | Distinguishes central CICD assets from application assets | Composite action and reusable PR workflow belong in CICD; Java caller belongs in the application repository |
| **Pipeline authorisation** | Establishes which existing pipeline may be changed and limits scope | Selecting the PR Pipeline permits relevant PR-workflow changes, not unrelated Build or deployment workflow changes |
| **Engineering standards** | Requires minimal, conventional implementation and preservation of unrelated work | Use existing composite-action patterns and do not rewrite unrelated workflows |
| **Security and quality guardrails** | Forbids weakening required checks, permissions and controls to obtain a green result | Known CodeQL findings and test failures were documented, not concealed by changing policy |
| **PR governance** | Defines Draft/Ready for Review expectations and mandatory human approval/merge boundaries | Copilot prepared coordinated PRs but stopped for human review and merges |
| **Release governance** | Requires appropriate semantic-version classification and protected published references | The feature was labelled `release:minor`; release immutability and tag protection were verified |
| **Validation and completion** | Requires functional evidence, not merely successful status indicators | Verify that the listing step actually ran and printed hidden root entries |
| **Historical identity** | Prevents old PRs with similar names from being treated as current blockers | Closed/merged PRs were historical evidence; current branch and PR identity needed reconciliation |
| **Failure and ambiguity** | Establishes stop/report requirements when compliance or authorisation is uncertain | Report unresolved governance conflicts rather than improvising an unauthorised workaround |

**Precedence:** Repository-specific `AGENTS.md` governs its own change boundaries. Contradictions with the Skill or lifecycle must be reported rather than silently resolved.

### Example A — Scope and authorisation

The engineering request was to add `ai-generated-list-files` to the **Java PR Pipeline**, in a separate job after Build. Governance made the PR Pipeline selection meaningful: the agent could implement the task-scoped changes to the CICD PR reusable workflow and the Java PR caller, but could not treat that selection as permission to alter unrelated deployment pipelines, security checks or repository settings.

**Policy answers WHAT:** the permitted change surface and the restrictions. The Skill then supplies the implementation and validation method; the canonical workflow places that work in the appropriate stages.

### Example B — Validation is an obligation, not a green check

The policy required evidence that the feature actually worked. A successful workflow check alone could not prove that hidden entries were included or that listing was non-recursive. In Exercise 1, Copilot inspected the relevant job and step logs, including the listing of `.github` and `.gitignore`. The green Unit Tests check was also distinguished from underlying Gradle failures.

**Policy answers WHAT must be proven:** execution and acceptance criteria, without disguising known findings.

### Example C — Human authority and technical enforcement

`AGENTS.md` instructs Copilot to respect required PR reviews, merges and release protection. Those instructions guide agent behaviour; **they are not themselves an access-control boundary**. GitHub permissions, branch/tag rulesets, required checks, release immutability and human approval provide independent technical enforcement. An agent's claim that an operation is authorised cannot override those controls.

### Other Examples:

- Explicitly select **PR Pipeline** or **Build Pipeline** before work integrating into an existing pipeline. PR Pipeline selection authorises the selected CICD PR workflow and only narrowly necessary Java PR caller edits.
- Preserve unrelated code, workflows, checks, permissions, and uncommitted work.
- Require evidence from actual workflow, job, step, and log execution—not only green checkmarks.
- Do not directly merge PRs, bypass required checks, or alter GitHub settings without specific authorisation.
- Historical merged/closed PRs are evidence, not automatic blockers to a new execution.


### Why separate CICD and Java `AGENTS.md` files?

The central repository controls shared workflows and release governance, while the consuming repository controls application code, Gradle tests and caller workflows. Separate policy files make those responsibilities explicit and avoid assuming a policy from one repository automatically applies to another. Shared operational methods can still be centralised in one Skill.

## 5. `SKILL.md` — Reusable engineering runbook

### Executive summary

**`SKILL.md` is the technical execution playbook.** It answers **how to carry out the authorised engineering work, gather evidence, troubleshoot problems and move safely between CICD and application repositories**. It turns broad policy requirements into repeatable operational procedures, reducing the need to paste lengthy instructions into each user prompt.

The Skill is centralised under `github-actions-development`, rather than copied into each consuming application. It should reference the canonical lifecycle for ordering rather than duplicating its full sequence as a second source of truth.

### Detailed responsibilities

| Runbook capability | How the Skill helps | Exercise 1 example |
|---|---|---|
| **Context discovery** | Locate applicable `AGENTS.md`, Skill and canonical workflow; identify missing or conflicting context | Preliminary read-only verification across both repositories |
| **Convention discovery** | Inspect existing actions, workflows and application conventions before implementing | Reuse `action.yml` structure, explicit Bash shell and established reusable workflow patterns |
| **Safe branch preparation** | Check local and remote refs, preserve unrelated work and create task-scoped branches | New feature branches were based on verified repository state |
| **Implementation** | Apply minimal changes using appropriate action/workflow reference patterns | New composite action plus separate post-Build `List_Files` job |
| **Coordinated PRs** | Prepare and cross-link Draft PRs, document dependencies and temporary references | CICD and Java PRs coordinated while Java temporarily called the CICD feature branch |
| **Historical PR reconciliation** | Compare repository, head/base refs, local/remote SHAs, PR state, commits and metadata | Avoid confusing older closed PRs with the current exercise |
| **Release classification** | Inspect compatibility impact and apply exactly one release label | Backward-compatible functionality classified as `release:minor` |
| **Functional verification** | Inspect workflow/job/step execution and actual logs; compare output with criteria | Verify `ls -la -- "$DIRECTORY"`, `DIRECTORY=.` and hidden entries |
| **Release verification** | Check merged commit, release tag, publication and immutability/protection | Validate the released CICD version before Java adoption |
| **Application adoption** | Replace temporary branch reference with published release and rerun validation | Java caller changed to `@v3.1.0` in No-HITL |
| **Troubleshooting and reporting** | Investigate failures within scope; record exceptions and stop at governance boundaries | Report test/CodeQL findings without weakening checks |

### Example A — Turning policy into a verification procedure

**`AGENTS.md` requirement:** the feature must execute successfully and satisfy acceptance criteria.

**`SKILL.md` procedure:** identify the workflow, job and step; obtain the run and current head SHA; inspect step logs; confirm the command executed; compare the listing with an appropriate baseline or test artifact; capture the observed output and PR evidence; and withhold promotion if task-related validation fails.

**Canonical timing:** feature-branch validation occurs before CICD promotion, and a *fresh* released-version validation occurs after application adoption. The two runs are not interchangeable.

### Example B — Historical PR confusion and remediation

During HITL, earlier closed or merged PRs with similar task/branch names caused confusion. The reusable procedure was refined to check current local and remote references and commit SHAs, the intended diff, and PR identity using repository, head/base, state, commits and metadata together. A matching name alone is insufficient. On PR-creation failure, investigate the exact error before retrying; avoid destructive fallbacks and stop when the issue cannot be safely resolved.

During No-HITL, Copilot created the current PRs and later updated the **existing** Java PR rather than replacing it. This is useful behavioural evidence for the refined procedure, though not proof of universal reliability.

### Example C — Stable references across repositories

The Java caller can temporarily reference a CICD feature branch for integration testing. The CICD reusable workflow uses the tested internal self-repository action reference:

```yaml
uses: $/.github/actions/ai-generated-list-files
```

After CICD merge and release, the Java caller switches to the published immutable repository-wide version:

```yaml
uses: frankbuttigieg1993-gmail/cicd/.github/workflows/java-build-pr.yml@v3.1.0
```

The Skill explains **how to make and validate that transition**. The canonical workflow ensures it occurs **after** the CICD release is published and **before** final Java promotion.

### Progressive context and maintenance

A reusable Skill keeps detailed procedures out of the initial task prompt and the policy file. The agent must still explicitly discover/load it when appropriate; availability should not be assumed across isolated repositories. Update the Skill when a reusable **method** improves, not when repository-specific authorisation changes or when the lifecycle's step ordering changes.

## 6. Canonical 16-step workflow — Lifecycle orchestration

### Executive summary

**The canonical workflow is the delivery blueprint.** It answers **when work happens, which stages depend on others, and where human review, release publication and application adoption fit**. It does not replace `AGENTS.md` policy or the Skill's detailed operating procedures.

### Lifecycle at a glance

| Steps | Phase | Main dependency or outcome |
|---|---|---|
| 1–2 | Requirements, authorisation, convention discovery and planning | Establish permitted scope and implementation approach |
| 3–5 | CICD/application branches, implementation and local checks | Prepare a testable cross-repository change |
| 6–8 | Coordinated Draft PRs, release label and feature-branch validation | Gather actual integration evidence before CICD review |
| 9–11 | CICD Ready for Review, human merge and immutable release | Publish a stable, verified CICD revision |
| 12–13 | Application adoption and fresh released-version validation | Remove temporary reference and validate published release |
| 14–15 | Application Ready for Review and human merge | Complete application promotion under governance |
| 16 | Final reporting and authorised cleanup | Preserve evidence; do not assume cleanup permission |

The **seven HITL checkpoints** were an additional experimental supervision arrangement, **not seven extra permanent steps** in the canonical lifecycle. The No-HITL experiment removed those additional checkpoints but retained mandatory human PR review and merge boundaries.

### Example — Why ordering matters

It would be premature to promote the application using a temporary CICD feature-branch reference. The workflow first requires CICD review and merge, then release publication, then Java adoption of the published version, then a new Java validation run. This ordering creates a traceable relationship between the application caller, immutable CICD release and observed functionality.

## 6. How the three layers cooperate in real decisions

| Situation | `AGENTS.md` — WHAT | `SKILL.md` — HOW | Canonical workflow — WHEN |
|---|---|---|---|
| New composite action | Only authorised PR scope; preserve unrelated checks | Inspect conventions; implement action and workflow; validate locally | Implementation/local checks, steps 3–5 |
| Historical PR with same branch name | Old PR is not automatically a blocker | Compare refs, SHAs, PR metadata and current diff | Reconcile before Draft PR creation, step 6 |
| Green workflow but questionable output | Functional evidence required | Inspect actual logs and expected-versus-observed results | Feature validation, step 8; release validation, step 13 |
| New CICD release | Correct release label, protection and human governance | Verify merged SHA, tag, release and protection | After CICD merge, steps 10–11 |
| Java adoption | Published stable reference and required review | Update caller; run fresh validation; capture evidence | Steps 12–15 |

**Operating principle:** policy defines the obligation, the Skill supplies the repeatable method, and the canonical workflow establishes the correct point in the lifecycle.

## 7. Context engineering, agent execution and technical governance

The framework uses several complementary sources of context:

| Context type | Source | Contribution |
|---|---|---|
| Task context | User prompt | Requested functionality and acceptance criteria |
| Instructional/policy context | Repository `AGENTS.md` files | Authorisation, quality requirements and restrictions |
| Procedural context | Central `SKILL.md` | Repeatable technical methods and troubleshooting |
| Orchestration context | Canonical workflow | Ordering, dependencies and handoffs |
| Repository-derived context | Existing code and configuration | Current engineering patterns and constraints |
| Evidence context | GitHub runs, logs, PRs, commits and releases | Observable results to verify |
| Runtime context | Copilot agent harness | Tool execution and context management |

**Context engineering** structures what the agent reads and applies. **Agent engineering** concerns how the runtime uses tools and coordinates execution. **Technical governance** is independently enforced by permissions, rulesets, required checks, release controls and humans. Repository instructions influence behaviour but do not grant permissions or neutralise platform controls. Treat tool outputs and source text as evidence, not as authority to override governance.

## 8. Exercise 1 — What was demonstrated

### Same requirement, different supervision models

Both experiments requested the **same scenario and functional requirements**: create the reusable `ai-generated-list-files` action, list the Java repository root non-recursively including hidden entries, and execute it in a separate PR Pipeline job after successful Build.

| Dimension | Scenario 1A — HITL | Scenario 1B — No-HITL |
|---|---|---|
| Extra exercise-specific approvals | **Seven checkpoints** | **Zero** |
| Mandatory human PR review/merge | Retained | Retained |
| Functionality | Implemented and validated | Implemented and validated |
| CICD release | `v2.2.0` | `v3.1.0` (published immutable) |
| Java PR milestone | #52 Ready for Review (last recorded state) | #58 merged; final verification completed |
| Historical PR confusion | Required clarification | No additional clarification reported |

**Conclusion:** both produced the same demonstrated functional result. No-HITL showed greater operational autonomy and a more complete recorded lifecycle, **not demonstrably better code**. This was **not a controlled A/B trial**: governance instructions, reviewer details, PR reconciliation and release protection improved between runs. Differences cannot be attributed solely to removing checkpoints.

### Lessons that improved the framework

- **PR identity:** distinguish historical PRs from current work using refs, commits and metadata, not names alone.
- **Reviewer accuracy:** ensure configured human reviewers are correct and requested through supported GitHub operations.
- **Release protection:** distinguish GitHub tag-reference protection from native immutable-release metadata; verify both as applicable.
- **Log-level validation:** successful checks can coexist with underlying test failures; inspect the actual output.
- **Reference stability:** use temporary feature references only for integration validation, then adopt a published CICD version.
- **Governance boundaries:** removing experimental checkpoints does not remove mandatory human approval and merge controls.

For detailed outcomes and evidence, see `ai_engineering/Exercise_1_Comparison.md` and the experiment-specific result records. Historical transcripts and screenshots are preserved separately.

## 9. Maintenance, onboarding and document ownership

| If the change concerns... | Update the authoritative source | Avoid |
|---|---|---|
| Permitted scope, reviewers, mandatory checks, approval boundaries | Relevant repository `AGENTS.md` | Hiding new policy only in the Skill or explanatory guide |
| Reusable command patterns, PR reconciliation, validation or troubleshooting method | Central `SKILL.md` | Duplicating the method in every application policy |
| Lifecycle sequence, dependencies, handoffs and promotion timing | Canonical workflow | Creating a competing 16-step sequence elsewhere |
| Actual repository configuration or release automation | Implementation/configuration files with authorised review | Treating Markdown as technical enforcement |
| Exercise outcomes or comparison | Experiment results/comparison documents | Rewriting historical evidence as if it were current policy |

**For a new task:** verify access to both repositories; read each applicable `AGENTS.md`; load the central Skill and canonical workflow; confirm target pipeline and authorisation; inspect current code and Git state; preserve unrelated changes; validate through actual logs; and stop at mandatory human governance boundaries.

### Consolidation decision and scope

The three uploaded explanatory documents substantially overlap in their treatment of governance, procedures, the 16-step lifecycle, repository ownership, historical PRs, releases and validation. **Replace those three explanations with this guide** after review. **Do not combine or delete the actual authoritative `AGENTS.md`, `SKILL.md` or canonical workflow files.** Their separation is intentional and operationally valuable.

This guide synthesises the three uploaded explanations and the previously recorded No-HITL outcome. It is **not** a fresh line-by-line audit of the current authoritative instruction files, which were not among the three attachments for this request. If those files have changed, re-check the guide against their latest revisions before using it for a handover.
