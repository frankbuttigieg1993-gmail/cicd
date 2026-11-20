# Exercise 1 — HITL: Full Historical Execution Review

> **Historical evidence report.** The executive summary and analytical narrative are newly written. Original Copilot text is preserved in the accompanying unabridged transcript. Original ChatGPT assessments visible in OneNote are preserved **as images** in the evidence section; they have not been silently paraphrased and called verbatim. The original complete ChatGPT message history is not fully recoverable from the partial HTML export.

## 1. Executive Summary

**Overall result: PASS — HITL engineering lifecycle completed through final application PR promotion, with mandatory human merge boundaries preserved.** This describes the observed state at the end of the exported Copilot session; it does **not** mean the Java application PR was merged.

The experiment asked GitHub Copilot to implement the reusable `ai-generated-list-files` composite action in the CICD repository, integrate it into the Java Application PR Pipeline after Build, and demonstrate end-to-end cross-repository validation. Execution was deliberately gated by **seven exercise-specific human-in-the-loop checkpoints**. The CICD PR was reviewed and merged by a human, producing CICD release **`v2.2.0`**. The Java Application PR adopted `@v2.2.0`, was validated again, and ultimately reached **Ready for Review**, with reviewer requested, while remaining unmerged.

Key issues encountered included historical pull requests being confused with newly created branches, an incorrect reviewer identifier in governance documentation, an initially non-immutable release, and a Java PR promotion blocker associated with required checks and repository rules. These were investigated and addressed during the HITL exercise. The pre-existing test-result discrepancy and CodeQL findings were documented rather than silently treated as passing tests or fixed outside scope.

| Field | Historical outcome |
|---|---|
| Execution model | Seven explicit HITL checkpoints, plus mandatory repository governance |
| Copilot source record | 14 exported conversation turns, including follow-up re-evaluations |
| CICD PR | **#7**, reviewed and human-merged |
| Historical CICD PR | **#6**, from earlier execution, not current PR |
| Java Application PR | **#52**, Ready for Review and unmerged at transcript end |
| Historical Java PR | **#51**, from earlier execution |
| CICD release | **`v2.2.0`** |
| Java caller adoption | **`@v2.2.0`** |
| Functional validation | Java PR Pipeline's List Files job executed; log evidence inspected |
| Human governance | Merge remained human-controlled; release and PR readiness were checked |
| Important qualification | A CodeQL workflow failed even though a separate CodeQL check context passed; final PR `mergeStateStatus` remained `UNSTABLE` |

### Evidence provenance and fidelity

The **Copilot Markdown transcript** is the authoritative chronological record of the Copilot-visible prompts, replies, and tool outputs. The **OneNote PDF** is a contemporaneous human record with screenshots, notes, and captured ChatGPT commentary. The screenshots below reproduce each **entire OneNote PDF page** (rather than cropping or inventing individual screenshots) so the historical context and any embedded ChatGPT wording remain intact. The HTML export was only a virtualized fragment of later No-HITL messages and cannot independently supply earlier ChatGPT assessments.

---

## 2. Full Historical Assessment — Evidence-Grounded Reconstruction

**Important distinction:** This section is a *new historical assessment*, not a verbatim reproduction of ChatGPT messages that are absent from the accessible conversation context. For verified original ChatGPT assessment screenshots, see the end-of-document evidence pages, particularly OneNote pages 13–15, 18 and 22–23. For **verbatim Copilot** activity, consult `GitHub_Copilot_HITL_Original_Transcript.md`, included alongside this report.

### Context verification (before implementation)

Copilot was instructed to independently discover both repositories' `AGENTS.md` instructions, the shared `SKILL.md`, and the canonical engineering workflow, and to report its understanding without changing code or triggering workflows. This established the intended separation between repository governance, procedural execution instructions, and lifecycle orchestration. **Assessment: the read-only context verification formed the baseline for the subsequent authorised work.** See transcript Turn 1 and OneNote pages 7–9.

### Checkpoint 1 — Planning

