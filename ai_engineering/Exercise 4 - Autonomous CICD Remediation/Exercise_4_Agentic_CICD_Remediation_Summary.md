# Exercise 4 — Agentic CI/CD Remediation

> **Status:** Technical remediation complete; CICD PR #9 merged and released as `v3.1.1`; Java Application PR #59 ready for human review but not yet merged in the supplied evidence.  
> **Evidence:** GitHub Copilot execution screenshots, PR descriptions, GitHub Actions run summaries, and *Exercise_4_Final_Engineering_Assessment.md*.  
> **Evidence note:** This is a retrospective account of the supplied evidence, not an independent rerun of the repositories or workflows.

## 1. Executive summary

Exercise 4 tested whether **GitHub Copilot Agent Mode could autonomously diagnose and remediate an unfamiliar CI/CD failure** using the context-engineering framework developed during Exercise 1, **without creating a new Skill or changing the existing governance documents**. Two defects were in scope: (1) failing Java unit tests and (2) a GitHub Actions PR Pipeline that could report success despite failed Gradle tests.

Copilot independently reproduced **five tests with three failures**, identified interacting Spring/Jackson dependency, controller, and test-context problems, and implemented Java corrections. It also changed the shared CICD Java test composite action to enforce Gradle and JUnit results after publishing reports. Local tests and failure-gate checks succeeded. A live PR run demonstrated a failing Gradle outcome propagating to a failed Unit Tests job; a subsequent same-SHA rerun passed. CICD PR **#9** was merged by the human operator, and the immutable release **`v3.1.1`** was published. Java PR **#59** adopted the release and its fresh PR Pipeline run **`44692544023`** passed with **five tests passed, zero failed, zero skipped**.

**Result:** Both targeted technical defects were addressed, and the existing framework supported autonomous remediation across repositories. The broader lifecycle was **not fully closed** in the supplied evidence: Java PR #59 remained open for human review, and the separate Java CodeQL policy check remained unsuccessful.

## 2. Objectives and evaluation questions

**Primary objective:** Diagnose and fix the existing Java unit-test failures and ensure genuine test/Gradle failures cause a failed GitHub Actions PR check.

**Secondary objective:** Test whether the existing `AGENTS.md`, shared `SKILL.md`, and canonical engineering lifecycle can govern a **single autonomous remediation execution** without additional exercise-specific checkpoints.

Success required fresh baseline evidence, confirmed root causes, a real passing test suite, correct failure propagation, minimal authorised changes, cross-repository PR/release discipline, and preservation of mandatory human approvals and security controls.

## 3. Architecture and execution locations

| Component | Execution location | Role in Exercise 4 |
|---|---|---|
| Human operator | Local workstation / GitHub | Defined scope, selected the PR Pipeline, authorised creation of `release:patch`, manually promoted the CICD PR to review, and merged CICD PR #9. Retained Java review/merge responsibility. |
| VS Code and GitHub Copilot Chat | Local workstation with connected services | Interface for the execution prompt, commands, progress and reports. |
| Copilot AI agent and harness | VS Code integration plus supporting remote services | Iterative investigation, code edits, Git operations, tool execution, workflow monitoring and evidence reporting. |
| LLM accessed through Copilot | Remote model infrastructure | Interpreted the objective and tool results, formed hypotheses and guided remediation. Exact model/runtime distribution not independently verified. |
| Local Git/Gradle worktrees | Local Windows workstation | Isolated baseline reproduction, implementation and test/negative-gate validation. |
| `cicd` repository | Local Git worktree and GitHub | Owned reusable PR workflow and Java test composite action; published the versioned fix. |
| `java_application` repository | Local Git worktree and GitHub | Owned application code, tests, dependency configuration and PR workflow caller. |
| GitHub Actions | GitHub-hosted execution environment | Ran PR Pipeline jobs and reported Build, List Files and Unit Tests outcomes. |
| GitHub PRs, release automation and rulesets | GitHub | Coordinated review, immutable release publication and technical governance. |

**Architecture classification:** A GitHub Copilot–driven, tool-using autonomous engineering workflow across local development tooling and GitHub CI/CD. **Unlike Exercises 2 and 3, no MCP server is established as a required component of this exercise.**

