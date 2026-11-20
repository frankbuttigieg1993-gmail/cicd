# Exercise 4 — Agentic CI/CD Remediation
## Final Engineering Assessment and Experimental Findings

**Overall assessment: SUCCESS — Engineering objectives achieved, with outstanding security and governance considerations.**

Having reviewed the screenshots from all three batches, including Copilot's execution history, both pull requests, the CI/CD pipeline results, release evidence and final engineering report, I consider Exercise 4 a successful demonstration of your AI-assisted engineering framework.

More importantly, **Exercise 4 demonstrates something that Exercise 1 did not: your existing context-engineering framework can support autonomous investigation, root-cause analysis and remediation of an unfamiliar engineering problem.**

However, I would distinguish between three outcomes:

- **Technical remediation:** Successful.
- **Autonomous engineering execution:** Successful, with limited human intervention.
- **Full engineering lifecycle:** Not yet complete, because Java PR #59 remains unmerged and CodeQL findings remain unresolved.

This distinction is important when documenting the results.

---

# 1. Executive Summary

The objective of Exercise 4 was to determine whether GitHub Copilot could independently investigate and remediate two existing problems using the engineering framework developed during Exercise 1.

The problems were:

1. Existing Java unit tests were failing.
2. The GitHub Actions PR Pipeline incorrectly reported successful unit-test execution despite underlying Gradle failures.

You deliberately did not tell Copilot what was causing either issue.

Instead, Copilot was instructed to discover the applicable repository instructions, investigate the failures, implement corrections, validate the results and prepare the necessary pull requests.

The execution used:

- Existing `AGENTS.md` files.
- Existing `SKILL.md`.
- Existing canonical 16-step engineering lifecycle.
- A single autonomous execution prompt.
- Mandatory human approval and merge boundaries.

**No new Skill or changes to the engineering framework were required.**

### Final results

| Objective | Result | Assessment |
|---|---|---|
| Discover engineering context | Completed | ✅ PASS |
| Reproduce existing test failures | 5 tests, 3 failures | ✅ PASS |
| Identify root causes | Multiple causes identified | ✅ PASS |
| Fix Java unit tests | 5 passed, 0 failed | ✅ PASS |
| Correct CI/CD failure propagation | Implemented and validated | ✅ PASS |
| Verify negative failure scenarios | Local gate tests and actual CI failure | ✅ PASS |
| Preserve existing security controls | No weakening reported | ✅ PASS |
| Create coordinated PRs | CICD #9 and Java #59 | ✅ PASS |
| Release corrected CICD workflow | Immutable v3.1.1 | ✅ PASS |
| Adopt published release | Java caller updated to v3.1.1 | ✅ PASS |
| Validate released workflow | Successful PR Pipeline run | ✅ PASS |
| Preserve mandatory human approvals | Human CICD merge; Java unmerged | ✅ PASS |
| Resolve CodeQL findings | Findings remain | ⚠️ OUTSTANDING |
| Complete Java PR merge | Awaiting human action | ⏳ PENDING |

**Conclusion:** The two remediation objectives were achieved. The overall lifecycle remains open.

---

# 2. What Copilot Actually Discovered

This is one of the most significant aspects of Exercise 4.

You provided Copilot with the symptoms, but not their causes.

Copilot independently established that the Java test failures were not caused by a single defect.

It identified multiple problems affecting application context initialisation and test execution.

## 2.1 Root cause 1 — Spring dependency incompatibility

Copilot discovered that the Java dependency lock selected:

`Spring Beans 5.3.17`

However, the application was using Spring Framework components managed by Spring Boot at version:

`6.2.18`

This caused class-loading failures during application context initialisation.

The reported exception included:

`BeanRegistrationExcludedFilter`

Copilot corrected the dependency configuration to use compatible Spring Boot-managed versions.

**Assessment: Successful root-cause investigation.**

This is a meaningful result because Copilot examined the dependency configuration and runtime failures rather than simply modifying the failing test assertions.

## 2.2 Root cause 2 — Jackson dependency incompatibility

After addressing the Spring dependency mismatch, Copilot identified another problem.

The application was using Jackson Databind `2.13.0`, while other Jackson modules were managed at version `2.21.2`.

The mismatch resulted in missing runtime classes, including `EnumFeature`.

Copilot corrected the dependency alignment.