Copilot received the HITL engineering objective and was required to plan implementation and identify scope before proceeding. The intended change was a new composite action, an update to the CICD reusable PR workflow, and an update to the Java Application PR caller. The user explicitly approved the plan before Checkpoint 2. **Assessment: checkpoint-based planning and human authorisation were observed.** See transcript Turns 2–3 and OneNote pages 9–10.

### Checkpoint 2 — Implementation

Copilot implemented the approved change in the two repositories, keeping the action and reusable workflow under CICD ownership and the caller integration under Java ownership. It used the established repository conventions, including a self-repository action reference in the reusable workflow. The user observed that branches existed locally at this stage rather than on GitHub. **Assessment: the implementation progressed within the approved three-file engineering scope before the next handoff.** See transcript Turn 3 and OneNote pages 10–11.

### Checkpoint 3 — Draft PRs and Integration Validation

Copilot was authorised to commit and push the feature branches, create cross-linked Draft PRs, classify the release and inspect feature-branch validation. A complication arose because CICD PR #6 and Java PR #51 belonged to a previous execution, although the newly created branches reused their names. The user clarified that the current branch instances contained new commits and that old PRs were historical. Copilot reassessed branch/PR identity rather than treating the old PRs as current or automatically replacing the new branches. New CICD PR #7 and Java PR #52 were used for this execution. **Assessment: feature validation and PR creation were completed, but historical PR reconciliation required an extra human clarification.** See transcript Turns 4–5 and OneNote pages 11–16.

### Checkpoint 4 — CICD PR Promotion

The user authorised promotion only after checking required repository controls, while keeping the Java PR in Draft. Copilot encountered a reviewer-identity inconsistency in `AGENTS.md` and `SKILL.md`. The governance files were corrected outside the operational implementation, and Copilot was asked to re-evaluate. The correct reviewer was then requested, and CICD PR #7 was prepared for human review. **Assessment: the agent respected the promotion boundary, but reviewer documentation needed correction.** See transcript Turns 6–8 and OneNote pages 16–18.

### Checkpoint 5 — CICD Release Verification

After the human merged CICD PR #7, Copilot checked the semantic release. Release **`v2.2.0`** existed, but the GitHub release API initially reported `immutable: false`, so Copilot blocked further application adoption. The user enabled release immutability and applied the tag-protection ruleset, then requested re-evaluation. The exercise subsequently proceeded with Checkpoint 5 approved. **Assessment: the agent identified a genuine release-governance issue and did not silently proceed.** Note that tag rulesets and the release API's immutable property are distinct protections; the report preserves what the transcript showed at each re-evaluation rather than assuming a setting change retroactively altered the earlier API response. See transcript Turns 9–11 and OneNote pages 19–20.

### Checkpoint 6 — Application Release Adoption and Validation

Following approval, Copilot replaced the temporary CICD feature-branch reference in Java PR #52 with the published version **`@v2.2.0`** and ran fresh PR validation. It checked the actual List Files job output, rather than treating an overall workflow success badge as sufficient. It also identified that a Unit Tests check could report success despite failures in the underlying Gradle tests; the user explained this was deliberate, pre-existing behaviour. CodeQL findings were likewise recorded as pre-existing and outside this exercise's scope. **Assessment: release adoption and functional evidence were demonstrated, with test/security qualifications explicitly retained.** See transcript Turn 12 and OneNote pages 21–23.

### Checkpoint 7 — Final Application Promotion

The user authorised Copilot to verify the Java PR's governance readiness and promote it if compliant, without merging. The first attempt encountered a required-check/ruleset blocker. Following a further re-evaluation, the active ruleset required `CI / Build` and `CI / Unit_Tests`, both reported successful for the current PR head. Copilot marked Java PR #52 **Ready for Review** and requested the designated reviewer. Its final state remained **OPEN, not Draft, unmerged**, and `mergeStateStatus` was **`UNSTABLE`**; the separate CodeQL workflow continued to show a failure. **Assessment: the defined PR-promotion action was achieved, but this should not be described as a clean, all-checks-green application merge.** See transcript Turns 13–14 and OneNote pages 24–25.

---

## 3. Technical and Governance Observations

