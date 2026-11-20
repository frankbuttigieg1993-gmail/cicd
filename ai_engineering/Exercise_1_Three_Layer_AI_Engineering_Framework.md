# Exercise 1 — Purpose of AGENTS.md, SKILL.md and the Canonical Workflow

Based on what we accomplished in **Exercise 1**, the three Markdown files form the foundation of a **governed, reusable AI-assisted software engineering framework**.

Each file serves a distinct purpose, but together they enable GitHub Copilot to understand **what it is allowed to do, how it should perform engineering activities, and when those activities must occur**.

The important achievement is that much of the engineering knowledge and process has moved out of individual prompts and into reusable, version-controlled instructions.

## 1. AGENTS.md — Engineering Governance and Policy

**Purpose: Defines the rules, responsibilities, authorisation boundaries and quality requirements that govern the AI agent's behaviour.**

`AGENTS.md` is the **engineering governance contract** between the human operator and GitHub Copilot. It establishes the rules that Copilot must follow when operating within a repository.

### What it controls

- **Repository responsibilities:** Which repository owns reusable workflows, composite actions, application code and caller workflows.
- **Authorisation boundaries:** What Copilot may modify based on the selected pipeline and what requires additional human approval.
- **Engineering standards:** Requirements for code quality, security, minimal changes and preserving existing functionality.
- **Pull request governance:** When PRs must remain Draft, when they can be promoted and who must review them.
- **Release governance:** Semantic versioning, immutable release tags and production-safe references.
- **Validation requirements:** Actual execution evidence must support claims of functional correctness.
- **Safety restrictions:** Copilot must not bypass required checks, overwrite unrelated work or merge PRs without authorisation.
- **Historical PR handling:** Previously closed or merged PRs must not automatically block new engineering work.

### What Exercise 1 demonstrated

Copilot followed these governance requirements throughout the exercise. For example, it:

1. Stopped at each HITL checkpoint.
2. Preserved unrelated repository modifications.
3. Distinguished successful CI execution from actual functional correctness.
4. Identified missing release-tag protection.
5. Refused to proceed until the governance requirement was satisfied.
6. Requested the designated reviewers.
7. Distinguished Ready for Review from Ready to Merge.

**Key outcome:** `AGENTS.md` helped ensure Copilot did not simply complete the requested technical change, but also respected the engineering controls surrounding that change.

---

## 2. SKILL.md — Reusable Engineering Execution Procedure

**Purpose: Defines the operational procedures, technical conventions and verification methods that Copilot uses to perform engineering tasks consistently.**

`SKILL.md` is the **AI agent's reusable engineering playbook**. Where `AGENTS.md` establishes the rules, `SKILL.md` explains how Copilot should execute engineering activities while complying with those rules.

### What it controls

The central `github-actions-development/SKILL.md` describes:

- How to discover existing engineering conventions.
- How to plan and implement composite actions and reusable workflows.
- How to create and manage feature branches safely.
- How to coordinate changes across CICD and application repositories.
- How to create and cross-reference Draft PRs.
- How to classify changes using semantic-version labels.
- How to validate functionality using actual GitHub Actions execution logs.
- How to verify immutable CICD releases.
- How to update application callers to released CICD versions.
- How to reconcile historical PRs with current branch and commit state.
- How to investigate failures without exceeding authorisation boundaries.

### What Exercise 1 demonstrated

Copilot successfully applied the shared engineering procedure to implement and validate the file-listing composite action. It independently:

1. Inspected existing composite actions to discover conventions.
2. Created the new composite action.
3. Integrated it into the PR reusable workflow.
4. Created coordinated feature branches and Draft PRs.
5. Applied the `release:minor` classification.
6. Executed and verified cross-repository integration tests.
7. Verified the published CICD release.
8. Updated the Java Application PR to consume `v2.2.0`.
9. Revalidated the functionality against the released version.

One particularly important result was the successful use of:

```yaml
uses: $/.github/actions/ai-generated-list-files
```

This allowed the CICD reusable workflow to resolve its internal composite action from the corresponding CICD revision, avoiding permanent dependencies on temporary feature branches.

**Key outcome:** `SKILL.md` enabled Copilot to apply a repeatable engineering procedure rather than relying on detailed task-specific instructions. Because the Skill is centralised in the CICD repository, the same procedure can be reused across multiple application repositories.

---

## 3. Canonical Workflow — Engineering Lifecycle and Orchestration

**Purpose: Defines the authoritative sequence of engineering activities, dependencies, promotion gates and handoffs from requirements analysis through implementation, release and application adoption.**

The canonical workflow is the **engineering lifecycle blueprint**. It establishes when activities occur and how the CICD and application repositories progress through the delivery process.

### What it controls

The canonical document defines a standard **16-step lifecycle** covering:

| Stage | Activities |
|---|---|
| Requirements and planning | Identify the selected pipeline, discover conventions and define the implementation |
| Implementation | Create branches, implement changes and validate locally |
| Draft PR preparation | Create cross-linked Draft PRs and apply semantic-version labels |
| Integration validation | Validate the CICD feature branch through the consuming application |
| CICD promotion | Promote the CICD PR for human review and merge |
| Release management | Publish the next immutable semantic-version release |
| Application adoption | Update the application to consume the released CICD version |
| Final validation | Verify the application against the published release |
| Application promotion | Request final human review and merge |
| Completion | Record evidence, outcomes and perform authorised cleanup |

### What Exercise 1 demonstrated

The canonical workflow successfully coordinated changes across two independent repositories.

**CICD feature development → Application integration testing → CICD review and merge → Immutable semantic release → Application adoption → Final validation → Human review.**