## 4. Scenarios, investigation and remediation

| Workstream | Initial evidence | Confirmed finding reported by Copilot | Remediation |
|---|---|---|---|
| Java test baseline | Current Java `main`: **5 tests, 3 failed** | Spring Beans **5.3.17** conflicted with Spring Boot-managed Spring Framework **6.2.18** | Align Spring dependencies with Boot-managed versions. |
| Additional class-loading issue | Runtime/test reports after initial investigation | Jackson Databind **2.13.0** conflicted with managed Jackson modules **2.21.2** | Align Jackson dependencies. |
| Application context | Full-context tests | Duplicate `/health` controller/bean definitions | Remove duplicate controller; update affected test. |
| Test-only dependency | Full-context test failure | Missing `DataSource` for intentionally vulnerable CodeQL demonstration fixture | Supply test-only mocked `DataSource`; preserve fixture and scans. |
| CI failure propagation | Historical Gradle failure and 3 failed tests while Unit Tests check was green | Composite action did not reliably enforce Gradle/JUnit failures after reporting | Read JUnit XML and enforce Gradle outcome, test counts, failed tests, missing reports and coverage outcomes. |

The agent treated initial clues as hypotheses, inspected actual Gradle/JUnit evidence, and revised its diagnosis as additional failures became visible. It did **not** merely disable tests or remove the security demonstration fixture to obtain a green build.

## 5. Validation and observed results

| Stage / evidence | Result | Interpretation |
|---|---|---|
| Fresh Java baseline | **5 tests, 3 failed** | Confirmed the problem existed on the current baseline. |
| Local corrected suite | **5 passed, 0 failed, 0 skipped** | Supports functional remediation. |
| Local failure-gate cases | Passing, failed JUnit, Gradle failure, coverage failure and missing-report cases checked | Supports correct gate logic in controlled local conditions. |
| Java PR run `44688537032`, first attempt | Unit Tests job **failed** when Gradle could not resolve buildscript artifacts; no tests ran | Demonstrates a real Gradle failure now fails the hosted job; **not** a hosted deliberately failing-JUnit test. |
| Same-SHA rerun, attempt 2 | Build, List Files and Unit Tests **passed**; 5/5 tests passed | Consistent with a transient dependency-resolution failure on the first attempt; precise infrastructure cause not proven. |
| CICD PR #9 and release | Human merge; immutable **`v3.1.1`** | Published the corrected reusable action through release automation. |
| Java caller update | `java-build-pr.yml@v3.1.1` | Replaced temporary CICD feature-branch reference with published tag. |
| Released-version Java PR run `44692544023` | **Success**; Bootstrap, Build, List Files and Unit Tests passed; **5 passed, 0 failed, 0 skipped** | Strong end-to-end evidence for the corrected Java code and released CICD workflow together. |

The negative-test claim has a boundary: **local** simulated failed-JUnit cases were reported, while the **hosted** failure evidence was an actual Gradle dependency-resolution failure. The supplied screenshots do not establish an intentionally injected failing JUnit test traversing the entire hosted pipeline.

## 6. Repository changes and release lifecycle

| Repository | PR | Change | Outcome in supplied evidence |
|---|---|---|---|
| `frankbuttigieg1993-gmail/cicd` | **#9 — `java: propagate unit test failures`** | `.github/actions/java/test/action.yml` enforced test and Gradle outcomes | **Merged by human**; merge SHA `c5d891c47249ef6bfa4810b1e30269b5eb61b3dc`; immutable release **`v3.1.1`** published. |
| `frankbuttigieg1993-gmail/java_application` | **#59 — `java: repair unit test configuration`** | `build.gradle`, `gradle.lockfile`, relevant Java tests, removal of duplicate controller, and PR caller update to `@v3.1.1` | **Ready for Review, open and unmerged** in final supplied report. |

The workflow followed the CICD-first dependency: validate coordinated feature branches, obtain human CICD approval/merge, publish the immutable release, update the Java caller, and revalidate against the release. The Java PR was not merged by Copilot.

## 7. Agent governance and human intervention

