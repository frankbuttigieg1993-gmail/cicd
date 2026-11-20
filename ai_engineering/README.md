# CICD — Reusable GitHub Actions Engineering Platform

## 1. Introduction

This repository provides reusable GitHub Actions workflows, composite actions, and shared automation for application repositories. It centralises common CI/CD capabilities so that consuming applications can adopt a versioned, reviewed implementation rather than duplicating pipeline logic. The Java Application repository is a principal consumer.

Key capabilities include application pull-request validation, build and security checks, development deployment, reusable composite actions, and automated semantic-version release promotion. The repository also contains a three-layer instruction framework for AI-assisted engineering: governance (`AGENTS.md`), operational procedures (`SKILL.md`), and an authoritative 16-step lifecycle.

## 2. Main CI/CD pipelines

| Pipeline | Workflow | Purpose | Typical outcome |
|---|---|---|---|
| **PR Pipeline** | [`.github/workflows/java-build-pr.yml`](.github/workflows/java-build-pr.yml) | Reusable validation workflow for application pull requests. Runs build and unit-test jobs and, following Exercise 1, a separate `List_Files` job after `Build`. | Evidence for human PR review; does not itself approve or merge a PR. |
| **Build Pipeline** | [`.github/workflows/java-build-all.yml`](.github/workflows/java-build-all.yml) | Broader build pipeline with build, tests, security analysis, software bill of materials, image publishing and tagging stages. | Build and package artefacts for downstream use, subject to job results and configured controls. |
| **Dev Deployment Pipeline** | [`.github/workflows/Java-Deployment-Dev.yaml`](.github/workflows/Java-Deployment-Dev.yaml) | Deploys a selected application image to the development EKS environment using AWS role assumption, Kubernetes tooling and Helm. | A development-environment deployment; separate from PR validation and CICD repository release promotion. |
| **CICD Release Promotion** | [`.github/workflows/promotion-auto-tag.yml`](.github/workflows/promotion-auto-tag.yml) | On merge of a CICD PR into `main`, reads the PR release label, calculates the next semantic version, creates a tag at the merge commit and publishes a GitHub Release. | A published versioned reference for application workflows. |

**Scope distinction:** The CICD release promotion workflow versions the **CICD repository and its reusable automation**. It does not itself deploy the Java application to development. The Build and Dev Deployment pipelines are separate application delivery activities.

## 3. Repository layout and document responsibilities

| Path | Role and purpose |
|---|---|
| [`.github/workflows/`](.github/workflows/) | **Executable CI/CD orchestration:** reusable PR/build workflows, deployment workflows and release-promotion automation. These are actual GitHub Actions definitions, not agent instructions. |
| [`.github/actions/`](.github/actions/) | **Reusable implementation components:** composite actions and supporting resources invoked by workflows. Exercise 1 introduced `ai-generated-list-files`. |
| [`.github/skills/github-actions-development/SKILL.md`](.github/skills/github-actions-development/SKILL.md) | **Operational runbook — HOW to execute:** reusable procedures for discovering conventions, preparing branches, reconciling existing PRs, implementing changes, validating logs, releasing and adopting published workflows. It translates governance into repeatable engineering actions. |
| [`AGENTS.md`](AGENTS.md) | **Agent governance — WHAT is permitted and the guardrails:** repository ownership, authorisation, scope restrictions, protected operations, evidence standards and mandatory human approval/merge boundaries. It constrains the agent; it is not a step-by-step implementation runbook. |
| [`../.github/Canoncial Engineering Lifecycle.md`](../.github/Canoncial%20Engineering%20Lifecycle.md) | **Canonical lifecycle — WHEN and in WHAT ORDER:** the authoritative 16-step sequence from planning and feature-branch work through cross-repository PRs, CICD release, application adoption, human merges and final reporting. It orchestrates the work without replacing policy or the runbook. |
| [`ai_engineering/`](ai_engineering/) | **Experiment documentation:** the two Exercise 1 execution histories, prompts, executive summaries and final HITL/No-HITL comparison. Historical results are evidence, **not instructions for future agents**. |
| [`README.md`](README.md) | **Human-facing entry point:** repository purpose, major pipelines, governance model and links to the authoritative instructions and experiment results. |

### How the three instruction layers work together

**`AGENTS.md` = permission and guardrails (WHAT is allowed).** **`SKILL.md` = execution runbook (HOW to do it safely).** **Canonical workflow = lifecycle orchestration (WHEN and in WHAT order).** GitHub and cloud enforcement mechanisms independently apply technical restrictions; prose instructions are not a substitute for access controls.

**Exercise 1 example:** The requirement was to add a reusable directory-listing action to the Java PR Pipeline. `AGENTS.md` limited changes to the authorised PR pipeline and required human-controlled merges. The Skill guided the agent through branch/PR reconciliation, action implementation, actual-log validation and immutable-release adoption. The canonical workflow required the CICD PR to be reviewed and merged, the versioned CICD release to be published, and only then the Java caller to adopt the released tag and undergo fresh validation.

## 4. Release promotion and versioned adoption

The [CICD Semantic Version Release workflow](.github/workflows/promotion-auto-tag.yml) runs when a pull request targeting `main` is closed **and merged**. It requires exactly one release classification label: `release:patch`, `release:minor`, or `release:major`. It determines the next version from existing semantic-version tags, verifies the merged commit is reachable from `main`, refuses to overwrite an existing release tag, creates a tag at the merged commit, and publishes a GitHub Release.

