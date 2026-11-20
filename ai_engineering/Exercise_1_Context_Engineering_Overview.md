# Context Engineering in Exercise 1 — GitHub Copilot Agentic Engineering

## 1. Overview

Your Exercise 1 solution demonstrates how **context engineering can transform a simple user prompt into a structured, reusable and governed agentic engineering process**.

Rather than providing GitHub Copilot with detailed implementation instructions every time, you've separated engineering knowledge into reusable sources of context.

The current versioned-release framework uses:

- **User prompts** to define the engineering task.
- **Two repository-specific `AGENTS.md` files** to define shared CICD and application-specific policies.
- **One central `cicd/.github/skills/github-actions-development/SKILL.md`** to define the cross-repository execution procedure.
- **`.github/Canoncial Engineering Lifecycle.md`** as the authoritative human-readable 16-step process reference.
- **GitHub Actions release automation** to create immutable semantic-version tags on merged CICD commits; application repositories adopt releases independently.
- **Existing repository code** to provide established implementation conventions.
- **GitHub tools and execution results** to provide evidence during implementation and validation.
- **GitHub Copilot's agent harness** to coordinate the agent loop and tool execution.
- **GitHub permissions, rulesets and release protection** to enforce technical governance.

This allows GitHub Copilot to undertake different engineering tasks while following a consistent process.

### Current source-of-truth layout

```text
cicd/
  AGENTS.md                                      # shared CICD policy
  .github/Canoncial Engineering Lifecycle.md
  .github/skills/github-actions-development/SKILL.md  # one central procedure
  .github/workflows/promotion-auto-tag.yml      # semantic release automation
java_application/
  AGENTS.md                                      # application-specific policy
```

There is **no duplicate Java application Skill**. Both `AGENTS.md` files remain relevant; the central Skill references the shared process document. This separation reduces conflicting instructions and repeated maintenance.


---

## 2. Purpose of AGENTS.md

**`AGENTS.md` is the authoritative source of engineering policy, standards, restrictions and expected outcomes.**

Think of it as your team's engineering policy and operating standards. It defines **WHAT IS REQUIRED**, rather than providing the detailed procedure for executing every task.

### What your AGENTS.md defines

| Area | Purpose | Example |
|---|---|---|
| Repository responsibilities | Defines ownership and responsibilities | `cicd` owns reusable workflows and composite actions |
| Pipeline selection | Defines the target workflow and authorisation rules | Selecting PR Pipeline authorises changes to `java-build-pr.yml` |
| Engineering conventions | Establishes implementation standards | Prefer inline `run` commands |
| Implementation simplicity | Prevents unnecessary complexity | Avoid separate scripts for operations requiring 10 lines or fewer |
| Change boundaries | Restricts modifications | Do not modify unrelated workflows |
| Security requirements | Protects existing controls | Do not weaken tests or security scans |
| PR governance | Defines the required PR lifecycle | Draft → Validate → Ready for Review |
| Validation requirements | Defines successful delivery | Inspect logs and verify functional output |
| Completion criteria | Defines when success may be reported | Required checks passed and evidence collected |
| Status definitions | Defines how incomplete work is reported | `BLOCKED - AWAITING USER INPUT` |

### Example: Pipeline authorisation

Suppose your prompt says:

> Create a composite action named `ai-generated-list-files` that lists files in a directory and executes after Build in the PR Pipeline.

The applicable `cicd/AGENTS.md` and `java_application/AGENTS.md` establish that:

- The PR Pipeline has been explicitly selected.
- This authorises task-scoped modifications to `.github/workflows/java-build-pr.yml`.
- The Build Pipeline must remain unchanged.
- Existing tests and security checks must be preserved.
- The implementation must follow repository conventions.
- Draft PRs must be created.
- The implementation must be functionally verified.
- The agent must not bypass governance or perform an unauthorised merge. CICD merges may be carried out by an authorised human or an explicitly permitted GitHub auto-merge mechanism; application merge remains under human review.

The prompt doesn't need to repeat those instructions.

### Context engineering classification

This is **persistent instructional and policy context engineering**. You're providing reusable instructions that influence the LLM's behaviour across engineering tasks.

It is also a form of constraint engineering because it establishes boundaries around permitted changes. Importantly, `AGENTS.md` provides behavioural instructions. GitHub permissions and repository rulesets provide independent technical enforcement.