| Framework layer | Responsibility | Observed application |
|---|---|---|
| **`AGENTS.md` — WHAT is permitted** | Authorisation, restrictions, repository ownership and mandatory human boundaries | PR Pipeline explicitly selected; unrelated workflows, IAM, security settings and governance files left outside scope. |
| **`SKILL.md` — HOW to execute** | Reusable investigation, implementation, validation and PR procedures | Guided baseline checks, isolated worktrees, cross-repository changes, log inspection and evidence. |
| **Canonical lifecycle — WHEN / in what order** | Sequence of branch, PR, release, adoption and review activities | CICD review/merge and immutable release preceded final Java adoption/validation. |
| **GitHub technical controls** | Rulesets, checks, reviews and release automation | Human CICD merge retained; a Java required-status-check protection concern was reported for follow-up. |

**Recorded human involvement:** (1) authorisation to create/apply the missing `release:patch` label, (2) manual promotion of CICD PR #9 to Ready for Review because of an unrelated issue, and (3) mandatory human merge of CICD PR #9. This was **high autonomy with explicit governance boundaries**, not literally zero human intervention.

## 8. Outstanding findings and limitations

**Java CodeQL:** The remediation-branch scan reported **2 findings and failed its policy step**; a baseline `main` scan reported **8 findings and also failed**. Exact alert overlap was not established. It would be incorrect to claim that six security findings were fixed. Dependency Review and Semgrep passed, and no security policy or fixture was weakened. The CodeQL result remained unresolved.

**Java branch protection:** Copilot's final report noted that the active Java `main` ruleset appeared not to include a required-status-check rule, although an earlier version reportedly included `code_quality`. This is a **reported governance concern requiring independent verification**, not a finding that the agent changed protections.

**Lifecycle status:** Java PR #59 remained open and unmerged in the final supplied report. A passing PR Pipeline does not itself establish that all mandatory security/governance requirements were met.

**Generalisability:** One remediation exercise is evidence that the framework worked in this case; it is not proof that it will diagnose every CI/CD failure. The screenshots and agent report were reviewed retrospectively rather than independently replayed.

## 9. Findings and interpretation

**Root-cause capability:** Copilot investigated multiple interacting causes and used execution evidence rather than accepting the first hypothesis.

**Engineering correctness:** The supplied evidence shows the Java tests moving from **3 failures out of 5** to **5 passes out of 5**, and the corrected reusable workflow being exercised successfully from its immutable release.

**Failure integrity:** The new gate distinguished successful execution from failed Gradle outcomes, while retaining report publication. Local negative cases support the intended JUnit and coverage enforcement.

**Framework reuse:** The same `AGENTS.md` / `SKILL.md` / canonical lifecycle structure developed in Exercise 1 supported a new class of task—autonomous diagnosis and remediation—**without a new Skill**.

**Governance:** The agent stopped or requested authorisation at repository-metadata and mandatory PR boundaries, rather than treating full autonomy as permission to override them.

## 10. Final executive assessment

> **Exercise 4 — TECHNICAL OBJECTIVES ACHIEVED; FINAL JAVA GOVERNANCE PENDING.** GitHub Copilot independently reproduced and investigated the failing Java tests, implemented application and CI/CD corrections, validated passing tests and failure propagation, and coordinated the CICD patch release **`v3.1.1`** and Java adoption. The final released-workflow PR run passed **5 tests with zero failures**. This is strong case-specific evidence that the existing context-engineering framework generalises from feature implementation to autonomous remediation. Human review/merge boundaries were preserved; Java PR #59 and the unrelated CodeQL policy failure remained open in the supplied evidence.

## 11. Evidence references

- CICD PR: https://github.com/frankbuttigieg1993-gmail/cicd/pull/9
- Java PR: https://github.com/frankbuttigieg1993-gmail/java_application/pull/59
- Initial / rerun Java PR validation: https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44688537032
- Released-version Java PR validation: https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44692544023
- Detailed companion assessment: `Exercise_4_Final_Engineering_Assessment.md`

These links identify evidence referenced in the supplied screenshots and reports; this summary does not claim a fresh live verification of their present status.