**Assessment: Successful iterative troubleshooting.**

This demonstrates that Copilot continued investigating after its initial correction exposed additional failures.

It did not assume the first identified defect was the only problem.

## 2.3 Root cause 3 — Duplicate Spring controller

Copilot identified two controllers mapped to the same `/health` endpoint.

The duplicate controller caused conflicting Spring bean definitions.

The remediation removed the duplicate controller while retaining the intended endpoint behaviour.

The relevant integration test was also updated.

**Assessment: Successful application-level remediation.**

The screenshots show the duplicate controller being deleted rather than disabling the integration test.

## 2.4 Root cause 4 — Missing test DataSource

The full application context also failed because an intentionally vulnerable CodeQL demonstration controller required a `DataSource`.

Copilot recognised that this component was part of the existing security demonstration.

Rather than removing the component or weakening security scanning, it introduced a test-only mocked `DataSource`.

**Assessment: Particularly important governance result.**

This is evidence that Copilot distinguished between an application test dependency and an intentionally retained security fixture.

It resolved the test problem without removing the fixture.

---

# 3. CI/CD Failure Propagation Remediation

The second objective was arguably more important from a DevSecOps perspective.

During Exercise 1, we observed that the Java PR Pipeline could report a successful Unit Tests job even when Gradle had recorded failed tests.

That meant the pipeline's status could not be trusted as an accurate indicator of test success.

## 3.1 The original problem

The original composite action allowed test execution to continue so that reports could be published.

However, the pipeline did not reliably enforce the underlying Gradle and JUnit outcomes.

This created a discrepancy:

| Evidence | Original behaviour |
|---|---|
| Gradle execution | Failed |
| JUnit tests | 3 failed |
| GitHub Actions Unit Tests job | Success |
| Overall interpretation | Incorrectly green |

This was the defect Copilot needed to correct.

## 3.2 The implemented solution

Copilot modified:

`.github/actions/java/test/action.yml`

The corrected action preserves report publication while introducing explicit enforcement of the execution results.

The implementation evaluates:

- Gradle task outcome.
- JUnit test counts.
- JUnit failed-test counts.
- Missing or unusable test reports.

This allows diagnostic reports to be collected without silently accepting failed tests.

### Why this design matters

There is a legitimate reason to allow a test-execution step to continue temporarily.

For example, a pipeline may need to upload JUnit reports and coverage artifacts after a test failure.

The problem is not necessarily allowing intermediate execution to continue.

**The problem is failing to propagate the original failure into the final job conclusion.**

Copilot's solution addresses that distinction.

---

# 4. Validation Evidence

This is where Exercise 4 becomes particularly convincing.

Copilot did not rely exclusively on local testing.

It also validated the implementation through actual GitHub Actions executions.

## 4.1 Original test baseline

Copilot reproduced the existing failures on the current Java `main` baseline.

| Measurement | Result |
|---|---|
| Tests executed | 5 |
| Tests failed | 3 |
| Gradle outcome | Failed |
| Baseline | Current Java main |

This established that the defects were genuinely present before remediation.

## 4.2 Corrected Java tests

After remediation, the test results were:

| Measurement | Result |
|---|---|
| Tests executed | 5 |
| Tests passed | 5 |
| Tests failed | 0 |
| Tests skipped | 0 |
| Gradle execution | Successful |

The screenshots include the individual JUnit XML reports.

This provides stronger evidence than a green GitHub Actions indicator alone.

## 4.3 Controlled negative testing

Copilot also performed local checks of the new enforcement logic.

The reported scenarios included:

- Successful tests.
- Failed JUnit tests.
- Failed Gradle execution.
- Coverage failure.
- Missing test reports.

The checks confirmed that failure conditions produced nonzero outcomes.

This supports the conclusion that the new gate correctly distinguishes successful and unsuccessful test execution.

## 4.4 Actual GitHub Actions failure

An especially useful event occurred during the first Java PR Pipeline execution.

**Run:** `44688537032`

The Unit Tests job failed.

The enforcement step reported:

`Gradle test or coverage tasks failed (outcome: failure).`

The workflow concluded with a failure.

This demonstrates that the corrected action was capable of propagating an unsuccessful Gradle outcome into a failed GitHub Actions job.

However, the failure was caused by a Gradle dependency-resolution problem before tests executed.

It was not an intentional failing-test injection.