This sequencing solved the temporary feature-branch reference problem encountered during the initial implementation. It also made the release process independent of Git merge strategy because the semantic-version release was created from the actual merged CICD commit.

**Key outcome:** The canonical workflow gave Copilot a consistent delivery lifecycle that can scale from one application repository to multiple independent consumers of the central CICD repository.

---

## 4. How the Three Components Work Together

| Component | Primary question | Responsibility |
|---|---|---|
| **AGENTS.md** | **WHAT is permitted and required?** | Governance, policies, authorisation, safety and quality standards |
| **SKILL.md** | **HOW should the work be performed?** | Engineering procedures, technical conventions, validation and troubleshooting |
| **Canonical Workflow** | **WHEN and in what order?** | Lifecycle sequencing, dependencies, promotion gates and handoffs |

These responsibilities complement one another. For example, `AGENTS.md` defines the requirement for immutable releases, the Skill describes how to verify them, and the canonical workflow specifies when that verification occurs.

### Example: Creating a Pull Request

Consider the historical PR issue encountered during Exercise 1.

**AGENTS.md establishes the policy:** A previously merged or closed PR must not automatically prevent new work merely because it used the same branch name.

**SKILL.md provides the procedure:** Copilot compares local and remote branch references, commit SHAs, PR states, head and base branches, and relevant metadata to distinguish historical work from the current execution.

**Canonical workflow establishes the timing:** This reconciliation occurs during Step 6, before creating the Draft PRs.

This illustrates how the three documents complement one another without unnecessarily duplicating instructions.

---

## 5. The Bigger Achievement — Separating Engineering Knowledge from Individual Prompts

Traditionally, a lengthy prompt might explain which files to modify, which engineering conventions to follow, how to create branches and PRs, how to validate implementation, how to release changes, and how to handle failures. That approach repeats substantial instructions across tasks.

Your architecture changes this: the human can provide a relatively concise engineering requirement, and Copilot consults the repository policies, shared engineering procedures and canonical lifecycle to determine how to execute it.

### The resulting model

**Human provides the engineering objective.**

↓

**AGENTS.md establishes governance and authorisation.**

↓

**SKILL.md provides reusable engineering procedures.**

↓

**Canonical workflow defines the delivery sequence.**

↓

**Copilot executes the authorised activities and gathers evidence.**

↓

**Human intervention occurs at defined approval and review boundaries.**

This separation improves consistency and maintainability because shared procedures can be updated centrally rather than repeated in every task prompt. Each application repository retains its own governance requirements while consuming a common CICD engineering procedure.

---

## 6. What Exercise 1 Actually Proved

| Capability | Exercise 1 result |
|---|---|
| Repository instruction discovery | ✅ Demonstrated |
| Engineering convention discovery | ✅ Demonstrated |
| Minimal, scoped implementation | ✅ Demonstrated |
| Cross-repository coordination | ✅ Demonstrated |
| Draft PR lifecycle management | ✅ Demonstrated |
| Semantic-version classification | ✅ Demonstrated |
| Feature-branch integration validation | ✅ Demonstrated |
| CICD release verification | ✅ Demonstrated |
| Release governance enforcement | ✅ Demonstrated |
| Application adoption of immutable release | ✅ Demonstrated |
| Functional verification using execution logs | ✅ Demonstrated |
| Human approval boundaries | ✅ Demonstrated |
| Historical PR reconciliation | ⚠️ Instructions improved; future behavioural validation needed |
| Fully autonomous execution | ⏳ Not yet demonstrated |
| Scaling to multiple application repositories | ⏳ Architecturally supported; not yet tested |

Exercise 1 provides strong evidence that the instructions can guide Copilot through a complex, supervised, cross-repository engineering lifecycle. It does not yet prove that Copilot will reliably perform the same activities without intermediate human intervention, or that the approach will behave consistently across many application repositories.

---

## 7. How to Describe the Architecture Professionally

| Artifact | Architectural role | Description |
|---|---|---|
| **AGENTS.md** | Governance Layer | Defines repository-specific policies, responsibilities, authorisation boundaries, safety controls and engineering quality requirements governing AI-assisted development. |
| **SKILL.md** | Execution Layer | Provides reusable operational procedures, technical conventions, validation methods and failure-handling guidance for consistent engineering execution across repositories. |
| **Canonical Workflow** | Orchestration Layer | Defines the authoritative engineering lifecycle, including activity sequencing, cross-repository dependencies, promotion gates, release management and human handoffs. |

Together, they form a **three-layer, repository-driven AI engineering framework**.

**Important qualification:** These files provide behavioural instructions to Copilot. They are not themselves a technical security boundary. GitHub permissions, branch rulesets, required checks and release protections remain responsible for enforcing the relevant controls.

---

## Overall Assessment

The value of the approach is not simply that Copilot created a composite action. A relatively small engineering requirement resulted in a coordinated delivery process involving:

- Two independent repositories.
- Reusable workflows and composite actions.
- Cross-repository integration testing.
- Semantic-versioned releases.
- Immutable release references.
- Evidence-based functional verification.
- Human-controlled promotion and approval.
- Governance enforcement and exception reporting.

The process also exposed weaknesses in the instructions that could be corrected centrally.

**Continuous improvement feedback loop:**

**Define standards → Execute engineering task → Observe agent behaviour → Identify gaps → Improve reusable instructions → Validate again.**

### Preferred one-sentence description

> **A three-layer AI engineering framework that separates governance (AGENTS.md), execution procedures (SKILL.md), and lifecycle orchestration (Canonical Workflow), enabling consistent, auditable and human-governed software delivery across multiple repositories.**

That describes what was built and validated through Exercise 1.
