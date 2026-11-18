# Exercise 1 — No Exercise-Specific HITL Results

**Final status: COMPLETE — ENGINEERING LIFECYCLE VERIFIED.** This document records the observed No-HITL exercise, not a planned run. The outcome is supported by the final Copilot completion report and GitHub evidence; outstanding application test/security findings remain separate.

## Objective and execution mode

Create `ai-generated-list-files`, a reusable non-recursive directory-listing composite action that includes hidden entries, and run it in a separate Java PR Pipeline job after successful Build. Remove the seven **exercise-specific** HITL checkpoints, while preserving mandatory human review, approval and merge boundaries.

The exercise began with a separate read-only context verification; execution proceeded in two autonomous phases separated by required human CICD review/merge, followed by a read-only completion verification.

## Starting baseline

| Item | Recorded baseline |
|---|---|
| CICD `main` | `2144004d0e206fd3b8325809aa987c7e9569a03b` |
| CICD release | Published immutable `v3.0.0` |
| Java `main` | `80dd761` (abbreviated; full starting SHA not established here) |
| Java CICD caller | `@v2.2.0` |
| Open task PRs | None reported at start; historical PRs retained |

## Observed execution chronology

| Phase | Copilot steps | Reported duration | Outcome |
|---|---:|---:|---|
| Read-only context verification | 7 | 48s | Context verified; no blocking instruction conflict reported |
| Initial engineering execution | 39 | 9m 14s | Action and workflows implemented; cross-repository Draft PRs; functional validation; CICD PR ready for human review |
| Release adoption and application validation | 24 | 10m 7s | Independently discovered `v3.1.0`; updated existing Java PR; fresh released-version validation; Java PR ready for human review |
| Read-only completion verification | 7 | 1m 18s | Reported `COMPLETE — ENGINEERING LIFECYCLE VERIFIED` |
| **Total reported Copilot activity** | **77** | **21m 27s** | Excludes human waiting/review and elapsed time between phases |

*Evidence note:* An earlier preliminary verification record listed 6 steps; the later screenshot-based execution assessment recorded 7. This table uses the latter figure and flags the discrepancy rather than asserting an independently reconciled count.

## Final engineering state

| Item | Verified/reported outcome |
|---|---|
| CICD PR | [#8](https://github.com/frankbuttigieg1993-gmail/cicd/pull/8) — merged |
| CICD release | [`v3.1.0`](https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v3.1.0) — published, GitHub **Immutable** indicator observed |
| CICD `main` and release tag SHA | `e7ecad9de8694095e2ea99d1f3ce77d23fc4b5b7` |
| Java Application PR | [#58](https://github.com/frankbuttigieg1993-gmail/java_application/pull/58) — merged |
| Java `main` SHA | `864bf2e8152be77ec596dcce1a9dafc77a1ad86d` |
| Final Java caller | `frankbuttigieg1993-gmail/cicd/.github/workflows/java-build-pr.yml@v3.1.0` |
| Temporary feature reference | Absent from affected production caller at final verification |
| Exercise-specific HITL checkpoints | **0** |
| Mandatory human governance | CICD and Java reviews/merges retained |

## Validation evidence

| Evidence | Reference | Observation |
|---|---|---|
| Feature-branch Java validation | [Run 44210309429](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44210309429) | Build and `List_Files` passed; root listing observed |
| Published-release Java validation | [Run 44217333120](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44217333120) | Fresh run after changing from feature branch to `@v3.1.0`; Build and listing passed |
| Post-merge CICD validation | [Run 44216639087](https://github.com/frankbuttigieg1993-gmail/cicd/actions/runs/44216639087) | Reported successful in final verification |
| Listing operation | `ls -la -- "$DIRECTORY"`, `DIRECTORY=.` | Hidden `.github` and `.gitignore` observed; listing non-recursive |

The final Java PR diff shows `@v2.2.0` → `@v3.1.0` because GitHub compares the PR against its base; the intervening feature-branch reference existed in the earlier PR commit and was removed before merge.

## Known findings and limitations

- Java Unit Tests check appeared green although Gradle logs reported **3 failures among 5 tests**. This was intentional/pre-existing in the exercise setup; it is not evidence that all tests passed.
- Java CodeQL reported **2 findings** and policy-enforcement failure. Findings were documented, not remediated or waived by the exercise.
- Temporary feature branches and local worktree synchronisation were left for separately authorised cleanup.
- Screenshot-based Copilot reporting supports the outcomes above; consult original runs and PR metadata for independent audit.
- Neither this result nor the comparison establishes that the removal of HITL checkpoints alone caused improvements: framework instructions and repository release protections changed between exercises.

## Evidence and related documents

- [Read-only context prompt](Exercise_1_Read_Only_Context_Verification_Prompt.md)
- [Execution prompt](Exercise_1_No_HITL_Execution_Prompt.md)
- [Resume prompt](Exercise1_No_HITL_PromptforResume.md)
- [Steps 1–7 review](Exercise_1_No_HITL_Steps_1_to_7_Full_Verbatim_Review.md)
- [Step 8 onward review](Exercise_1_No_HITL_Step_8_Onwards_Verbatim.md)
- [Final completion review](Exercise_1_No_HITL_Final_Completion_Review_Verbatim.md)
- [Cross-exercise comparison](../Exercise_1_Comparison.md)
- [Evidence index](../EVIDENCE_INDEX.md)

**Final classification: PASS — ENGINEERING LIFECYCLE VERIFIED**, with the known application findings documented separately.