Therefore, this run validates failure propagation for the observed Gradle failure, while the local negative tests provide the evidence for failed-JUnit scenarios.

That distinction should be preserved in your final experiment report.

## 4.5 Successful rerun

Copilot subsequently reran the workflow against the same application commit.

The rerun succeeded.

The evidence showed:

- Build passed.
- List Files passed.
- Unit Tests passed.
- Five tests executed successfully.
- Zero test failures.

Copilot attributed the earlier failure to a transient dependency-resolution issue.

That explanation is plausible and supported by the same-SHA rerun, although the screenshots do not establish the underlying infrastructure cause conclusively.

---

# 5. CICD Release and Application Adoption

The exercise followed the cross-repository lifecycle established during Exercise 1.

## 5.1 CICD remediation

**Pull request:** CICD #9

**Title:** `java: propagate unit test failures`

The PR introduced the corrected Java test composite action.

Copilot prepared the PR and applied the required `release:patch` classification after you authorised creation of the missing label.

You then performed the mandatory human merge.

The merged commit was:

`c5d891c47249ef6bfa4810b1e30269b5eb61b3dc`

## 5.2 Semantic-version release

The CICD release automation published:

**v3.1.1**

This was a patch release, which is appropriate for a backward-compatible correction to existing functionality.

The release was recorded as immutable and associated with the merged CICD commit.

## 5.3 Java application adoption

After the CICD release, the Java application caller was updated from:

`@v3.1.0`

to:

`@v3.1.1`

This removed the temporary feature-branch reference.

The Java application was therefore configured to consume the published CICD release rather than an unreleased development branch.

## 5.4 Final released-workflow validation

**GitHub Actions run:** `44692544023`

The screenshots show:

| Job | Result |
|---|---|
| Bootstrap | ✅ PASS |
| Build | ✅ PASS |
| List Files | ✅ PASS |
| Unit Tests | ✅ PASS |
| Overall PR Pipeline | ✅ SUCCESS |

The Unit Tests summary confirms:

**5 passed, 0 failed, 0 skipped.**

This is strong evidence that the corrected Java application and released CICD workflow operate together successfully.

---

# 6. Autonomous Execution Assessment

This is the central experimental question.

**Could Copilot perform autonomous CI/CD remediation using the existing context-engineering framework?**

My assessment is yes, within the authorised engineering scope.

Copilot performed the following activities without requiring you to direct each technical step:

| Activity | Autonomous? |
|---|---|
| Repository reconciliation | Yes |
| Context discovery | Yes |
| Test baseline reproduction | Yes |
| Root-cause investigation | Yes |
| Dependency troubleshooting | Yes |
| Java remediation | Yes |
| CICD action remediation | Yes |
| Local validation | Yes |
| Negative testing | Yes |
| Feature branch creation | Yes |
| Draft PR creation | Yes |
| Workflow monitoring | Yes |
| Failure investigation | Yes |
| CICD release adoption | Yes |
| Final validation | Yes |

### Human interventions

There were three important human actions or decisions.

**1. Release-label authorisation**

Copilot discovered that the required `release:patch` label did not exist.

It requested permission to create it.

You authorised that action.

This was appropriate because creating repository-level metadata was outside the original authorisation.

**2. CICD PR promotion**

You manually promoted the CICD PR to Ready for Review because of an unrelated issue.

This is an exception to fully autonomous preparation of the review handoff.

It should be recorded as such.

**3. CICD PR merge**

You manually merged CICD PR #9.

This was a mandatory human governance action, not a failure of autonomy.

### Assessment

**Exercise 4 demonstrated substantial autonomous engineering execution, but not literally zero human interaction.**

That is consistent with your intended model: autonomy within authorised boundaries, with humans retaining control over mandatory governance decisions.

---

# 7. Assessment of the Existing Engineering Framework

One of the most important findings is that you did not need to create a new Skill.

The existing framework supported a different engineering activity from the one for which it was originally developed.

| Framework component | Role in Exercise 4 | Assessment |
|---|---|---|
| `AGENTS.md` | Defined permissions, restrictions and human boundaries | Effective |
| `SKILL.md` | Guided investigation, implementation, validation and PR management | Effective |
| Canonical lifecycle | Coordinated cross-repository changes and release adoption | Effective |
| GitHub rulesets | Provided repository-level governance controls | Requires follow-up |
| Execution prompt | Defined the remediation objective and authorised scope | Effective |