---

## 3. Purpose of SKILL.md

**`SKILL.md` is the authoritative source of the reusable engineering execution procedure.**

Think of it as your team's engineering runbook or Standard Operating Procedure (SOP). It defines **HOW TO EXECUTE THE ENGINEERING PROCESS**.

Your central Skill coordinates the complete 16-step development, release and application-adoption lifecycle. Its detailed procedures should refer to the authoritative process document rather than duplicate it.

| Lifecycle segment | Responsibility |
|---|---|
| Discovery and implementation | Confirm pipeline authorisation, inspect conventions, create branches, implement and validate locally |
| Draft PRs and feature testing | Create both Draft PRs, apply exactly one release label, test the application against the CICD feature branch, inspect logs |
| CICD promotion and release | Prepare CICD PR for review; after authorised merge, verify immutable semantic-version release on the actual merged commit |
| Application adoption | Replace temporary caller reference with the newly published CICD version; rerun application CI and verify functionality |
| Final review and reporting | Promote application PR when requirements are met, request review, document evidence and clean up safely |

### Example: Functional verification

Your `AGENTS.md` establishes the requirement:

> The agent must verify that newly implemented functionality executes successfully and produces the expected results.

Your `SKILL.md` operationalises that requirement. The agent must:

1. Identify the relevant workflow, job and step.
2. Retrieve the execution results.
3. Confirm the relevant step executed successfully.
4. Retrieve and inspect the actual execution logs.
5. Compare the observed output against the acceptance criteria.
6. Record supporting evidence in the PR.
7. Keep the PR in Draft if functional verification fails.

**AGENTS.md defines the requirement. SKILL.md defines the procedure for satisfying it.**

### Context engineering classification

This is **procedural context engineering**. You're providing reusable knowledge about how to complete a multi-step engineering task.

Skills can also support **progressive context loading**. Instead of placing every procedural detail into `AGENTS.md`, the relevant Skill can be discovered and loaded when the agent undertakes a matching engineering task. This helps keep the initial context focused.

---

## 4. Human and Agent Perspectives

One important improvement from your refactor is that your files serve two audiences.

### 4.1 Human perspective — Documentation and governance

A developer reading your files should quickly understand:

| Question | Where the answer is found |
|---|---|
| What is the standard engineering process? | Human quick reference |
| What are the engineering conventions? | AGENTS.md — Engineering Standards |
| What can the agent modify? | AGENTS.md — Governance |
| What are the completion criteria? | AGENTS.md — Validation and Completion |
| What happens when something fails? | SKILL.md — Validation and Remediation |
| What evidence should be provided? | SKILL.md — Reporting |

The human quick reference at the beginning allows developers to understand the overall engineering lifecycle without reading every detailed instruction.

### 4.2 Agent perspective — Actionable instructions

For GitHub Copilot, the same files provide precise instructions.

| Characteristic | Purpose |
|---|---|
| **Unambiguous** | Clear requirements using MUST, MUST NOT and STOP |
| **Actionable** | Specific procedures rather than general recommendations |
| **Discoverable** | The Skill must be available when the relevant task begins |
| **Consistent** | AGENTS.md and SKILL.md must not contain contradictory requirements |
| **Verifiable** | Important requirements must have observable outcomes |

For example, instead of simply saying *“Validate the implementation,”* your Skill requires the agent to inspect GitHub Actions execution logs and compare the observed output against the acceptance criteria. That makes the requirement actionable and verifiable.

---

## 5. Your Standard Engineering Lifecycle — Current 16-Step Model

The earlier lifecycle model has evolved into **16 steps** covering development, CICD release and application adoption. The detailed authoritative process is `cicd/.github/Canoncial Engineering Lifecycle.md`; the table below is a quick reference.

