# Exercise 1 — HITL vs No-HITL: Results and Final Assessment

## Executive summary

**Overall assessment: Scenario 1B (No-HITL) produced a better recorded operational outcome, while both scenarios achieved equivalent demonstrated functionality.** There is no evidence that No-HITL produced better code or superior functional correctness. The principal difference was that the agent could progress between mandatory human PR approval and merge boundaries without the seven additional experimental review checkpoints used in Scenario 1A.

The No-HITL run also reached a later recorded lifecycle milestone: both repository PRs were merged and final read-only completion verification was performed. In the HITL record, the Java application PR had reached Ready for Review but its merge was not confirmed. This difference in recorded completion must not be mistaken for evidence that HITL could not have completed the remaining stages.

**The strongest finding is about context engineering and governed autonomy:** the refined `AGENTS.md`, central `SKILL.md`, canonical 16-step workflow, and repository protections supported autonomous continuation without abandoning mandatory human controls. The two runs did not share identical framework or repository baselines, so they cannot isolate the causal effect of removing HITL checkpoints.

## Research question

Can GitHub Copilot implement and validate **the same engineering scenario and functional requirements** with seven additional human-in-the-loop checkpoints (Scenario 1A) versus no additional experimental checkpoints (Scenario 1B), while retaining mandatory PR review, approval and merge governance?

## Experimental design and limitations

**Scenario and requirements were the same in both runs.** Both requested a reusable `ai-generated-list-files` composite action that lists the Java Application repository root non-recursively, including hidden entries, in a separate PR Pipeline job after Build. Both used the same functional acceptance criteria and the same canonical engineering lifecycle.

- **Scenario 1A — HITL:** Seven additional experimental approval checkpoints required the agent to stop for human review and explicit permission to continue at successive stages. Mandatory PR reviews and merges also applied.
- **Scenario 1B — No-HITL:** No additional experimental approval checkpoints. The agent could perform authorised work autonomously, but still had to stop for mandatory human PR review, approval and merge. **No-HITL did not mean unrestricted autonomy.**

**This was not a controlled A/B experiment.** Between executions, repository instructions, historical-PR reconciliation guidance, reviewer details and release immutability controls were refined. Differences in operational friction, continuity and completion cannot be attributed solely to removing exercise-specific HITL checkpoints. The runs also reached different *documented* final merge milestones.

## Observed outcomes

