# Exercise 1 --- HITL Results

**Status:** Seven supervised checkpoints completed; Java PR promoted to Ready for Review. Final Java merge not confirmed.

## Objective and execution mode

Create `ai-generated-list-files`, a non-recursive composite action listing the Java repository root including hidden entries, in a separate PR Pipeline job after successful Build. Follow the central engineering framework with seven **additional** human approval checkpoints. See `objective_HITL.md` (reconstruction) and `Exercise1_prompt.md` (stored prompt).

## Checkpoint outcomes

  -----------------------------------------------------------------------
Checkpoint                          Result ----------------------------------- ----------------------------------- 1 --- Planning                      Completed; requirements,
                                      conventions, scope and validation
                                      plan reviewed

2 --- Implementation                Completed; scoped implementation
                                      and local checks

3 --- Draft PRs and Integration     Completed; cross-repository Validation                          feature-branch validation and
                                      evidence

4 --- CICD PR Promotion             CICD PR #7 promoted, reviewer
                                      requested

5 --- CICD Release Verification     CICD PR #7 merged; `v2.2.0`
                                      published; governance blocker
                                      resolved with tag ruleset

6 --- Application Release Adoption  Java PR #52 updated to `@v2.2.0`; and Validation                      fresh logs verified functionality

7 --- Final Application Promotion   Java PR #52 promoted to Ready for
                                      Review; final human review/merge
                                      outstanding
  -----------------------------------------------------------------------

## Engineering evidence

  ---------------------------------------------------------------------------------------------------------------------------
Item                                Observed value ----------------------------------- --------------------------------------------------------------------------------------- CICD PR                             https://github.com/frankbuttigieg1993-gmail/cicd/pull/7

Java PR                             https://github.com/frankbuttigieg1993-gmail/java_application/pull/52

CICD release                        `v2.2.0`

CICD merge commit                   `1c0e8e3021c35de606b0df685d5fdd6374c66b78`

CICD release run                    https://github.com/frankbuttigieg1993-gmail/cicd/actions/runs/44014320065

Java released-version validation    https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44016664579 run

Application release reference       `@v2.2.0`

Functional evidence                 Listing executed after Build; expected root entries including `.github` and
                                      `.gitignore` observed; 37 tracked entries compared

Reviewer requested                  `frankbuttigieg93-png`

Final observed application PR state Ready for Review, not confirmed merged
  ---------------------------------------------------------------------------------------------------------------------------

## Important findings and responses

**Historical PR confusion:** Earlier closed/merged PRs and reused branch names were initially misinterpreted. Later policy and Skill revisions added explicit branch/PR identity reconciliation. A later No-HITL run demonstrated successful reconciliation in that scenario; this does not change the historical HITL finding.

**Reviewer correction:** An outdated reviewer reference was corrected across instructions; Copilot re-evaluated and requested the intended reviewer.

**Release immutability:** Copilot identified missing technical protection for the already-published `v2.2.0`. A tag ruleset was added to restrict updates and deletion, and native release immutability was enabled for future releases. Existing release API immutability and tag protection are distinct.

**Test and security findings:** Unit Tests reported green despite intentionally tolerated underlying test failures; known CodeQL findings remained. Copilot documented these rather than claiming all underlying tests passed. Final GitHub merge state was reported `UNSTABLE`; the human merge decision remained subject to repository rules.

## What the experiment demonstrated

The supervised process coordinated two repositories, verified an unreleased feature, published and protected a CICD version, adopted it in an application, and inspected actual step logs. The self-repository action reference `uses: $/.github/actions/ai-generated-list-files` worked in the tested reusable workflow.

It **did not** prove unattended autonomous execution, a completed Java merge, or scaling across multiple application repositories.

## Evidence and provenance

The authoritative raw record is `Exercise 1 - HITL.md` / `.json`, plus the linked GitHub PRs and workflow runs. This summary reflects the recorded checkpoint assessments; independently verify any disputed detail against those records. Exact initial instruction SHAs, starting commits, elapsed time and intervention counts are **not yet reconstructed** and should not be guessed.

## Follow-up

Use this as the completed comparison baseline; preserve historical PRs, tags, runs and exports. The later No-HITL exercise completed its full lifecycle; see the [comparison](../Exercise_1_Comparison.md), [experiment index](../EXPERIMENT_INDEX.md) and [historical report](Exercise_1_HITL_Full_Historical_Report.md).