| Step | Activity | Expected outcome |
|---|---|---|
| 1 | Requirements analysis and pipeline selection | Confirm task, acceptance criteria, selected PR/Build pipeline and authorised scope; read applicable instructions. |
| 2 | Repository convention discovery and planning | Inspect comparable actions, reusable and caller workflows; plan minimal change. |
| 3 | Create CICD feature branch | Implement action/workflow changes; use approved self-repository references for internal actions. |
| 4 | Create application feature branch | Temporarily point affected caller workflow to CICD feature branch. |
| 5 | Local validation | Check YAML, metadata, job dependencies, refs, commands and scope. |
| 6 | Create both Draft PRs | Reconcile current local/remote refs and SHAs with historical PRs; then create cross-linked Draft PRs and document temporary references. |
| 7 | Apply semantic-release label | Apply exactly one of release:patch, release:minor or release:major to CICD PR and explain selection. |
| 8 | Feature-branch integration validation | Run application PR against CICD feature branch; inspect step logs and compare actual output with criteria. |
| 9 | Promote CICD PR | Record evidence and move to Ready for Review when applicable gates are met. |
| 10 | Review and merge CICD PR | Obtain required approval; authorised human/GitHub auto-merge performs merge. |
| 11 | Publish immutable CICD release | After merge, release automation tags actual merged commit and publishes one repository-wide semantic version. |
| 12 | Update application Draft PR | Change caller to newly released CICD tag; push to trigger fresh validation. |
| 13 | Final application validation | Verify released workflow, step logs, functionality and removal of temporary refs. |
| 14 | Promote application PR | Update evidence; mark Ready for Review when eligible and request designated reviewer. |
| 15 | Final human review and merge | Human approves and merges application PR under repository rules. |
| 16 | Final reporting and cleanup | Record PRs, release tag/SHA, logs and results; safely delete unused branches without altering immutable tags. |

**Remediation is iterative:** Investigate task-related failures and retest within authorised scope. Known accepted findings remain documented; mandatory GitHub checks and rulesets cannot be bypassed by a chat instruction.

### Lifecycle in one line

**Prompt → Discover → Plan → Branches → Implement → Local checks → Both Draft PRs → Release label → Feature-branch CI and logs → CICD review/merge → Immutable semantic release → Application version update → Released-version CI and logs → Application review/merge → Report.**

### Validated architecture and release assumptions

- The CICD repository has **one semantic version for the entire repository**, covering all workflows and composite actions.
- Internal CICD actions use the tested self-repository reference form, for example `uses: $/.github/actions/ai-generated-list-files`, so the reusable workflow and action resolve from the corresponding CICD revision.
- During development, an application caller references the CICD feature branch; after CICD release, it references an **immutable release tag** such as `@v2.2.0`.
- Tags are created **after** merging and point to the actual merged commit. This design is independent of merge-commit, squash and rebase merge strategies; the other strategies have not all been separately tested.
- `release:patch`, `release:minor`, and `release:major` classify CICD PRs. Exactly one label is required; release automation should reject missing or conflicting labels.
- Multiple application repositories may independently adopt different CICD versions. A CICD release does not automatically upgrade every consumer.
- In the latest supervised Exercise 1, CICD PR #7 used `release:minor` and the release workflow advanced `v2.1.0` to `v2.2.0` on the actual merged commit. Java Application PR #52 adopted `@v2.2.0` and its PR pipeline reproduced the expected file-listing behaviour. These outcomes are drawn from the recorded Copilot checkpoint reports and GitHub screenshots; this document does not independently rerun GitHub CI.

---

## 6. Types of Context Engineering You're Using

Based on your Exercise 1 implementation, there are six core forms of context engineering, plus explicit lifecycle orchestration and release/dependency context.

### Type 1 — Task Context Engineering

**Source: User prompt**

The prompt provides task-specific context. For example:

> Create a composite action named `ai-generated-list-files` that lists all files in a directory.
>
> Execute it after Build in the PR Pipeline.
>
> Follow the repository's AGENTS.md and development Skill.

The prompt establishes the objective, functionality, target pipeline and acceptance criteria.

**Purpose:** Define WHAT needs to be accomplished without repeating the engineering procedure.

### Type 2 — Instructional and Policy Context Engineering

**Source: AGENTS.md**

The two repository-specific `AGENTS.md` files provide reusable instructions governing the agent's behaviour. Examples include:

- Pipeline selection constitutes authorisation for the selected workflow.
- Existing repository conventions must be followed.
- Simple operations should use inline commands.
- Unrelated workflows must remain unchanged.
- PRs must initially be Draft.
- The agent must follow the defined merge-authorisation policy; it must never bypass approvals or merge the application PR on its own.