| Topic | Observation | Significance |
|---|---|---|
| Three-layer context model | Repository `AGENTS.md` governance, central `SKILL.md` procedure, canonical 16-step lifecycle | Gave Copilot a reusable process rather than an ad hoc coding prompt |
| Cross-repository ownership | CICD action and reusable workflow; Java application caller | Prevented mixing implementation ownership |
| Historical PR confusion | Previous PRs #6/#51 were mistaken for current execution | Led to explicit identity-reconciliation guidance in later framework revisions |
| Reviewer identity | Wrong login in instructions caused review-request issues | Demonstrated why exact reviewer identifiers matter |
| Immutable release | Published `v2.2.0` was initially reported non-immutable | Demonstrated the value of a release verification gate |
| Test result interpretation | Green job status did not prove Gradle tests all passed | Motivated inspection of underlying command logs |
| Security findings | CodeQL workflow failure remained visible | Known findings must not be confused with automatically approved exceptions |
| Final application boundary | PR #52 Ready for Review, not merged | Preserved human ownership of the final merge |

### Original human notes versus formal lifecycle

The OneNote summary (pages 26–28) suggests that application adoption and final PR promotion might be optional when the Java PR exists only to test the reusable workflow. This is preserved as the author's historical observation, **not** silently substituted for the mandatory 16-step lifecycle used during the experiment. For this HITL execution, the Java adoption and Ready-for-Review steps **were performed**.

### Comparison with No-HITL (limited, not controlled)

The HITL run required seven explicit exercise checkpoints and additional re-evaluation messages. The subsequent No-HITL run reached the CICD review boundary without exercise-specific checkpoints, but used a revised instruction baseline and started from a different release. These results demonstrate a difference in observed human interruption, **not** a controlled measurement of the causal effect of removing HITL alone.

---

## 4. Verbatim Copilot User Prompts (from the Original Transcript)

The following are the **exact user instructions** as recorded in the Copilot Markdown export, preserving the original words. The full unabridged Copilot responses and tool outputs are retained in the accompanying `GitHub_Copilot_HITL_Original_Transcript.md` rather than being shortened and mislabeled verbatim.


### Copilot Turn 1 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 1.


```text
Exercise 1 — Context Verification

Before beginning
implementation, locate and read the applicable AGENTS.md, SKILL.md and
supporting engineering documentation across the CICD and Java Application
repositories.

Using only the
instructions discovered in those files, provide a concise summary of:

1. The responsibilities of each
     repository.
2. The applicable engineering
     standards and implementation conventions.
3. The authorisation
     requirements and change restrictions.
4. The standard end-to-end
     engineering lifecycle.
5. The validation,
     release-management and completion requirements.
6. Any conflicting, ambiguous or
     missing instructions.

Identify the files
you accessed and explain how they relate to one another.

Do not assume that
instructions from another repository have been automatically loaded.

This is a read-only verification task. Do not
create branches, modify files, execute implementation commands, create PRs or
trigger pipelines.

If the required
context is available and consistent, report:

STATUS: CONTEXT VERIFIED — READY FOR EXERCISE 1

Otherwise, report:

STATUS: BLOCKED — AWAITING USER INPUT

Stop after providing
your findings.
```


### Copilot Turn 2 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 2.


```text
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
```


### Copilot Turn 3 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 3.


```text
Checkpoint 1 is approved.

Proceed with Checkpoint 2 — Implementation, following the applicable engineering instructions and the approved implementation plan.

Respect the established HITL execution boundaries.

Stop at Checkpoint 2 and present the required implementation evidence before proceeding further.
```


### Copilot Turn 4 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 4.


```text
Checkpoint 2 is approved.

Proceed with Checkpoint 3 — Draft PRs and Integration Validation, following the applicable engineering instructions and approved implementation.

Respect the established HITL execution boundaries.

Stop at Checkpoint 3 and present the required PR details, release classification, execution evidence and validation results before proceeding further.
```


### Copilot Turn 5 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 5.