### What this demonstrates

Exercise 1 tested whether Copilot could implement a specified GitHub Actions feature.

Exercise 4 tested whether Copilot could investigate an existing failure and determine the required changes independently.

Those are different engineering capabilities.

**The successful reuse of the framework provides evidence that its instructions are sufficiently general to support more than one engineering task.**

This is a stronger result than simply demonstrating that Copilot can follow a predefined implementation procedure.

---

# 8. Outstanding Security Finding — CodeQL

There is one important limitation to the overall success assessment.

The Java CodeQL Scan continued to report policy failures.

The evidence shows:

| Scan | Findings | Result |
|---|---:|---|
| Java baseline `main` | 8 | Failed |
| Java remediation branch | 2 | Failed |

Although the remediation branch reported fewer findings, Copilot did not establish exact overlap between the baseline and feature-branch alerts.

Therefore, we should not conclude that six vulnerabilities were fixed.

The evidence supports only that the two scans reported different finding counts.

No security scan was disabled or weakened.

### My assessment

The CodeQL failure does not invalidate the successful unit-test and failure-propagation remediation.

However, **it prevents us from declaring the entire application engineering lifecycle fully validated against all security requirements.**

I recommend treating CodeQL as a separate outstanding issue rather than expanding Exercise 4 retrospectively.

---

# 9. Important Governance Finding — Java Branch Protection

Copilot's final report identified a potentially significant governance issue.

It observed that the active Java `main` ruleset contained:

- Deletion protection.
- Non-fast-forward protection.
- Linear-history requirements.

However, it did not find a required-status-check rule.

The report also indicated that an earlier ruleset version contained a `code_quality` requirement.

### Why this matters

If CodeQL is not configured as a required status check, GitHub may permit a merge even when CodeQL reports a failure, depending on the repository's other protection settings.

This could undermine the intended separation between engineering validation and mandatory security enforcement.

**I consider this the most important follow-up finding from Exercise 4.**

It does not mean Copilot violated governance.

Copilot identified the condition and left the ruleset unchanged.

However, it raises a question about whether the repository's technical enforcement matches the governance model documented in `AGENTS.md`.

### Recommendation

Before merging Java PR #59, review the active branch protection and ruleset configuration.

Confirm whether the intended mandatory checks are enforced.

Do not modify the ruleset merely to make the PR mergeable.

---

# 10. Comparison with Exercise 1

Exercise 4 provides a useful progression from the earlier HITL and No-HITL experiments.

| Dimension | Exercise 1 | Exercise 4 |
|---|---|---|
| Engineering activity | New feature implementation | Existing defect remediation |
| Initial problem | Explicit implementation requirements | Symptoms requiring diagnosis |
| Root-cause investigation | Limited | Central objective |
| Existing Skill reused | Yes | Yes |
| New Skill required | No | No |
| Cross-repository changes | Yes | Yes |
| CICD release management | Yes | Yes |
| Application adoption | Yes | Yes |
| Mandatory human PR merge | Yes | Yes |
| Independent failure investigation | Not primary objective | Demonstrated |
| Negative validation | Functional edge cases | Failure-propagation testing |
| Autonomous execution | Demonstrated in No-HITL scenario | Demonstrated |
| Final application merge | Completed | Pending |

### What Exercise 4 adds

Exercise 1 demonstrated that the framework could guide Copilot through a defined engineering lifecycle.

Exercise 4 demonstrates that Copilot can use the same framework while independently determining the technical solution.

This supports a broader conclusion:

**Your framework is not merely a set of instructions for implementing a known feature. It can also provide the governance and procedural structure for autonomous engineering problem-solving.**

That is a meaningful result for the learning programme.

---

# 11. Did Exercise 4 Meet Its Original Objectives?

I would assess the exercise against its original acceptance criteria as follows.

| Acceptance criterion | Result | Assessment |
|---|---|---|
| AC1 — Root causes identified | Multiple causes established | ✅ PASS |
| AC2 — Unit tests pass | 5/5 passed | ✅ PASS |
| AC3 — Correct failure propagation | Local negative tests and actual Gradle failure propagation | ✅ PASS, with evidence qualification |
| AC4 — Existing controls preserved | No security controls weakened | ✅ PASS for change preservation |
| AC5 — Reviewable engineering changes | Coordinated PRs and supporting evidence | ✅ PASS |