**Purpose:** Establish consistent engineering standards, expectations and behavioural boundaries.

### Type 3 — Procedural Context Engineering

**Source: SKILL.md**

The single central Skill instructs the agent to consult the authoritative 16-step process and execute the relevant operations:

```text
Task and policy discovery -> convention discovery -> implementation
    -> both Draft PRs + release label -> feature-branch validation
    -> CICD review and merge -> immutable semantic release
    -> application adoption -> released-version validation
    -> application review and final report
```

**Purpose:** Provide a reusable engineering procedure without embedding every implementation step into the prompt.

### Type 4 — Repository-Derived Context Engineering

**Source: Existing repository code**

Rather than specifying exactly how to implement every composite action, your instructions require the agent to inspect existing implementations.

For example, it might discover:

```yaml
runs:
  using: composite
  steps:
    - name: Build application
      shell: bash
      run: ./gradlew build
```

The LLM identifies established patterns:

- Composite actions use `action.yml`.
- Commands execute inline.
- Gradle operations use the Gradle wrapper.
- Simple functionality doesn't require separate scripts.

It then applies those conventions when implementing new functionality.

**Purpose:** Allow the agent to learn from your team's existing engineering practices rather than inventing new patterns.

This is a form of **dynamic context retrieval**.

### Type 5 — Tool and Evidence Context Engineering

**Sources: GitHub tools, GitHub Actions, terminal commands and tool responses**

During implementation, Copilot interacts with external systems. For example, it retrieves:

```text
Workflow: Java PR Build
Conclusion: success

Job: Build
Conclusion: success

Step: List directory contents
Conclusion: success
```

Your Skill requires the agent to go further: it must retrieve and inspect the actual logs. For example:

```text
Run ls -alrt

.gitignore
.github
README.md
build.gradle
```

The LLM then evaluates whether the requested functionality actually executed and whether the output satisfies the acceptance criteria.

| Type | Meaning |
|---|---|
| **Execution success** | Workflow, job and step completed successfully |
| **Functional success** | The requested operation actually performed its intended function |
| **Acceptance success** | The observed results satisfy the user's requirements |

**Purpose:** Ground the agent's decisions and final report in actual execution evidence.

Tool results are evidence, not authoritative instructions. Repository files and logs should not override the agent's governing instructions.

### Type 6 — Runtime Context Management

**Source: GitHub Copilot's agent harness and conversation context**

GitHub Copilot coordinates interactions between the LLM and available tools:

```text
LLM
 |
 | Proposes inspecting failed job
 v
GitHub Copilot Harness
 |
 | Executes tool request
 v
GitHub Actions
 |
 | Returns failure logs
 v
Harness
 |
 | Supplies results
 v
LLM
 |
 | Analyses failure
 v
Proposes remediation
```

The process repeats as necessary. The harness manages tool execution and supplies relevant results to the LLM. It may also select, truncate or summarise context as execution continues.

**Purpose:** Ensure the LLM receives relevant information throughout the agent loop.

Unlike the first five forms, runtime context management is primarily controlled by GitHub Copilot rather than directly by your repository instructions.

---


## 6A. Canonical Workflow as a Distinct Context Layer

The original description grouped lifecycle context with procedural context. The current architecture distinguishes them more precisely:

| Layer | Source | Question answered | Authority |
|---|---|---|---|
| Governance | `cicd/AGENTS.md` and `java_application/AGENTS.md` | **What is permitted, required, or prohibited?** | Repository-specific policy and authorisation |
| Execution | Central `github-actions-development/SKILL.md` | **How should each engineering operation be carried out and verified?** | Shared technical runbook |
| Orchestration | `Canoncial Engineering Lifecycle.md` | **When, in what order, and with which handoffs?** | Canonical 16-step lifecycle |

The three layers are complementary, not mutually exclusive. For example, policy requires technically protected release tags, the Skill directs the agent to verify them, and the canonical workflow places that verification after CICD merge and before application adoption. If the documents disagree, the agent should surface the conflict rather than silently selecting a convenient instruction.

**Human-facing documentation** such as the framework README explains the architecture and onboarding, but does not replace these authoritative instructions. This is a useful fourth *documentation surface*, not a fourth source of operational authority.

---