**Exercise 1 release example — `v3.1.0`:** CICD PR **#8** introduced backward-compatible new functionality and carried `release:minor`. After the mandatory human merge, the release workflow published **CICD Release v3.1.0**, with tag target `e7ecad9de8694095e2ea99d1f3ce77d23fc4b5b7`. The GitHub Releases page displayed **Latest** and **Immutable**, and the active release-tag ruleset provided an additional protection boundary. This is the release shown in the Exercise 1 screenshot; it is an example of the promotion outcome, not a permanently prescribed version.

Applications consume the published reusable workflow through a versioned reference, for example the **Exercise 1 result**:

```yaml
uses: frankbuttigieg1993-gmail/cicd/.github/workflows/java-build-pr.yml@v3.1.0
```

During feature validation, the Java caller temporarily used a CICD feature-branch reference. After release publication, it was updated to `@v3.1.0` and a **fresh PR Pipeline run** verified the published implementation before the Java PR was reviewed and merged. For future changes, use the **actual newly published and verified release**, not this historical example by default.

## 5. Engineering governance and onboarding

Before modifying the repository, read [`AGENTS.md`](../AGENTS.md), the [central Skill](../.github/skills/github-actions-development/SKILL.md), and the [canonical lifecycle](../.github/Canoncial%20Engineering%20Lifecycle.md). For work involving the Java Application repository, also read its own `AGENTS.md`; instructions from this repository are **not automatically inherited** by another repository.

A task must identify its intended pipeline and authorised change scope. Use task-specific feature branches and Draft PRs, preserve unrelated work, validate actual workflow/job/step logs rather than relying on green status alone, and document outstanding findings. Required human reviews and merges remain human actions. Do not modify security settings, rulesets, infrastructure or governance instructions merely to unblock implementation; obtain the separate authorisation required by repository policy.

**Onboarding sequence:** understand the repository and pipelines here; read the three authoritative instruction documents; inspect current GitHub repository settings and applicable application instructions; then establish a fresh branch/PR baseline before execution.

## 6. AI engineering guardrails — four enforcement tiers

The AI agent operates within layered controls. The tiers below describe the **control model**; current AWS account policies, role trust conditions, GitHub settings and reviewer requirements must be checked in their respective consoles before treating any individual control as verified.

| Tier | Control boundary | Purpose and examples |
|---|---|---|
| **1. AWS account and environment** | Cloud and runtime boundary | AWS account configuration, environment separation, service-side permissions and EKS/deployment configuration limit the cloud resources and environments an automation can affect. The Dev Deployment workflow targets the `dev` environment and an EKS cluster. |
| **2. IAM and workload identity** | Authentication and authorisation | IAM roles/policies and the GitHub-to-AWS role-assumption path determine which AWS actions a workflow can perform. The Dev Deployment workflow references an AWS role for credential configuration; its effective permissions and trust policy must be verified in AWS. |
| **3. GitHub repository enforcement** | Source-control and release protection | Repository permissions, required checks/reviews, branch rulesets, tag-protection rulesets and immutable GitHub Releases constrain merges, tag mutation and release changes independently of agent instructions. Exercise 1 verified the protected immutable `v3.1.0` release. |
| **4. Agent instructions and workflow process** | Behavioural and procedural guardrails | `AGENTS.md` establishes allowed scope and human boundaries; `SKILL.md` provides safe procedures; the canonical workflow enforces sequencing and evidence handoffs. GitHub Actions job permissions and validation provide further workflow-level controls. |

**Important:** Tier 4 guidance does not technically enforce Tiers 1–3. A compliant design requires both agent behaviour and independently configured access controls. This README does not claim that every AWS/IAM setting has been audited.

## 7. AI Engineering experiment — Exercise 1

### What the agent was asked to build

Implement a reusable GitHub Actions composite action named `ai-generated-list-files` that lists the immediate contents of a specified directory, **including hidden files and directories**, and integrate it as a separate `List_Files` job in the Java Application **PR Pipeline**, dependent on a successful `Build`. Preserve existing build, test and security behaviour, and verify the actual listing output and job execution.

### Context supplied to the agent

The agent was instructed to discover and read the CICD and Java Application `AGENTS.md` files, the central `github-actions-development` Skill, the canonical 16-step workflow and relevant existing workflows/actions. These files supplied governance (**what was permitted**), operational procedures (**how to execute**), and lifecycle order (**when to act**). The engineering requirement and explicit pipeline selection defined the task-specific scope.

### Two executions of the same scenario

| | **Scenario 1A — HITL at each stage** | **Scenario 1B — No additional HITL** |
|---|---|---|
| Scenario and functional requirements | Same directory-listing action, integration and acceptance criteria | **Identical** |
| Experimental intervention model | Copilot paused at **seven additional human approval checkpoints** throughout execution | Copilot progressed without additional experimental checkpoints |
| Mandatory PR governance | Human PR review and merge still required | **Human PR review and merge still required** |
| CICD release | `v2.2.0` | `v3.1.0` |
| Functional outcome | Implementation and integration validated | Same functionality implemented and validated |
| Final recorded application milestone | Java PR **#52** reached Ready for Review | Java PR **#58** merged; final lifecycle verified |

**Conclusion:** Both execution models achieved the required functional outcome. The deliberate difference was **seven additional experimental HITL checkpoints in Scenario 1A versus none in Scenario 1B**; neither model removed mandatory human PR approvals and merges. The framework and repository protections were refined between runs, so this comparison does **not** isolate the effect of HITL removal alone.

See [AI Engineering](ai_engineering/README.md) for the two experiment histories and [comparison](ai_engineering/Exercise_1_Comparison.md) for conclusions and limitations. Original evidence is stored separately.
