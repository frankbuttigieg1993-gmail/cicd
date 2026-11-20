# Exercise 1 — No Exercise-Specific HITL Results

**Final status: COMPLETE — ENGINEERING LIFECYCLE VERIFIED.**

## Executive summary

Scenario 1B — No-HITL successfully implemented and validated the same engineering scenario and functional requirements as Scenario 1A — HITL, without the seven additional experimental human approval checkpoints. GitHub Copilot implemented the reusable composite action, integrated it into the Java Application PR Pipeline, coordinated cross-repository pull requests, inspected actual execution logs, independently discovered and adopted the published immutable CICD release, and completed the engineering lifecycle.

Mandatory human review, approval and merge remained in place for both the CICD and Java Application PRs. **No-HITL did not mean unrestricted autonomy:** only the additional experiment-specific checkpoints were removed. The result demonstrated greater operational autonomy with the same observed functional outcome, not superior code quality. Because the engineering instructions and release protections evolved between scenarios, the improvement cannot be attributed solely to checkpoint removal.

## Objective and execution mode

Create `ai-generated-list-files`, a reusable non-recursive directory-listing composite action that includes hidden entries, and run it in a separate Java PR Pipeline job after successful Build. Remove the seven **exercise-specific** HITL checkpoints, while preserving mandatory human review, approval and merge boundaries.

The exercise began with a separate read-only context verification; execution proceeded in two autonomous phases separated by required human CICD review/merge, followed by a read-only completion verification. Mandatory human PR review, approval and merge, repository rulesets, required checks, release immutability, semantic-version governance and scope restrictions remained applicable throughout.

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

## Concise comparison with Scenario 1A — HITL

| Dimension | Scenario 1A — HITL | Scenario 1B — No-HITL |
|---|---|---|
| Engineering scenario and functional requirements | Same | Same |
| Additional experimental approval checkpoints | 7 | **0** |
| Functional implementation and validation | Successful | Successful |
| Mandatory human PR governance | Preserved | Preserved |
| CICD release | `v2.2.0` | `v3.1.0` |
| Final recorded Java PR milestone | Ready for Review | Merged |
| Final lifecycle verification | Not recorded | Completed |

Both scenarios achieved the required functional outcome. Scenario 1B demonstrated greater operational autonomy and reached a later documented lifecycle milestone, but this does not establish that Scenario 1A could not have done the same. The framework and repository configuration changed between executions, so this was not a controlled test of HITL removal alone. See the [full comparison](../Exercise_1_Comparison.md) for interpretation and limitations.

## Known findings and limitations

- Java Unit Tests check appeared green although Gradle logs reported **3 failures among 5 tests**. This was intentional/pre-existing in the exercise setup; it is not evidence that all tests passed.
- Java CodeQL reported **2 findings** and policy-enforcement failure. Findings were documented, not remediated or waived by the exercise.
- Temporary feature branches and local worktree synchronisation were left for separately authorised cleanup.
- Screenshot-based Copilot reporting supports the outcomes above; consult original runs and PR metadata for independent audit.
- Neither this result nor the comparison establishes that the removal of HITL checkpoints alone caused improvements: framework instructions and repository release protections changed between exercises.

## Supporting documentation

- [No-HITL experiment overview](README.md)
- [Exercise 1 — HITL versus No-HITL comparison](../Exercise_1_Comparison.md)

Original Copilot transcripts, execution screenshots, detailed historical assessments and supporting evidence are preserved separately in the Exercise 1 evidence archive. GitHub PR, release and Actions links above remain the primary navigable evidence references in this results document.

**Final classification: PASS — ENGINEERING LIFECYCLE VERIFIED**, with known application findings documented separately.
