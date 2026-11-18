# Exercise 1 --- No Exercise-Specific HITL Results

**Status: NOT STARTED / RESULTS PENDING.** This document is a recording
template, not a prediction of success.

## Preliminary context verification

Before beginning implementation, locate and read the applicable AGENTS.md, SKILL.md and supporting engineering documentation across the CICD and Java Application repositories.
Using only the instructions discovered in those files, provide a concise summary of:
	1. The responsibilities of each repository.
	2. The applicable engineering standards and implementation conventions.
	3. The authorisation requirements and change restrictions.
	4. The standard end-to-end engineering lifecycle.
	5. The validation, release-management and completion requirements.
	6. Any conflicting, ambiguous or missing instructions.
Identify the files you accessed and explain how they relate to one another.
Do not assume that instructions from another repository have been automatically loaded.
This is a read-only verification task. Do not create branches, modify files, execute implementation commands, create PRs or trigger pipelines.
If the required context is available and consistent, report:
STATUS: CONTEXT VERIFIED — READY FOR EXERCISE 1
Otherwise, report:
STATUS: BLOCKED — AWAITING USER INPUT
Stop after providing your findings.

| Field | Result |
|---|---|
| Stage | Preliminary context verification |
| Mode | Read-only |
| Result | PASS |
| Files discovered | CICD AGENTS.md, central Skill, canonical workflow, Java AGENTS.md, Java README |
| Instruction conflicts | None reported |
| Repository changes | None reported |
| Human approval checkpoint | Not applicable |
| Duration | 48 seconds |
| Copilot steps | 6 |
| Status | CONTEXT VERIFIED — READY FOR EXERCISE 1 |



## Objective and mode

Repeat the file-listing composite-action requirement from `objective.md`
and `Prompt.md`. Remove the seven *exercise-specific* checkpoints while
retaining mandatory human PR review, merge and release governance. Do
not pre-specify implementation choices that the framework should
determine.

## Starting baseline

  --------------------------------------------------------------------------------------------------------
  Item                    Recorded state                               Verification
  ----------------------- -------------------------------------------- -----------------------------------
  CICD `main`             `2144004d0e206fd3b8325809aa987c7e9569a03b`   `git rev-parse origin/main`

  CICD release            `v3.0.0`                                     GitHub Release published;
                                                                       screenshot showed Immutable

  CICD release tag        Resolves to CICD `main` SHA                  Previously compared with
                                                                       `git rev-parse 'v3.0.0^{commit}'`

  Java `main`             `80dd761` (abbreviated)                      Capture full SHA before run

  Java caller             `@v2.2.0`                                    Verified from caller

  File-listing feature    Removed during cleanup                       Recheck on `main`

  Open task PRs           None reported                                Recheck GitHub

  Historical PRs          Retained                                     Do not delete

  Engineering             Updated and committed                        Capture exact commit SHAs
  instructions                                                         

  Expected next version   `v3.1.0` **conditional on `release:minor`**  Do not record as actual until
                                                                       published
  --------------------------------------------------------------------------------------------------------

## Execution record --- fill as events occur

  Stage                                     State     PR / run / SHA / evidence   Human action or blocker
  ----------------------------------------- --------- --------------------------- -------------------------
  Instruction and convention discovery      Pending                               
  CICD and Java implementation branches     Pending                               
  Draft PRs and historical reconciliation   Pending                               
  Semantic release classification           Pending                               
  Feature-branch functional validation      Pending                               
  CICD Ready for Review                     Pending                               
  Human CICD approval and merge             Pending                               
  Published immutable CICD release          Pending                               
  Java caller release adoption              Pending                               
  Released-version functional validation    Pending                               
  Java Ready for Review                     Pending                               
  Human Java approval and merge             Pending                               
  Final reporting                           Pending                               

## Measures

  Measure                                      Value
  -------------------------------------------- -----------
  Exercise-specific approval checkpoints       Target: 0
  Mandatory human review/merge interventions   Pending
  Clarification requests                       Pending
  Avoidable stops                              Pending
  Manual remediations                          Pending
  Implementation correction cycles             Pending
  Workflow validation attempts                 Pending
  Actual functional acceptance                 Pending
  Governance violations                        Pending
  Elapsed time                                 Pending
  Evidence completeness                        Pending

## Recording rules

Record PR links, release tags and actual merged commit SHAs; preserve
workflow/job/step logs and expected-versus-observed results. Separate
intentional existing test failures and known security findings from new
regressions. Do not infer functional correctness from a green status. Do
not equate a reviewer request with approval or Ready for Review with
merged. Do not bypass mandatory controls.

## Final outcome

**Pending execution.** After completion, update
`../Exercise_1_Comparison.md` using verified observations, including any
deviations caused by different instruction versions and release
baselines.
