# Context Engineering in Exercise 1 — GitHub Copilot Agentic Engineering

## 1. Overview

Your Exercise 1 solution demonstrates how **context engineering can transform a simple user prompt into a structured, reusable and governed agentic engineering process**.

Rather than providing GitHub Copilot with detailed implementation instructions every time, you've separated engineering knowledge into reusable sources of context.

Your solution uses:

- **User prompts** to define the engineering task.
- **`AGENTS.md`** to define engineering policies, standards, restrictions and completion requirements.
- **`SKILL.md`** to define the reusable engineering procedure.
- **Existing repository code** to provide established implementation conventions.
- **GitHub tools and execution results** to provide evidence during implementation and validation.
- **GitHub Copilot's agent harness** to coordinate the agent loop and tool execution.
- **GitHub permissions and branch protection** to enforce technical governance.

This allows GitHub Copilot to undertake different engineering tasks while following a consistent process.

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

Your `AGENTS.md` establishes that:

- The PR Pipeline has been explicitly selected.
- This authorises task-scoped modifications to `.github/workflows/java-build-pr.yml`.
- The Build Pipeline must remain unchanged.
- Existing tests and security checks must be preserved.
- The implementation must follow repository conventions.
- Draft PRs must be created.
- The implementation must be functionally verified.
- The agent must never merge the PRs.

The prompt doesn't need to repeat those instructions.

### Context engineering classification

This is **persistent instructional and policy context engineering**. You're providing reusable instructions that influence the LLM's behaviour across engineering tasks.

It is also a form of constraint engineering because it establishes boundaries around permitted changes. Importantly, `AGENTS.md` provides behavioural instructions. GitHub permissions and repository rulesets provide independent technical enforcement.

---

## 3. Purpose of SKILL.md

**`SKILL.md` is the authoritative source of the reusable engineering execution procedure.**

Think of it as your team's engineering runbook or Standard Operating Procedure (SOP). It defines **HOW TO EXECUTE THE ENGINEERING PROCESS**.

Your refactored Skill uses five operational phases.

| Phase | Responsibility |
|---|---|
| **1. Select, discover and plan** | Confirm pipeline selection, analyse requirements, inspect repository conventions and establish the implementation plan |
| **2. Branch, implement and validate locally** | Create feature branches, implement minimal changes and execute local validation |
| **3. Publish Draft PRs** | Push changes and create cross-referenced Draft PRs |
| **4. Execute CI, inspect logs and verify functionality** | Run pipelines, inspect execution evidence, validate behaviour and remediate failures |
| **5. Promote PRs, request review and report** | Mark successful PRs Ready for Review, request review and report results |

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

## 5. Your Standard Engineering Lifecycle

Your refactored documents establish the following standard process.

| Step | Activity | Expected outcome |
|---|---|---|
| **1** | Pipeline selection | User explicitly selects PR or Build Pipeline |
| **2** | Requirements and convention discovery | Agent understands requirements and existing engineering patterns |
| **3** | Planning | Identify implementation approach and affected files |
| **4** | Branch creation | Create task-specific feature branches |
| **5** | Implementation | Make minimal changes following repository conventions |
| **6** | Local validation | Validate syntax and execute relevant tests |
| **7** | Draft PR creation | Create cross-referenced Draft PRs |
| **8** | CI/CD and functional verification | Inspect workflow, job and step status, actual logs and expected output |
| **9** | PR promotion | Mark both PRs Ready for Review after successful validation |
| **10** | Human review | Request review from `frankbuttigieg-93`; never merge |

**Failure investigation and remediation occur during validation whenever required.**

### Complete lifecycle

**Prompt → Pipeline Selection → Convention Discovery → Plan → Branch → Implement → Local Validation → Draft PRs → Execute CI → Inspect Logs → Verify Functionality → Remediate (if required) → Ready for Review → Human Review.**

This lifecycle is reusable regardless of whether the task involves creating a composite action, modifying a reusable workflow or troubleshooting a failed build.

