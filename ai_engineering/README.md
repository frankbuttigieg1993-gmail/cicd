# AI Engineering — Context Engineering Experiments

**Start here.** This directory records the engineering framework and the completed Exercise 1 HITL and No-HITL experiments. It is a **human-facing handover and evidence index**, not an authoritative agent instruction source.

## Purpose

Evaluate whether version-controlled repository context can guide GitHub Copilot through a cross-repository engineering lifecycle with fewer exercise-specific human interruptions, while retaining required governance and evidence-based validation.

## Three-layer instruction framework

| Layer | Authoritative location | Purpose |
|---|---|---|
| Governance | CICD and Java Application `AGENTS.md` | **What** is authorised, mandatory and prohibited |
| Execution | CICD `.github/skills/github-actions-development/SKILL.md` | **How** to implement, validate, reconcile PRs and handle failures |
| Orchestration | CICD `.github/Standard CICD Engineering, Release & Application Promotion Workflow.md` | **When** lifecycle steps and handoffs occur |

GitHub permissions, rulesets, required checks and release protection enforce platform controls; Markdown alone does not.

## Exercise 1 outcomes

| Experiment | Observed result | Final recorded milestone |
|---|---|---|
| HITL | Seven additional checkpoints; CICD PR #7 merged; immutable/protected `v2.2.0`; Java PR #52 adopted release | Java PR Ready for Review; final merge not confirmed |
| No-HITL | Zero additional exercise checkpoints; CICD PR #8 merged; immutable `v3.1.0`; Java PR #58 adopted release | Java PR merged; final lifecycle verification complete |

**No-HITL does not mean no human governance.** Both executions retained mandatory PR reviews and merges. The instruction and repository baselines differed, so the comparison is observational, not a controlled causal test.

## Documentation map

| File | Purpose |
|---|---|
| [Framework handover](AI_Engineering_Framework_README.md) | Architecture, governance and onboarding |
| [HITL results](Exercise%201%20-%20HITL/RESULTS.md) | Supervised checkpoint outcomes |
| [No-HITL results](Exercise%201%20-%20No%20HITL/RESULTS.md) | Completed autonomous execution and final verification |
| [Comparison](Exercise_1_Comparison.md) | Cross-experiment findings and limitations |
| [Experiment index](EXPERIMENT_INDEX.md) | Quick status and artifact navigation |
| [Evidence index](EVIDENCE_INDEX.md) | PRs, releases, SHAs, workflow runs and screenshot archive guidance |
| [HITL stored execution prompt](Exercise%201%20-%20HITL/Exercise1_prompt.md) | Historical HITL prompt |
| [No-HITL context-verification prompt](Exercise%201%20-%20No%20HITL/Exercise_1_Read_Only_Context_Verification_Prompt.md) | Read-only understanding check |
| [No-HITL execution prompt](Exercise%201%20-%20No%20HITL/Exercise_1_No_HITL_Execution_Prompt.md) | Autonomous engineering objective |
| [No-HITL resume prompt](Exercise%201%20-%20No%20HITL/Exercise1_No_HITL_PromptforResume.md) | Continuation after mandatory CICD merge |

Historical transcripts, assessments and screenshots are evidence, not current operational instructions. See the evidence index for asset availability.

## Starting another exercise

Read current policy, Skill and canonical workflow from the actual repositories. Record starting repository SHAs, release/tag state, pipeline authorisation and known findings. Distinguish read-only context verification from implementation. Preserve actual PR/run/log evidence and mandatory human governance boundaries. Do not copy exercise-specific solutions into general instructions.

## Maintenance

Change governance in the relevant `AGENTS.md`, reusable procedures in the central `SKILL.md`, and lifecycle ordering in the canonical workflow. Keep exercise objectives, results and historical evidence under `ai_engineering/`. Review proposed framework changes separately from routine engineering execution.

**Status:** HITL historical milestone recorded; No-HITL full engineering lifecycle verified.
