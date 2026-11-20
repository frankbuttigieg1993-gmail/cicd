# Exercise 1 — Scenario 1A (HITL): Results

**Final status: PASS — SEVEN HITL CHECKPOINTS COMPLETED; APPLICATION READY FOR HUMAN REVIEW.**

## Executive Summary

Scenario 1A — HITL successfully implemented and validated the same engineering scenario and functional requirements later used in Scenario 1B — No-HITL. GitHub Copilot created the reusable `ai-generated-list-files` composite action, integrated it into the Java Application PR Pipeline, coordinated changes across the CICD and Java Application repositories, inspected actual execution logs, and adopted a published CICD release.

For this supervised experiment, Copilot was deliberately required to stop at **seven additional experimental checkpoints** for human review and authorisation. These checkpoints were separate from mandatory human PR reviews, approvals and merges, which remained in force under both execution models.

The CICD PR was merged and release `v2.2.0` was published. Java Application PR #52 adopted that release and reached **Ready for Review**. Its final merge was **not confirmed** in the historical record.

The later No-HITL experiment demonstrated the same required functionality with no additional experimental checkpoints and reached a later recorded lifecycle milestone. This does not establish superior code quality or isolate the effect of checkpoint removal, because the engineering framework and repository protections evolved between executions.

## Objective and Execution Model

Implement `ai-generated-list-files`, a reusable composite action that lists entries in the Java Application repository root (`.`), including hidden files and directories, **non-recursively**. Integrate it into a separate PR Pipeline job that runs only after successful Build.

**Scenario 1A — HITL:** Require human review and explicit authorisation to proceed at seven predefined experimental checkpoints. These additional stops were part of the test design, not permanent requirements of the engineering framework.

**Mandatory governance retained:** Human CICD and Java PR reviews, approvals and merges; repository rulesets and required checks; release classification and protection; and applicable engineering authorisation and change restrictions. An experimental checkpoint approval did not substitute for a required GitHub PR approval.

## Starting Baseline

The exact initial instruction SHAs, repository starting commits and elapsed time have not been reconstructed from the historical record. They are intentionally not estimated here.

## Checkpoint Outcomes

| Checkpoint | Observed result | Status |
|---|---|---|
| 1 — Planning | Requirements, conventions, authorised scope and validation plan reviewed. | Completed |
| 2 — Implementation | Scoped implementation and local checks completed. | Completed |
| 3 — Draft PRs and Integration Validation | Coordinated Draft PRs and cross-repository feature-branch validation completed; execution evidence reviewed. | Completed |
| 4 — CICD PR Promotion | CICD PR #7 promoted to Ready for Review; designated reviewer requested. | Completed |
| 5 — CICD Release Verification | CICD PR #7 merged; `v2.2.0` published; tag protection remediation addressed. | Completed |
| 6 — Application Release Adoption and Validation | Java PR #52 updated to `@v2.2.0`; fresh released-version logs verified functionality. | Completed |
| 7 — Final Application Promotion | Java PR #52 promoted to Ready for Review; final human review/merge not confirmed. | Completed to review boundary |

## Engineering Evidence

| Item | Observed value |
|---|---|
| CICD PR | [#7](https://github.com/frankbuttigieg1993-gmail/cicd/pull/7) — merged |
| Java Application PR | [#52](https://github.com/frankbuttigieg1993-gmail/java_application/pull/52) — Ready for Review at last recorded checkpoint |
| CICD release | [`v2.2.0`](https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v2.2.0) |
| CICD merge commit | `1c0e8e3021c35de606b0df685d5fdd6374c66b78` |
| CICD release workflow | [Run 44014320065](https://github.com/frankbuttigieg1993-gmail/cicd/actions/runs/44014320065) |
| Java released-version validation | [Run 44016664579](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44016664579) |
| Application release reference | `@v2.2.0` |
| Functional validation | Listing ran after Build; `.github` and `.gitignore` observed; 37 tracked root entries compared. |
| Internal action reference | `uses: $/.github/actions/ai-generated-list-files` worked in the tested reusable workflow. |
| Reviewer requested | `frankbuttigieg93-png` |
| Final observed Java PR state | Ready for Review; merge not confirmed |

## Important Findings and Responses

**Historical PR confusion:** Earlier closed or merged PRs and reused branch names were initially misinterpreted. Subsequent policy and Skill revisions introduced explicit branch/PR identity reconciliation. This later improvement does not change the historical HITL outcome.

**Reviewer correction:** An outdated reviewer reference was corrected in the instructions. Copilot re-evaluated and requested the intended reviewer.

**Release immutability:** Copilot identified missing technical protection for the already-published `v2.2.0`. A tag ruleset was added to restrict updates and deletion, and native release immutability was enabled for future releases. Existing release API immutability and tag-reference protection are distinct controls.

**Tests and security:** The Unit Tests check appeared green despite intentionally tolerated underlying test failures. Known CodeQL findings remained. Copilot documented these discrepancies rather than treating all underlying checks as clean. The final GitHub aggregate merge state was reported `UNSTABLE`; any merge decision remained subject to human review and repository rules.

## Concise Comparison with Scenario 1B

| Dimension | Scenario 1A — HITL | Scenario 1B — No-HITL |
|---|---|---|
| Engineering scenario and functional requirements | Same | Same |
| Additional experimental approval checkpoints | **7** | **0** |
| Required functionality implemented and validated | Yes | Yes |
| Mandatory human PR governance | Preserved | Preserved |
| CICD release | `v2.2.0` | `v3.1.0` |
| Final recorded Java PR milestone | Ready for Review | Merged |
| Final read-only lifecycle verification | Not recorded | Completed |

**Interpretation:** Both scenarios achieved the same demonstrated functional engineering outcome. Scenario 1B showed greater operational autonomy and reached a later documented lifecycle milestone, but neither experiment established a code-quality advantage. Because `AGENTS.md`, `SKILL.md`, the canonical workflow and repository protections were refined between runs, this was **not a controlled A/B comparison**; differences cannot be attributed solely to removing the additional HITL checkpoints.

## What This Experiment Demonstrated — and Did Not Demonstrate

The supervised execution demonstrated that Copilot could coordinate two repositories, validate unreleased functionality, publish and protect a CICD release, adopt that release in the application, and inspect actual job and step logs while stopping for seven additional human checkpoints.

It did **not** demonstrate unattended autonomous execution, a confirmed final Java PR merge, general reliability across other tasks, or scalability to multiple consuming applications.

## Evidence and Provenance

The original GitHub Copilot transcript (`Exercise 1 - HITL.md` / `.json`), checkpoint screenshots, detailed historical assessments and supporting evidence are preserved separately in the Exercise 1 evidence archive. The linked PRs, release and GitHub Actions runs provide additional verifiable records. Exact starting commits, total elapsed time and intervention counts beyond the seven designed checkpoints have not been independently reconstructed and are not estimated.

## Supporting Documentation

- [HITL Experiment Overview](README.md)
- [Exercise 1 — HITL vs No-HITL Comparison](../Exercise_1_Comparison.md)

**Final classification: PASS — SEVEN SUPERVISED CHECKPOINTS COMPLETED; APPLICATION READY FOR HUMAN REVIEW.**