| Dimension | HITL | No-HITL |
|---|---|---|
| Exercise-specific checkpoints | 7 completed | **0** |
| Context verification | Completed | Completed; separate read-only stage |
| CICD PR | [#7](https://github.com/frankbuttigieg1993-gmail/cicd/pull/7) merged | [#8](https://github.com/frankbuttigieg1993-gmail/cicd/pull/8) merged |
| CICD release | [`v2.2.0`](https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v2.2.0) | [`v3.1.0`](https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v3.1.0) |
| Release protection | Required remediation; tag ruleset and native immutability addressed | Published release observed immutable without new remediation |
| Java PR | [#52](https://github.com/frankbuttigieg1993-gmail/java_application/pull/52) Ready for Review at last recorded checkpoint | [#58](https://github.com/frankbuttigieg1993-gmail/java_application/pull/58) merged |
| Final Java reference | `@v2.2.0` | `@v3.1.0` |
| Historical PR handling | Required clarification | No extra clarification reported |
| Feature-branch validation | Demonstrated | Demonstrated |
| Fresh release-based validation | Demonstrated | Demonstrated |
| Actual listing logs | Inspected | Inspected |
| Final completion verification | Not recorded | Completed, read-only |
| Mandatory human governance | Retained | Retained |
| Known test/CodeQL issues | Documented | Documented; unresolved |

## No-HITL execution measurements

| Stage | Steps | Copilot-reported duration |
|---|---:|---:|
| Context verification | 7 | 48s |
| Initial execution | 39 | 9m 14s |
| Release adoption | 24 | 10m 7s |
| Final verification | 7 | 1m 18s |
| **Total** | **77** | **21m 27s** |

The totals exclude human review, waiting time and gaps between phases. An earlier context-verification record said 6 steps; the final screenshot-based summary used 7. Comparable HITL total steps, duration, clarification count and remediation count have **not** been independently reconstructed, so no quantitative efficiency ratio is claimed.

## Technical evidence

| Item | HITL | No-HITL |
|---|---|---|
| CICD merge SHA | `1c0e8e3021c35de606b0df685d5fdd6374c66b78` | `e7ecad9de8694095e2ea99d1f3ce77d23fc4b5b7` |
| Java merge SHA | Not confirmed in HITL record | `864bf2e8152be77ec596dcce1a9dafc77a1ad86d` |
| Released-version validation | [Run 44016664579](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44016664579) | [Run 44217333120](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44217333120) |
| Feature-branch validation | Refer to HITL transcript | [Run 44210309429](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44210309429) |

## Comparative assessment

| Evaluation dimension | Assessment | Rationale |
|---|---|---|
| Functional correctness | **Equivalent on demonstrated criteria** | Both implemented and validated the required listing action and Java PR Pipeline integration. |
| Implementation quality | **No demonstrated winner** | The available evidence does not establish a code-quality advantage for either execution model. |
| Operational autonomy | **No-HITL** | No additional exercise-specific approval checkpoints versus seven in HITL. |
| Human interruptions | **No-HITL, by design** | The experiment intentionally removed discretionary checkpoints, not mandatory governance. |
| Historical PR handling | **No-HITL operationally** | No-HITL reconciled historical/current PR state without extra clarification; guidance had been improved beforehand. |
| Release management friction | **No-HITL operationally** | Release protections were already established; HITL required remediation during its run. |
| Governance compliance | **Equivalent in observed boundaries** | Both retained mandatory human review and merge controls. |
| Recorded lifecycle completion | **No-HITL** | No-HITL completed both merges and final verification; HITL's last recorded Java milestone was Ready for Review. |

### Finding 1 — Functional equivalence, not better code

Both runs delivered the same requested capability: a reusable GitHub Actions composite action that lists directory contents (including hidden entries), integrated into the Java PR Pipeline after Build. Both inspected actual workflow logs rather than treating green status indicators as sufficient proof. Neither run demonstrated a clear technical superiority in the implemented functionality. **It would be inaccurate to claim that No-HITL wrote better code.**

### Finding 2 — Greater operational autonomy

HITL required seven extra experimental stops for review and authorisation. No-HITL completed authorised work between the two mandatory PR governance boundaries without those additional stops. This is a direct observed difference in the execution model, not proof of a general time saving: comparable HITL end-to-end timing and human waiting time have not been established.

### Finding 3 — Better operational continuity in the later run

The HITL run encountered historical PR confusion and release-immutability remediation. The No-HITL run reconciled current versus historical branches/PRs, reused the existing Java PR during release adoption, discovered the immutable release, and progressed to final verification. These improvements are consistent with the **more mature context-engineering framework and repository configuration** used for the later run; they cannot be credited to checkpoint removal alone.

### Finding 4 — Different documented completion milestones

HITL successfully reached Java Application Ready for Review; No-HITL went further, including the mandatory human Java merge and read-only verification of the final production reference. That is a stronger *recorded* lifecycle outcome, not evidence that the HITL approach was technically incapable of completing those stages.

### Finding 5 — Known findings remain outside the functional claim

Both experiments documented the pre-existing discrepancy between green Java Unit Tests checks and underlying Gradle failures, as well as separate Java CodeQL findings. Neither listing-action implementation resolved these issues. Successful functional validation should not be confused with a clean application test/security posture.

## Interpretation of the context-engineering framework

- **`AGENTS.md` — What is permitted:** repository ownership, authorisation, restrictions, guardrails and mandatory human review/merge boundaries.
- **Central `SKILL.md` — How to execute:** the reusable operational runbook for branches, PR reconciliation, implementation, testing, release adoption, log inspection and failure handling.
- **Canonical 16-step workflow — When and in what order:** the engineering lifecycle sequence, promotion dependencies and handoffs.

The HITL exercise exposed operational gaps that were addressed as the framework evolved. The No-HITL exercise then provided stronger end-to-end evidence that the refined framework could support governed autonomy for this specific engineering task. This is **stronger evidence for the practical value of context engineering** than for any general superiority of No-HITL over HITL.

## What would make a stronger future comparison?

To isolate the effect of HITL checkpoints, repeat the same task with the **same** `AGENTS.md`, `SKILL.md`, canonical workflow, repository protections, starting state and acceptance criteria; vary only the checkpoint model. Record human waiting time, total elapsed time, interventions, rework, quality findings and completion status for both runs.

## Conclusion

**Scenario 1B — No-HITL produced a better overall *recorded operational* outcome, while achieving the same demonstrated functional engineering result as Scenario 1A — HITL.** The advantage was greater autonomous continuity and the absence of seven additional experimental approval checkpoints, **not** demonstrably better code. Mandatory human PR review, approval and merge controls remained in force in both scenarios.

Because the context-engineering framework and repository configuration matured between runs, the evidence supports a bounded conclusion: **a refined, well-governed AI engineering framework enabled Copilot to complete this particular cross-repository lifecycle with fewer discretionary human interruptions, without sacrificing the demonstrated functional outcome.** It does not prove that No-HITL is always superior or that removing checkpoints alone caused the improvement.

## Related records

- [HITL experiment](HITL/README.md) — original prompts, checkpoint summaries and recorded outcome.
- [No-HITL experiment](NO_HITL/README.md) — original prompts, execution-phase summaries and recorded outcome.
- [AI Engineering overview](README.md) — experiment navigation and framework context.

Original transcripts, screenshots and full historical evidence are archived separately.
