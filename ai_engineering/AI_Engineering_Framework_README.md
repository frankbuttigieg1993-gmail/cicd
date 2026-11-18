# AI-Assisted CICD Engineering Framework

> **Handover guide** \| Central CICD repository and consuming
> application repositories\
> **Status:** Exercise 1 HITL execution completed through application
> Ready for Review; final application merge is a separate human
> activity.\
> **Scope:** GitHub Copilot, GitHub Actions, reusable workflows,
> composite actions, semantic releases, and cross-repository promotion.

## 1. Executive summary

This framework uses version-controlled instructions to guide AI-assisted software engineering across a central CICD repository and one or more application repositories. It separates **governance**, **execution procedure**, and **lifecycle orchestration** so an agent can work consistently without requiring every engineering prompt to restate the entire delivery process.

The design was exercised with a new file-listing composite action integrated into the Java application's PR pipeline. The supervised **Exercise 1** reached all seven human-in-the-loop (HITL) checkpoints and promoted the Java application PR to Ready for Review. It did **not** establish that the Java PR was merged or that fully autonomous operation has been validated.

**Operating principle:** `AGENTS.md` defines **what is allowed and required**; `SKILL.md` defines **how to do it**; the canonical workflow defines **when and in what order**.

## 2. Repository architecture and ownership

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Repository                                                                                                    Responsibilities        Key engineering artifacts ------------------------------------------------------------------------------------------------------------- ----------------------- ---------------------------------------------------------------------------------- [`frankbuttigieg1993-gmail/cicd`](https://github.com/frankbuttigieg1993-gmail/cicd)                           Shared GitHub Actions   `AGENTS.md`, `.github/skills/github-actions-development/SKILL.md`,
                                                                                                                reusable workflows,     `.github/Standard CICD Engineering, Release & Application Promotion Workflow.md`
                                                                                                                composite actions,      
                                                                                                                release automation, and 
                                                                                                                central engineering     
                                                                                                                procedure               

[`frankbuttigieg1993-gmail/java_application`](https://github.com/frankbuttigieg1993-gmail/java_application)   Application source,     `AGENTS.md`, `.github/workflows/pr.yml`
                                                                                                                Gradle, tests, and      
                                                                                                                application-side caller 
                                                                                                                workflows               
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Application repositories have their **own** `AGENTS.md` policies. Instructions from another repository are **not automatically inherited**. The shared CICD Skill is used when available in the agent's workspace; do not assume it is accessible from an isolated application workspace.

The central CICD repository uses **one semantic version for the entire repository**, not independent versions for individual actions or reusable workflows. Each consuming application adopts a published CICD version through its own reviewed change. A new CICD release does **not** automatically update unrelated applications.

## 3. The three-layer instruction architecture

### Layer 1 --- `AGENTS.md`: governance and policy

**Question answered: What is permitted and required?**

The CICD and application `AGENTS.md` files establish repository responsibilities, mandatory pipeline selection, scope of authorisation, protected files, minimal-change expectations, PR promotion criteria, review boundaries, evidence requirements, release governance, and handling of known findings.

Examples:

-   Explicitly select **PR Pipeline** or **Build Pipeline** before work
    integrating into an existing pipeline. PR Pipeline selection
    authorises the selected CICD PR workflow and only narrowly necessary
    Java PR caller edits.
-   Preserve unrelated code, workflows, checks, permissions, and
    uncommitted work.
-   Require evidence from actual workflow, job, step, and log
    execution---not only green checkmarks.
-   Do not directly merge PRs, bypass required checks, or alter GitHub
    settings without specific authorisation.
-   Historical merged/closed PRs are evidence, not automatic blockers to
    a new execution.

**Precedence:** Repository-specific `AGENTS.md` governs its own change boundaries. Contradictions with the Skill or lifecycle must be reported rather than silently resolved.

### Layer 2 --- `SKILL.md`: reusable execution procedure

**Question answered: How should the work be performed?**

The central `github-actions-development` Skill provides the technical runbook for discovering conventions, creating and validating actions/workflows, safely managing branches, coordinating Draft PRs, classifying release labels, inspecting logs, handling failures, and performing post-release application adoption.

It includes the **Historical PR and Feature-Branch Reconciliation** procedure: compare local and remote refs/SHAs, identify PRs using repository, head/base refs, current SHA, state, commits, and metadata, distinguish current work from historical records, and avoid destructive fallback actions. Plausibly transient PR-creation failures may receive at most two bounded retries after read-only investigation.

This shared Skill is intended to be reused across multiple application repositories; a duplicate Java-specific Skill is not required.

### Layer 3 --- canonical workflow: lifecycle orchestration

**Question answered: When and in what order?**

The authoritative sequence is:

`.github/Standard CICD Engineering, Release & Application Promotion Workflow.md`

It defines the **16-step** delivery lifecycle, CICD-first merge/release dependencies, application adoption and revalidation, human review gates, and reporting. It is a sequence document, not a replacement for repository policy or the detailed Skill.

### How the layers cooperate

  -----------------------------------------------------------------------
Situation         `AGENTS.md`       `SKILL.md`        Canonical
                                                        workflow
----------------- ----------------- ----------------- ----------------- Historical PR     Says a matching   Compares refs,    Performs shares a branch   name is not proof SHAs, PR          reconciliation name              of current        metadata; safely  before Draft PR
                    execution         handles failures  creation (Step 6)

New CICD          Authorises scoped Specifies         Schedules composite action  work and          metadata, shell,  implementation
                    prohibits         checkout,         and local
                    unrelated changes action-ref and    validation (Steps
                                      validation        3--5)
                                      practices         

CICD release      Requires proper   Verifies merge    Releases only
                    label,            SHA, tag, release after CICD merge
                    merged-commit tag workflow and      (Steps 10--11)
                    and technical     protections       
                    protection                          

Application       Requires          Inspects new PR   Adopts release, promotion         release-based     run and step logs validates, then
                    functional                          requests review
                    evidence and                        (Steps 12--15)
                    human review                        
  -----------------------------------------------------------------------

## 4. Standard 16-step engineering lifecycle

1.  **Requirements Analysis and Pipeline Selection** --- Confirm PR or
    Build Pipeline and authorised scope.
2.  **Repository Convention Discovery and Planning** --- Inspect
    comparable implementations, requirements and acceptance criteria.
3.  **Create CICD Feature Branch** --- Branch from verified `main`;
    implement CICD changes using established conventions.
4.  **Create Application Feature Branch** --- Branch from verified
    `main`; temporarily point the authorised caller to the CICD feature
    branch.
5.  **Perform Local Validation** --- Check YAML, action metadata,
    references, dependencies and functionality.
6.  **Create Both Draft PRs** --- Reconcile historical/current branches
    and PRs; create cross-linked Draft PRs with evidence and
    dependencies.
7.  **Classify the CICD Release and Apply the PR Label** --- Apply
    **exactly one** `release:patch`, `release:minor`, or `release:major`
    label.
8.  **Execute End-to-End Feature-Branch Validation** --- Run the
    application PR pipeline and inspect actual logs.
9.  **Promote CICD PR to Ready for Review** --- Check evidence, stable
    internal references, label and applicable gates; request review.
10. **Review and Merge CICD PR** --- Human approval and authorised
    GitHub merge.
11. **Automatically Create the Semantic-Version Release** --- Tag the
    **actual merged CICD commit**, publish and verify the release.
12. **Update the Application Draft PR** --- Using configured automation
    or an authorised agent operation, replace the temporary CICD ref
    with the published version.
13. **Execute Final Application Validation** --- Trigger a fresh PR run
    against the released CICD revision and inspect logs.
14. **Promote Application PR to Ready for Review** --- Verify gates and
    request designated review.
15. **Final Human Review and Merge** --- Human reviewer evaluates and
    merges through GitHub governance.
16. **Final Reporting and Cleanup** --- Preserve PRs, SHAs, logs and
    release evidence; clean up branches only when authorised and no
    longer referenced.

**Note:** The 16 steps are the standard lifecycle. Exercise 1 grouped activities into **seven HITL checkpoints** for supervised testing. Those checkpoints are not automatically permanent requirements for every execution.

## 5. GitHub Actions reference and release model

### Development-time references

The consuming application's caller may temporarily use the CICD feature branch to validate unreleased functionality:

``` yaml
uses: frankbuttigieg1993-gmail/cicd/.github/workflows/java-build-pr.yml@feature/ai-generated-list-files
```

Inside the CICD reusable workflow, the validated self-repository action syntax is:

``` yaml
uses: $/.github/actions/ai-generated-list-files
```

This avoids a hard-coded internal action feature branch and allows the action to follow the reusable workflow's CICD revision in the tested setup. Verify the syntax and resolution in the actual execution environment; do not assume ordinary `./.github/actions/...` resolves to CICD when the application repository is checked out.

### Release-time references

After CICD review and merge, release automation creates the next semantic version on the **actual merged commit** (works with merge commit, squash or rebase when correctly implemented). The application then adopts that published release:

``` yaml
uses: frankbuttigieg1993-gmail/cicd/.github/workflows/java-build-pr.yml@v2.2.0
```

**Immutability:** Published version tags must not be moved, reused or deleted. Enforce protection using GitHub rulesets or equivalent controls. Native GitHub Release immutability and tag-reference protection are distinct: a previously published release may still show `immutable: false` even when its tag is protected against updates and deletion.

**Release labels:** `release:patch` = compatible fix; `release:minor` = compatible feature; `release:major` = breaking change. The agent must inspect the diff, apply exactly one appropriate label to the CICD PR, and verify it was recorded. Do not assume release automation will infer it.

## 6. Validation, governance and human responsibilities

**Functional evidence required:** Record the current head SHA, run URL/ID, workflow/job/step execution, actual log excerpts, and expected-versus-observed results. A green check does not prove the requested feature executed.

**Separate gates:** CICD Ready for Review, CICD merged/released, application release adopted/validated, application Ready for Review, and application merged are distinct states. Never describe one as proof of another.

**Human and platform controls:** The agent can prepare branches, PRs and authorised changes, but cannot directly approve or merge PRs under this policy. GitHub permissions, required checks, rulesets and release protection provide technical enforcement; Markdown instructions provide behavioural guidance.

**Designated reviewer:** `frankbuttigieg93-png` where GitHub permits. A review request is not an approval. If GitHub rejects the request, report it without impersonation or substitution.

**Known findings:** Record accepted, pre-existing security/test findings separately from task-related regressions. Acknowledgement does not automatically waive required checks, and checks must not be weakened to make CI appear green.

**Handover owner actions:** Ensure the next operator has access to both repositories, the correct GitHub account and reviewer, the shared Skill, the canonical lifecycle, the release workflow, and the relevant GitHub rulesets. Confirm which operations require explicit approval before beginning.

## 7. Exercise 1 --- supervised validation case study

**Objective:** Add a composite action to list direct entries in the Java repository root, including hidden files, as a PR-only job after successful Build.

  -----------------------------------------------------------------------------------------------------------------------------------------
Milestone                           Observed outcome ----------------------------------- ----------------------------------------------------------------------------------------------------- CICD implementation                 New `ai-generated-list-files` composite action and `List_Files` job

Application integration             Java caller temporarily used CICD feature branch

Initial integration                 Build and listing executed; actual logs were inspected

CICD PR                             [PR #7](https://github.com/frankbuttigieg1993-gmail/cicd/pull/7) merged

CICD release                        `v2.2.0` created on merge SHA `1c0e8e3021c35de606b0df685d5fdd6374c66b78`

Release governance                  Tag ruleset enabled to block updates/deletions; native immutability enabled for future releases

Application PR                      [PR #52](https://github.com/frankbuttigieg1993-gmail/java_application/pull/52) adopted `@v2.2.0`,
                                      reached Ready for Review

Released-version validation         [Java PR run
                                      44016664579](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44016664579)
                                      verified listing after Build

Final state observed                All seven supervised checkpoints completed; application PR remained open/unmerged at last recorded
                                      checkpoint
  -----------------------------------------------------------------------------------------------------------------------------------------

The listing logs contained all **37 tracked root entries**, including hidden `.github` and `.gitignore`. Some runtime/checkout entries also appeared.

**Known, documented limitations:** The Unit Tests check reported success despite intentional pre-existing underlying test failures; CodeQL reported known findings; GitHub reported aggregate merge state `UNSTABLE` at final review. These were documented, not silently treated as fully clean results. Final merge readiness remained subject to GitHub governance and human review.

### Lessons incorporated into the framework

-   **Historical PR ambiguity:** Earlier PRs with the same task/branch
    name caused confusion. The updated Skill and policies require
    current branch/PR identity reconciliation rather than relying on
    names.
-   **Reviewer typo:** Correcting the configured reviewer and
    re-evaluating allowed the review request to be recorded.
-   **Release protection:** Copilot detected that a published tag was
    not technically protected; the team added tag ruleset protection and
    re-ran verification.
-   **Status versus evidence:** Logs exposed test failures beneath a
    green check, demonstrating why log-level verification is mandatory.
-   **Reference strategy:** Self-repository composite action references
    plus CICD semantic releases eliminated permanent temporary
    feature-branch dependencies.

**What this proves:** The supervised two-repository lifecycle was exercised through application review handoff. It does **not** yet establish fully autonomous execution or reliable operation across five or ten application repositories; those require further testing.

## 7A. Exercise 1 — autonomous execution validation case study

The No-HITL repetition used the same functional requirement with **zero additional exercise-specific approval checkpoints**. Mandatory human CICD and Java PR reviews/merges remained in force. The refined instruction baseline and release protection differed from the earlier HITL run.

| Milestone | Observed outcome |
|---|---|
| Preliminary read-only context verification | Passed; Copilot identified governance, Skill and canonical lifecycle |
| Implementation and integration | New action and separate post-Build `List_Files` job; coordinated PRs |
| CICD review and release | [CICD PR #8](https://github.com/frankbuttigieg1993-gmail/cicd/pull/8) merged; published immutable `v3.1.0` |
| Release discovery and adoption | Copilot independently selected published `v3.1.0`, updating existing [Java PR #58](https://github.com/frankbuttigieg1993-gmail/java_application/pull/58) |
| Released-version validation | [Java run 44217333120](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44217333120) inspected actual listing results |
| Final governance boundary | Java PR #58 promoted for human review and subsequently merged by a human |
| Final read-only verification | Reported `COMPLETE — ENGINEERING LIFECYCLE VERIFIED` |

**Final commits:** CICD `e7ecad9de8694095e2ea99d1f3ce77d23fc4b5b7`; Java `864bf2e8152be77ec596dcce1a9dafc77a1ad86d`. Final application caller: `@v3.1.0`. The temporary feature-branch reference was absent from the affected production caller.

**Observed autonomy:** Copilot reconciled historical PR context, resumed after the CICD human merge, discovered the immutable release, revalidated against the release and stopped at the application review boundary without exercise-specific approval interruptions. Underlying Gradle test failures and Java CodeQL findings were documented rather than concealed or remediated within the listing task.

**Interpretation:** This validates one end-to-end scenario with the **refined** framework; it does not demonstrate that removing checkpoints alone caused improvements, nor establish general reliability for other tasks. See [No-HITL results](Exercise%201%20-%20No%20HITL/RESULTS.md) and [final comparison](Exercise_1_Comparison.md).

## 8. Practical handover and onboarding checklist

Before a new task, the operator should:

1.  Open the appropriate multi-root workspace and verify access to both
    repositories.
2.  Read the **latest** CICD `AGENTS.md`, application `AGENTS.md`,
    shared `SKILL.md`, and canonical workflow; do not rely only on chat
    summaries.
3.  Confirm the selected pipeline (**PR** or **Build**) and the exact
    requested change.
4.  Check branch/worktree status and preserve unrelated modifications.
5.  Confirm existing release baseline, semantic release workflow, tag
    ruleset and release immutability settings.
6.  Confirm the reviewer identity and the applicable GitHub
    rulesets/required checks.
7.  Check current branches and open/closed/merged PRs using refs and
    SHAs---not branch names alone.
8.  Agree on HITL checkpoints or other task-specific approvals; do not
    assume the previous exercise's checkpoint structure applies.
9.  Require actual logs and expected-versus-observed evidence at
    validation gates.
10. Retain PR links, commit SHAs, release tag, workflow runs, exceptions
    and final handoff notes.

### Minimum information for a new engineering request

Provide the **target application repository**, **PR or Build Pipeline selection**, desired behaviour, acceptance criteria, and any task-specific constraints. The agent should discover existing conventions and apply the established lifecycle rather than requiring the full procedure to be pasted into each prompt.

## 9. Change management and ownership

  -----------------------------------------------------------------------
Artifact                Change when...          Review emphasis ----------------------- ----------------------- ----------------------- CICD `AGENTS.md`        Shared governance or    Safety, permissions,
                          authorisation policy    release/PR rules
                          changes                 

Application `AGENTS.md` Application-specific    Local ownership and
                          policy or caller        standalone clarity
                          boundaries change       

Shared `SKILL.md`       Reusable operational    Accuracy,
                          technique or            reproducibility, no
                          troubleshooting         duplicated policy
                          procedure improves      

Canonical workflow      Lifecycle ordering,     Sequencing, approval
                          dependencies or         gates, consistency
                          handoffs change         

GitHub rulesets /       Technical enforcement   Explicit approval, release automation      or release mechanics    tested controls and
                          change                  rollback
  -----------------------------------------------------------------------

Review the four documents together when changing cross-cutting behaviour, but avoid duplicating detailed procedures. Update the **single authoritative location** and use concise references elsewhere. Treat documentation changes as version-controlled engineering changes, not as an implicit grant to modify repository settings or protected branches.

## 10. Open questions and future validation

-   Extend historical-PR reconciliation testing beyond the successfully observed No-HITL scenario.
-   Repeat autonomous execution with other tasks and repositories while preserving explicit authorisation and merge governance.
-   Validate the architecture with additional application repositories
    and independent release adoption.
-   Continue verifying release immutability on future CICD releases; `v3.1.0` was published and observed immutable.
-   Decide whether the intentionally green Unit Tests check and known
    security findings need separate governance remediation; they were
    explicitly outside Exercise 1's feature scope.
-   Establish long-term owners for the Skill, policy documents, release
    workflow and evidence retention.

## 11. Source-of-truth and useful links

**Read the actual files before acting.** This README is a handover guide, not the authoritative instruction source.

-   **CICD policy:** `cicd/AGENTS.md`
-   **Application policy:** `java_application/AGENTS.md`
-   **Central execution runbook:**
    `cicd/.github/skills/github-actions-development/SKILL.md`
-   **Canonical lifecycle:**
    `cicd/.github/Standard CICD Engineering, Release & Application Promotion Workflow.md`
-   **CICD PR:** https://github.com/frankbuttigieg1993-gmail/cicd/pull/7
-   **Application PR:**
    https://github.com/frankbuttigieg1993-gmail/java_application/pull/52
-   **Release:**
    https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v2.2.0
-   **CICD release workflow run:**
    https://github.com/frankbuttigieg1993-gmail/cicd/actions/runs/44014320065
-   **Application release-validation run:**
    https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44016664579

------------------------------------------------------------------------

**Framework summary:** A three-layer, repository-driven AI engineering framework separating **governance (`AGENTS.md`)**, **execution procedure (`SKILL.md`)**, and **lifecycle orchestration (canonical workflow)** to support consistent, auditable, human-governed delivery across a central CICD repository and its application consumers.

**Additional evidence:** [Experiment index](EXPERIMENT_INDEX.md) · [Evidence index](EVIDENCE_INDEX.md) · [Final comparison](Exercise_1_Comparison.md).