```text
The `feature/ai-generated-list-files` branches in both repositories were created during this execution and did not exist before Exercise 1 began.

CICD PR #6 and Java Application PR #51 belong to the previous execution. Their original feature branches were deleted.

Please reassess the situation using the current GitHub branch and pull-request state.

Specifically:

1. Verify that the current feature branches contain the new commits created during Checkpoint 3.
2. Confirm that the historical PRs are not associated with the current branch instances or commits.
3. Determine whether GitHub permits creating new Draft PRs from the current feature branches despite their names having been used previously.
4. Preserve the current branches, commits and implementation.
5. Do not create replacement branches unless GitHub actually prevents creating new PRs from the existing branches.
If the existing branches can be used, continue with the authorised Checkpoint 3 activities, including Draft PR creation, release classification and integration validation.

Preserve the previous PRs as historical evidence.

Respect the existing HITL boundaries and stop at the end of Checkpoint 3.

If GitHub prevents PR creation, report the exact error and proposed remediation before making further changes.
```


### Copilot Turn 6 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 6.


```text
Checkpoint 3 is approved.

Proceed with Checkpoint 4 — CICD PR Promotion, following the applicable engineering instructions and established HITL boundaries.

The existing Java CodeQL findings are known and outside the scope of this exercise. Do not modify unrelated application code or weaken security controls to address them.

Before promoting the CICD PR, verify the applicable repository governance requirements, including required checks and review requirements.

If the CICD PR satisfies its promotion requirements, mark it Ready for Review and request the required review.

Keep the Java Application PR in Draft status.

Do not merge either PR or initiate release activities.

Stop at Checkpoint 4 and report the PR status, review-request results, supporting evidence and any outstanding governance limitations.
```


### Copilot Turn 7 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 7.


```text
I just updated AGENTS.md and SKILLs.MD, Please re-evaluate
```


### Copilot Turn 8 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 8.


```text
Sorry there was a typo in the files. Please re-evaluate
```


### Copilot Turn 9 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 9.


```text
CICD PR #7 has been reviewed and merged through the authorised GitHub process.

Resume at Checkpoint 5 — CICD Release Verification.

Retrieve the current GitHub state and verify that the CICD merge and semantic-version release completed successfully.

Follow the applicable engineering instructions and existing HITL boundaries.

Present the release details and supporting evidence.

Stop at Checkpoint 5 before modifying the Java Application PR.

Report the required execution status.
```


### Copilot Turn 10 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 10.


```text
please re-evaluate
```


### Copilot Turn 11 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 11.


```text
re-evaluate
```


### Copilot Turn 12 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 12.


```text
Checkpoint 5 is approved.

Proceed with Checkpoint 6 — Application Release Adoption and Validation, following the applicable engineering instructions and established HITL boundaries.

Stop at Checkpoint 6 and present the required application release-adoption evidence, validation results and any outstanding findings before proceeding further.

Do not promote or merge the Java Application PR.
```


### Copilot Turn 13 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 13.


```text
Checkpoint 6 is approved.

The Unit Tests job's successful status despite underlying test failures is intentional, pre-existing behaviour that I have configured. It is known and outside the scope of this exercise.

The previously identified CodeQL findings are also known and outside the scope of this exercise.

Document these findings accurately, but do not modify unrelated application code, tests, workflows or security controls.

Proceed with Checkpoint 7 — Final Application Promotion, following the applicable engineering instructions and HITL boundaries.

Before promoting Java Application PR #52, verify that all applicable promotion and GitHub governance requirements are satisfied.

If any mandatory requirement remains unsatisfied, report the blocker rather than bypassing it.

Do not merge the Java Application PR.

Present the final engineering report and supporting evidence.
```


### Copilot Turn 14 — Original user instruction

> Source: `GitHub_Copilot_HITL_Original_Transcript.md`, Turn 14.


```text
Re-evaluate
```


---

## 5. Screenshot Evidence — Original OneNote Pages (Chronological)

**Evidence handling:** Each page below is a rendered image of the original 28-page OneNote PDF, including any screenshots, annotations, and captured ChatGPT reviews. Pages are included whole to avoid losing provenance. The original PDF is also included in the ZIP. Some original screenshots may be small because of the PDF export's resolution; this report does not claim to have restored original full-resolution images.