---

## 6. Types of Context Engineering You're Using

Based on your Exercise 1 implementation, there are six main forms of context engineering.

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

Your `AGENTS.md` provides reusable instructions governing the agent's behaviour. Examples include:

- Pipeline selection constitutes authorisation for the selected workflow.
- Existing repository conventions must be followed.
- Simple operations should use inline commands.
- Unrelated workflows must remain unchanged.
- PRs must initially be Draft.
- The agent must never merge PRs.

**Purpose:** Establish consistent engineering standards, expectations and behavioural boundaries.

### Type 3 — Procedural Context Engineering

**Source: SKILL.md**

Your Skill defines the operational sequence the agent follows:

```text
Requirements Analysis
        |
        v
Convention Discovery
        |
        v
Implementation Planning
        |
        v
Branch Creation
        |
        v
Implementation
        |
        v
Draft PR Creation
        |
        v
CI/CD Validation
        |
        v
Functional Verification
        |
        v
Ready for Review
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

## 7. How the Context Engineering Components Work Together

| Context engineering type | Source | Your implementation |
|---|---|---|
| **Task context** | User prompt | Defines functionality, acceptance criteria and target pipeline |
| **Instructional context** | AGENTS.md | Defines engineering standards, restrictions and expected outcomes |
| **Procedural context** | SKILL.md | Defines the reusable implementation and validation procedure |
| **Repository-derived context** | Existing repository code | Supplies examples of established engineering conventions |
| **Tool and evidence context** | GitHub Actions, Git and tool responses | Supplies execution evidence for validation and troubleshooting |
| **Runtime context management** | GitHub Copilot harness | Coordinates tool execution and working context |

The first three are the forms of context you design directly. The fourth and fifth are forms of context you deliberately instruct the agent to retrieve. The sixth is primarily managed by the agent platform.

---

## 8. What Changed After Your Refactor?

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
> `AGENTS.md` provides persistent instructional and policy context by defining engineering standards, repository conventions, authorisation boundaries, governance requirements and completion criteria.
>
> `SKILL.md` provides reusable procedural context by defining how the agent performs convention discovery, implementation, validation, troubleshooting and pull-request management.
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
> **Prompt → Pipeline Selection → Convention Discovery → Plan → Branch → Implement → Local Validation → Draft PRs → Execute CI → Inspect Logs → Verify Functionality → Remediate (if required) → Ready for Review → Human Review.**
>
> The result is a task-agnostic engineering process in which simple user prompts can delegate complex engineering activities while maintaining consistent standards, evidence-based validation and appropriate governance.

---

## 11. Key Takeaway

Your refactored architecture establishes the following separation:

| Component | Responsibility |
|---|---|
| **User Prompt** | WHAT and WHERE |
| **AGENTS.md** | RULES, STANDARDS and EXPECTATIONS |
| **SKILL.md** | HOW and WHEN |
| **Existing Repository Code** | ESTABLISHED CONVENTIONS |
| **Tool Responses** | EXECUTION EVIDENCE |
| **LLM** | REASONING, DECISIONS and REPORTING |
| **GitHub Copilot Harness** | EXECUTION and CONTEXT MANAGEMENT |
| **GitHub Permissions** | TECHNICAL ENFORCEMENT |

### Final assessment

Your approach has evolved from simply instructing an AI agent to create a GitHub Actions component into a **reusable, governed agentic engineering framework**.

The most significant context-engineering improvement is that you've moved recurring engineering knowledge out of individual prompts and into structured, reusable instructions.

You've also introduced two particularly valuable capabilities:

**Repository-derived context:** The agent discovers and follows your team's existing engineering conventions.

**Evidence-based validation:** The agent must prove that its implementation works by inspecting actual execution results, rather than relying solely on successful GitHub Actions status checks.

Together, these make your context-engineering approach more maintainable, consistent and suitable for increasingly complex AI-delegated engineering tasks.
