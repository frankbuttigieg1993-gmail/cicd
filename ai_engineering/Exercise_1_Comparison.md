# Exercise 1 — HITL vs No-HITL: Final Comparison

## Research question

Can the same cross-repository GitHub Actions change be completed with fewer **exercise-specific** human approval checkpoints while preserving functional validation and mandatory human governance?

## Experimental design and limitations

Both experiments requested a reusable `ai-generated-list-files` composite action, listing the Java Application repository root non-recursively (including hidden entries), in a separate PR Pipeline job after Build. HITL used **seven additional approval checkpoints**; No-HITL used **zero**. Both retained mandatory human PR reviews and merges.

**This was not a controlled A/B experiment.** Between executions, repository instructions, historical-PR reconciliation, reviewer details and release immutability controls were refined. Differences cannot be attributed solely to removing exercise-specific HITL checkpoints. HITL and No-HITL also reached different documented final merge milestones.

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

## Findings and interpretation

1. **Autonomous continuity:** No-HITL resumed after the mandatory CICD merge, discovered the published immutable release and updated the existing Java PR rather than replacing it.
2. **Functional evidence:** Both exercises examined actual listing output; a green workflow alone was not considered proof of test correctness.
3. **Governance:** Both preserved mandatory review and merge boundaries. No-HITL removed only additional exercise-specific approvals.
4. **Release and historical-PR improvements:** No-HITL avoided two earlier interruptions, but the underlying protections/instructions had been improved between experiments.
5. **Residual issues:** Java CodeQL findings and underlying Gradle test failures remained documented, not resolved by the listing exercise.

## Conclusion

**Observed outcome:** The refined context-engineering framework supported the No-HITL exercise through both repository merges and final read-only verification with **zero additional exercise-specific HITL checkpoints**. The HITL exercise demonstrated the supervised lifecycle through Java PR Ready for Review. This supports the practicality of the refined framework in this scenario; it does **not** isolate the causal impact of checkpoint removal or prove general reliability across future tasks.

See [HITL results](Exercise%201%20-%20HITL/RESULTS.md), [No-HITL results](Exercise%201%20-%20No%20HITL/RESULTS.md), [experiment index](EXPERIMENT_INDEX.md) and [evidence index](EVIDENCE_INDEX.md).