## 6B. Historical PR Reconciliation — A New Context-Engineering Improvement

The supervised exercise exposed a failure mode: older merged or closed PRs used the same feature-branch names as a new execution. Copilot initially treated the historical records as a possible blocker even though the current branches contained different commits. The new instructions address that ambiguity explicitly.

- **Governance context (`AGENTS.md`):** A matching branch name or SHA alone does not prove execution identity. Historical closed/merged PRs are evidence, not automatic blockers; preserve current work and existing authorisation boundaries.
- **Procedural context (`SKILL.md`):** Compare local worktree/ref/SHA with remote ref/SHA, inspect the intended diff, and identify PRs using repository, head/base refs, current head SHA, state, commits and relevant metadata together. Before creating a PR, check for an appropriate active PR. If creation fails, capture the exact error, investigate read-only, allow no more than two retries for plausible transient failures, and stop before destructive fallback changes.
- **Lifecycle context (Step 6):** Perform reconciliation **before** creating Draft PRs, not as an appendix after the 16-step process.

This is an example of **feedback-driven context engineering**: observed agent confusion was converted into reusable, task-agnostic instructions. The revised behaviour has been documented but should be tested again in a later execution; documentation correctness alone does not prove behavioural reliability.

---

## 6C. Exercise 1 — Observed HITL Execution and Evidence

The exercise used seven human-in-the-loop checkpoints to supervise the standard 16-step lifecycle. These checkpoints were **exercise-specific**, not additional mandatory steps in the canonical process.

| Checkpoint | Focus | Observed outcome |
|---|---|---|
| 1 | Planning | Scoped PR-only listing action, conventions and validation plan |
| 2 | Implementation | Composite action, post-Build job and temporary Java caller reference implemented and locally checked |
| 3 | Draft PRs and integration validation | CICD PR #7 and Java PR #52 created; feature-branch Build and List Files execution verified through logs |
| 4 | CICD PR promotion | CICD PR promoted to Ready for Review; reviewer request corrected and recorded |
| 5 | CICD release verification | CICD PR #7 merged; `v2.2.0` published on merge SHA; missing tag protection detected and subsequently addressed |
| 6 | Application release adoption and validation | Java PR #52 changed to `@v2.2.0`; fresh PR run confirmed the listing behaviour |
| 7 | Final application promotion | Java PR #52 promoted to Ready for Review; reviewer requested; no application merge claimed |

**Recorded references**