### OneNote page 01

![OneNote evidence page 01](screenshots/OneNote_Page_01.png)


### OneNote page 02

![OneNote evidence page 02](screenshots/OneNote_Page_02.png)


### OneNote page 03

![OneNote evidence page 03](screenshots/OneNote_Page_03.png)


### OneNote page 04

![OneNote evidence page 04](screenshots/OneNote_Page_04.png)


### OneNote page 05

![OneNote evidence page 05](screenshots/OneNote_Page_05.png)


### OneNote page 06

![OneNote evidence page 06](screenshots/OneNote_Page_06.png)


### OneNote page 07

![OneNote evidence page 07](screenshots/OneNote_Page_07.png)


### OneNote page 08

![OneNote evidence page 08](screenshots/OneNote_Page_08.png)


### OneNote page 09

![OneNote evidence page 09](screenshots/OneNote_Page_09.png)


### OneNote page 10

![OneNote evidence page 10](screenshots/OneNote_Page_10.png)


### OneNote page 11

![OneNote evidence page 11](screenshots/OneNote_Page_11.png)


### OneNote page 12

![OneNote evidence page 12](screenshots/OneNote_Page_12.png)


### OneNote page 13

![OneNote evidence page 13](screenshots/OneNote_Page_13.png)


### OneNote page 14

![OneNote evidence page 14](screenshots/OneNote_Page_14.png)


### OneNote page 15

![OneNote evidence page 15](screenshots/OneNote_Page_15.png)


### OneNote page 16

![OneNote evidence page 16](screenshots/OneNote_Page_16.png)


### OneNote page 17

![OneNote evidence page 17](screenshots/OneNote_Page_17.png)


### OneNote page 18

![OneNote evidence page 18](screenshots/OneNote_Page_18.png)


### OneNote page 19

![OneNote evidence page 19](screenshots/OneNote_Page_19.png)


### OneNote page 20

![OneNote evidence page 20](screenshots/OneNote_Page_20.png)


### OneNote page 21

![OneNote evidence page 21](screenshots/OneNote_Page_21.png)


### OneNote page 22

![OneNote evidence page 22](screenshots/OneNote_Page_22.png)


### OneNote page 23

![OneNote evidence page 23](screenshots/OneNote_Page_23.png)


### OneNote page 24

![OneNote evidence page 24](screenshots/OneNote_Page_24.png)


### OneNote page 25

![OneNote evidence page 25](screenshots/OneNote_Page_25.png)


### OneNote page 26

![OneNote evidence page 26](screenshots/OneNote_Page_26.png)


### OneNote page 27

![OneNote evidence page 27](screenshots/OneNote_Page_27.png)


### OneNote page 28

![OneNote evidence page 28](screenshots/OneNote_Page_28.png)


---

## 6. Source Inventory and Verification Limits

- **`GitHub_Copilot_HITL_Original_Transcript.md`** — full Copilot-visible chronological export (14 turns); the definitive verbatim Copilot source.
- **`Original_OneNote_Notes.pdf`** — 28 original OneNote pages; contemporaneous human notes, images, and captures of ChatGPT responses.
- **`screenshots/OneNote_Page_01.png` ... `OneNote_Page_28.png`** — lossless PNG renders of the PDF pages, included at the end of this Markdown report.
- **Current ChatGPT conversation context** — used to understand the broader HITL/No-HITL comparison, but not asserted to contain every early ChatGPT response verbatim.
- **`AI For DevOps.html`** — inspected separately; contains a virtualized fragment of the later conversation, not the early HITL assessments, and is therefore not used as a verbatim HITL source.

**Fidelity statement:** Newly authored historical analysis is explicitly distinguished from original source text. Original ChatGPT assessments are preserved where captured visually in OneNote, but are not transcribed or represented as full verbatim text when that wording cannot be independently verified. The final PR's `UNSTABLE` state and the remaining CodeQL workflow failure are not concealed by the successful Ready-for-Review transition.