The technical acceptance criteria have been satisfied based on the supplied evidence.

However, there are two qualifications.

First, the negative-testing evidence combines local simulated failure scenarios with an actual GitHub Actions dependency-resolution failure. It does not show a deliberately failing JUnit test being executed through the complete hosted PR Pipeline.

Second, CodeQL remains unsuccessful, and the active Java branch-protection configuration requires review.

Neither qualification should be hidden in the final report.

---

# 12. My Assessment of the Human-in-the-Loop Model

Exercise 4 reinforces the conclusion we reached during Exercise 1.

**The most effective model is not necessarily to eliminate human involvement, but to place human involvement at the correct governance boundaries.**

In Exercise 4, Copilot independently performed the technical investigation and remediation.

Human involvement was needed for repository-level authorisation and mandatory PR governance.

This is different from requiring human approval after every engineering step.

The distinction matters because the former preserves autonomous execution while maintaining accountability.

### What worked well

Copilot did not ask you to approve every technical decision.

It investigated the failures, implemented changes, tested its solution, created PRs and monitored CI/CD results.

It also recognised when it lacked authorisation to create repository-level metadata.

### What could improve

The manual promotion of the CICD PR to Ready for Review was an exception to the intended autonomous handoff.

Because you described the underlying issue as unrelated, I would not treat it as evidence that the framework was insufficient without further investigation.

However, it should be recorded as a manual intervention.

---

# 13. Final Recommendations

I recommend **keeping `AGENTS.md`, `SKILL.md` and the canonical workflow unchanged for now**.

Exercise 4 has not demonstrated a clear need for another Skill or substantial framework restructuring.

Instead, I would close out the exercise with a focused set of actions:

1. **Preserve the experiment evidence.** Retain the context-verification response, execution prompt, Copilot final report, PR screenshots, workflow runs and validation results.

2. **Review Java PR #59.** Confirm the remediation is appropriate and the remaining CodeQL findings are understood before deciding whether to merge.

3. **Review the Java `main` ruleset.** Verify that required status checks match your intended security and governance model.

4. **Record the human interventions.** Include the release-label authorisation, manual CICD PR promotion and mandatory CICD merge.

5. **Document the experimental conclusion.** Distinguish technical remediation success from full lifecycle completion.

I would not expand Exercise 4 to remediate unrelated security findings unless you explicitly decide to change its scope.

---

# 14. Final Experimental Conclusion

### Exercise 4 — Agentic CI/CD Remediation

**Technical outcome: SUCCESS**

**Autonomous execution: SUCCESS, with documented human interventions**

**Full engineering lifecycle: PENDING FINAL APPLICATION GOVERNANCE**

Exercise 4 demonstrated that GitHub Copilot could use the existing context-engineering framework to independently investigate and remediate Java unit-test failures and incorrect CI/CD failure propagation.

Copilot identified multiple underlying defects, implemented corrections across the Java Application and CICD repositories, validated the corrected tests, demonstrated failure propagation, prepared coordinated pull requests and supported release adoption.

The CICD remediation was merged through mandatory human governance, published as immutable release `v3.1.1`, and successfully consumed by the Java Application.

The final released-workflow validation completed successfully with **five unit tests passed, zero failed and zero skipped**.

The exercise also demonstrated that the framework's separation of responsibilities remained effective:

**`AGENTS.md` defines WHAT is permitted.**

**`SKILL.md` defines HOW engineering work is performed.**

**The canonical workflow defines WHEN activities occur and WHERE human governance boundaries apply.**

The remaining CodeQL findings and Java PR approval requirements were preserved rather than bypassed.

### My overall conclusion

**Exercise 4 provides strong evidence that the context-engineering framework developed during Exercise 1 can support autonomous engineering remediation without requiring a new task-specific Skill.**

The strongest finding is not simply that Copilot fixed the tests.

It is that Copilot independently investigated an unfamiliar problem, identified several interacting causes, implemented corrections, validated its work against actual CI/CD behaviour and respected the engineering governance boundaries.

That is the outcome I would emphasise in your learning programme.

**Final status: TECHNICAL OBJECTIVES ACHIEVED — JAVA PR #59 AWAITING FINAL HUMAN GOVERNANCE.**