- CICD PR: [#7](https://github.com/frankbuttigieg1993-gmail/cicd/pull/7).
- Java application PR: [#52](https://github.com/frankbuttigieg1993-gmail/java_application/pull/52).
- CICD release: [`v2.2.0`](https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v2.2.0).
- Merged CICD commit: `1c0e8e3021c35de606b0df685d5fdd6374c66b78`.
- Release workflow run: [44014320065](https://github.com/frankbuttigieg1993-gmail/cicd/actions/runs/44014320065).
- Application release-based PR validation run: [44016664579](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44016664579).

The recorded listing output included **all 37 tracked Java repository root entries**, including hidden `.github` and `.gitignore`, along with checkout/runtime entries. The action ran after successful Build in the PR pipeline, and the same behaviour was observed against the released CICD version.

**Important caveats:** The Unit Tests job's green conclusion coexisted with known, intentionally tolerated underlying test failures. CodeQL findings were also known and out of scope for the listing feature. The final application PR was Ready for Review but GitHub reported aggregate merge state `UNSTABLE`; **Ready for Review is not Ready to Merge**. These limitations were documented, not resolved by weakening checks.

**Release-governance lesson:** The existing `v2.2.0` GitHub Release still reported `immutable: false` after publication. An active tag ruleset matching `refs/tags/v*` blocked updates and deletion without bypass actors, providing technical tag-reference protection. Native release immutability was enabled for future releases. Tag protection and GitHub Release immutability must not be conflated.

---

## 6D. Evidence, Governance, and Trust Boundaries

The framework separates three questions that a green CI indicator cannot answer by itself:

1. **Execution:** Did the intended workflow, job and step actually run on the relevant commit?
2. **Functionality:** Did the command perform the requested operation and produce the expected output?
3. **Governance:** Are the required review, branch, release, permissions and protection conditions satisfied?

A GitHub Action can complete successfully while an underlying test command reports failures. A release can publish successfully while its tag lacks technical protection. The agent must inspect logs, commit references, release metadata and rulesets rather than infer completion from high-level status.

`AGENTS.md` and `SKILL.md` are behavioural instructions, **not** security boundaries. GitHub rulesets, required checks, repository permissions, release protection and human approval provide independent technical governance. Tool outputs, PR bodies, source files and logs are evidence to inspect; they are not permission to override governing instructions.

---

## 6E. Scalability, Maintenance, and Handover

The central CICD repository owns one versioned set of reusable workflows and actions. Each consuming application may adopt the released version independently through a reviewed caller change. This architecture supports multiple application repositories without copying the central Skill into each repository, but Exercise 1 directly tested only the CICD–Java pair.

For a new maintainer:

1. Read the latest CICD and application `AGENTS.md` files, central Skill and canonical lifecycle **from the actual workspace**; do not assume they are automatically loaded or rely solely on chat summaries.
2. Confirm pipeline selection and task-specific authorisation before existing-pipeline integration work.
3. Check local and remote branch state and reconcile historical PRs before creating new Draft PRs.
4. Confirm exactly one release classification label, release automation configuration and current technical tag protection.
5. Preserve PR links, head and merged SHAs, workflow run links, step logs, expected-versus-observed output and accepted findings.
6. Treat reviewer requests, approval, release publication and application adoption as distinct gates.
7. Update shared procedure in the central Skill, repository-specific policy in the relevant `AGENTS.md`, and lifecycle sequencing in the canonical workflow; avoid duplicating long instructions across files.

**Further validation needed:** repeat the historical-PR scenario with the revised instructions; exercise lower-intervention operation while preserving human merge gates; test independent adoption by additional application repositories; and verify the next release under native release immutability plus tag rulesets.

---

## 7. How the Context Engineering Components Work Together

| Context engineering type | Source | Your implementation |
|---|---|---|
| **Task context** | User prompt | Defines functionality, acceptance criteria and target pipeline |
| **Instructional context** | AGENTS.md | Defines engineering standards, restrictions and expected outcomes |
| **Procedural context** | SKILL.md | Defines the reusable implementation and validation procedure |
| **Repository-derived context** | Existing repository code | Supplies examples of established engineering conventions |
| **Tool and evidence context** | GitHub Actions, Git and tool responses | Supplies execution evidence for validation and troubleshooting |
| **Runtime context management** | GitHub Copilot harness | Coordinates tool execution and working context |
| **Release and dependency context** | PR labels, tags, release events, version references | Grounds promotion and application adoption in the published CICD revision |

Task, policy, procedure and lifecycle context are deliberately designed; the canonical workflow is a distinct orchestration source rather than merely a quick reference. The fourth and fifth are forms of context you deliberately instruct the agent to retrieve. The sixth is primarily managed by the agent platform.

---

## 8. What Changed After Your Refactor and Versioned Release Redesign?

Before the refactor, your files contained overlapping instructions. For example, the PR lifecycle appeared in several sections across both files. That created a maintenance risk because changing one requirement could require updates in several places.

| Before | After |
|---|---|
| Engineering rules repeated across files | AGENTS.md is the authoritative policy |
| Procedures mixed with governance | SKILL.md is the authoritative procedure |
| Repeated lifecycle descriptions | Concise human-readable quick reference |
| Difficult to identify the source of a requirement | Clearer separation of responsibilities |
| Risk of contradictory instructions | Reduced duplication |
| Task examples mixed with general rules | Task-agnostic engineering conventions |
| General validation requirements | Explicit execution-log inspection and functional verification |
| Separate procedural Skill per application | One central Skill for the entire cross-repository lifecycle |
| Temporary action refs needing cleanup | Tested self-repository references for internal CICD actions |
| Application caller tracking `@main` | Controlled adoption of immutable semantic-version tags |
| CICD changes deployed without a release boundary | Post-merge tag and GitHub Release created from actual merged commit |

The refactor primarily improved the **organisation, consistency, discoverability and maintainability of the context supplied to the LLM**. It didn't fundamentally change your agent architecture.

---

## 9. Context Engineering vs Agent Engineering vs Governance

These are three related but distinct disciplines.

| Discipline | What it controls | Your implementation |
|---|---|---|
| **Context engineering** | What information and instructions the LLM receives | Prompts, AGENTS.md, SKILL.md, repository code and tool results |
| **Agent engineering** | How the system reasons, uses tools and completes tasks | GitHub Copilot, agent loop and integrations |
| **Governance and security engineering** | What operations are technically permitted | GitHub permissions, branch protection, required checks and reviews |

For example, your `AGENTS.md` tells Copilot not to merge pull requests. That is instructional context engineering.

GitHub branch protection and repository permissions can independently restrict unauthorised merges. That is technical governance.

**Instructions influence agent behaviour; permissions enforce access boundaries.**

---

## 10. Recommended Summary for Your Learning Notes

> My AI-Delegated GitHub Engineering solution uses multiple forms of context engineering to guide GitHub Copilot through a reusable, governed engineering lifecycle.
>
> The user prompt provides task-specific context by defining the requested functionality, acceptance criteria and target CI/CD pipeline.
>
> `cicd/AGENTS.md` and `java_application/AGENTS.md` provide persistent instructional and policy context by defining engineering standards, repository conventions, authorisation boundaries, governance requirements and completion criteria.
>
> The single central `SKILL.md` provides reusable procedural context by defining how the agent performs convention discovery, implementation, validation, troubleshooting and pull-request management. The canonical 16-step workflow separately defines sequencing, dependencies and human handoffs.
>
> Both files are designed for human and agent consumption. A concise quick reference explains the engineering lifecycle, while the detailed instructions provide actionable requirements for GitHub Copilot.
>
> Existing repository code provides dynamically retrieved context, allowing the LLM to identify and follow established engineering patterns.
>
> GitHub tools and GitHub Actions provide execution evidence, including workflow results and logs, which the LLM evaluates against the acceptance criteria.
>
> GitHub Copilot's agent harness manages the agent loop, tool execution and working context throughout the process.
>
> The standard engineering lifecycle is:
>
> **Prompt → Pipeline Selection → Convention Discovery → Plan → Branches → Implement → Local Validation → Both Draft PRs → Semantic Release Label → Feature-Branch CI and Log Verification → CICD Review/Merge → Immutable Semantic Release → Application Adoption → Released-Version CI and Log Verification → Application Review/Merge → Report.**
>
> The supervised Exercise 1 demonstrated this process through CICD release `v2.2.0` and application Ready for Review. Its lessons—including historical PR identity, reviewer correction and release protection—were incorporated into reusable instructions. Fully autonomous and multi-application operation remain future validation goals.

---

## 11. Key Takeaway

Your current central-Skill, versioned-release architecture establishes the following separation:

| Component | Responsibility |
|---|---|
| **User Prompt** | WHAT and WHERE |
| **AGENTS.md** | RULES, STANDARDS and EXPECTATIONS |
| **Central SKILL.md** | HOW: operational procedure across repositories |
| **Standard Workflow.md** | WHEN: authoritative 16-step sequence, dependencies and handoffs |
| **Release automation** | Semantic-version tagging on the actual CICD merge commit, subject to technical release/tag protection |
| **Application AGENTS.md** | Application-specific change boundaries and CICD release-consumption policy |
| **Existing Repository Code** | ESTABLISHED CONVENTIONS |
| **Tool Responses** | EXECUTION EVIDENCE |
| **LLM** | REASONING, DECISIONS and REPORTING |
| **GitHub Copilot Harness** | EXECUTION and CONTEXT MANAGEMENT |
| **GitHub Permissions** | TECHNICAL ENFORCEMENT |

### Final assessment

The supervised evidence shows your approach has evolved from simply instructing an AI agent to create a GitHub Actions component into a **reusable, governed agentic engineering and versioned-release framework**.

The most significant context-engineering improvement is that you've moved recurring engineering knowledge out of individual prompts and into structured, reusable instructions.

You've also introduced two particularly valuable capabilities:

**Repository-derived context:** The agent discovers and follows your team's existing engineering conventions.

**Evidence-based validation:** The agent must prove that its implementation works by inspecting actual execution results, rather than relying solely on successful GitHub Actions status checks.

Together, these make the framework more maintainable and auditable. Further exercises are needed to establish reliability under autonomous execution and across additional application repositories.
