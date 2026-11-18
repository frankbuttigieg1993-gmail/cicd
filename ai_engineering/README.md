# AI Engineering --- Context Engineering Experiments

**Start here.** This directory documents the engineering framework, the
completed supervised Exercise 1, and the planned execution without
exercise-specific HITL checkpoints. This is a human-facing index, not an
authoritative agent instruction.

## Purpose

Evaluate whether reusable, version-controlled engineering context
enables GitHub Copilot to implement and validate the same
cross-repository GitHub Actions change with fewer human interventions
while retaining functional quality and mandatory governance.

## Three-layer framework

  ---------------------------------------------------------------------------------------------------------------------------------------
  Layer                   Source                                                                                  Responsibility
  ----------------------- --------------------------------------------------------------------------------------- -----------------------
  Governance              `cicd/AGENTS.md` and `java_application/AGENTS.md`                                       **What** is authorised,
                                                                                                                  required and prohibited

  Execution               `cicd/.github/skills/github-actions-development/SKILL.md`                               **How** to implement,
                                                                                                                  verify, reconcile PRs
                                                                                                                  and handle failures

  Orchestration           `cicd/.github/Standard CICD Engineering, Release & Application Promotion Workflow.md`   **When** the 16
                                                                                                                  lifecycle steps,
                                                                                                                  handoffs and promotion
                                                                                                                  gates occur
  ---------------------------------------------------------------------------------------------------------------------------------------

GitHub rulesets, permissions, required checks and release protection
enforce technical controls. Markdown instructions influence agent
behaviour; they do not replace platform controls.

## Exercises

**Exercise 1 --- HITL:** Seven supervised checkpoints were completed.
CICD PR [#7](https://github.com/frankbuttigieg1993-gmail/cicd/pull/7)
was merged; CICD `v2.2.0` was released and protected; Java PR
[#52](https://github.com/frankbuttigieg1993-gmail/java_application/pull/52)
adopted the release and reached Ready for Review. Final Java merge was
not confirmed.

**Exercise 1 --- No HITL:** The same functional requirement will be
repeated from the cleaned CICD `main`
(`2144004d0e206fd3b8325809aa987c7e9569a03b`), published immutable
release `v3.0.0`, and Java `main` (`80dd761`, abbreviated). Java
currently calls CICD `@v2.2.0`. The expected next release is `v3.1.0`
**if** the new change is classified as `release:minor` and release
automation recognises the baseline. Outcomes are pending.

**No HITL** means no *extra exercise checkpoints*; mandatory human
review and merge boundaries still apply.

## Documentation index

  ------------------------------------------------------------------------------------------------------------
  Document                                                                 Audience and purpose
  ------------------------------------------------------------------------ -----------------------------------
  `AI_Engineering_Framework_README.md`                                     Operational framework handover and
                                                                           onboarding

  `Exercise 1 - HITL/Exercise_1_Context_Engineering_Overview.md`           Types of context engineering and
                                                                           evidence

  `Exercise 1 - HITL/Exercise_1_Three_Layer_AI_Engineering_Framework.md`   Architecture rationale for the
                                                                           three layers

  `Exercise 1 - HITL/objective_HITL.md`                                    Reconstructed HITL objective and
                                                                           checkpoint design; **not** a
                                                                           verbatim historical prompt

  `Exercise 1 - HITL/Exercise1_prompt.md`                                  Stored HITL execution prompt

  `Exercise 1 - HITL/Exercise 1 - HITL.md` and `.json`                     Raw Copilot conversation exports

  `Exercise 1 - HITL/RESULTS.md`                                           Concise observed HITL outcomes and
                                                                           lessons

  `Exercise 1 - No HITL/objective.md`                                      Autonomous exercise objective and
                                                                           rationale

  `Exercise 1 - No HITL/Prompt.md`                                         Actual proposed No-HITL execution
                                                                           prompt

  `Exercise 1 - No HITL/RESULTS.md`                                        Baseline and pending result-capture
                                                                           template

  `Exercise_1_Comparison.md`                                               Cross-exercise comparison and
                                                                           measurement protocol
  ------------------------------------------------------------------------------------------------------------

## How to run and record an exercise

Read the **latest** policy, Skill and canonical lifecycle; confirm the
explicitly selected pipeline; capture the current repository and
instruction SHAs; preserve unrelated work and historical PRs. Start a
new Copilot session for the No-HITL run. Record actual PRs, SHAs,
labels, runs, logs, governance stops, human interventions and
exceptions. Do not mark anticipated outcomes as achieved.

## Maintenance

Change policies in the relevant `AGENTS.md`, reusable procedures in the
central Skill, and lifecycle ordering in the canonical workflow. Keep
exercise-specific objectives and observations in this directory. Update
the comparison only from recorded evidence.

**Status:** HITL evidence captured; No-HITL execution pending.
