# Exercise 4 — Copilot Read-Only Context Verification Response

> Verbatim transcription of the Copilot response supplied by the user.

## Files Read

**Instruction files accessed by repository-relative path:**

- CICD: `AGENTS.md`
- Java Application: `AGENTS.md`
- CICD: `.github/skills/github-actions-development/SKILL.md`
- CICD: `.github/Canoncial Engineering Lifecycle.md`

**Relevant workflow, action, build, and test files:**

- CICD: `.github/workflows/java-build-pr.yml`
- Java Application: `.github/workflows/pr.yml`
- CICD: `.github/actions/java/test/action.yml` and `.github/actions/java/test/README.md`
- CICD comparable action: `.github/actions/java/build/action.yml`
- Java Application: `build.gradle`, `gradle/wrapper/gradle-wrapper.properties`, and representative tests `EnvironmentValueServiceTest.java` and `EnvLoggerSchedulerTest.java`
- Exercise context: `Exercise_4_Autonomous_Execution_Prompt.md`

The three-layer relationship is clear: **`AGENTS.md` defines what is permitted; `SKILL.md` describes how to execute; the canonical workflow defines when and in what order.** The Java Application policy points to the shared CICD Skill and does not require a duplicate application Skill.

## Context and Scope

- `frankbuttigieg1993-gmail/cicd` owns reusable workflows and composite actions. `frankbuttigieg1993-gmail/java_application` owns Java source, Gradle, tests, and caller workflows.
- The user explicitly selected **PR Pipeline** and authorized investigation of both reported issues, plus changes to the named PR workflow/action and directly relevant Java code, tests, or Gradle configuration when justified by confirmed evidence. The **Build Pipeline is not selected**.
- The test action is tracked in CICD, not in the Java Application workspace. Its current configuration includes a Gradle invocation with `-PignoreFailures=true` and `continue-on-error: true`; its README describes an independent test-result gate. This is a static observation for later investigation—not a root-cause conclusion.
- The operator-reported current test failures have **not** been independently reproduced.

## Current Repository State

- CICD local `main`, cached `origin/main`, and live remote `main` match at `ca3489823b1f42a9769fd12141814030b6c3f144`.
- Java Application local `main`, cached `origin/main`, and live remote `main` match at `fd7eda894017859291f66e654ce8a2f28f86f29a`, dated 2026-11-20 with commit message “Updating AGENTS.md.” This verifies the reported main update reached the remote.
- The Java Application main worktree is clean. CICD has pre-existing modifications to the two Exercise 4 prompt documents; preserve them. Do not overwrite or revert them.
- There are no current Exercise 4 PRs. Java has unrelated open Dependabot PRs; CICD has no open PRs. Historical [CICD #8](https://github.com/frankbuttigieg1993-gmail/cicd/pull/8) and [frankbuttigieg1993-gmail/java_application#58](https://github.com/frankbuttigieg1993-gmail/java_application/pull/58) are merged. Their associated feature branch remains in local/remote refs, but its linked worktree paths are missing and marked prunable. Avoid relying on those stale paths or reusing the historical branch without reconciliation.
- A Java **Build Pipeline** run, [44684590632](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44684590632), was already queued on the current Java main SHA when observed. It was not triggered during this task; no logs or outcome were available.

## Authorisation and Governance

PR Pipeline authorization covers the intended investigation and narrowly necessary changes in the selected workflow and Java PR caller. It does not authorize Build Pipeline edits, unrelated workflows or functionality, governance files, settings, protections, infrastructure, IAM, or weakening security and quality controls.

There is a **conditional policy tension**: the exercise prompt says to follow an application-only PR lifecycle if only Java changes are needed, while CICD `AGENTS.md` says that when only one repository needs a meaningful change, do not invent a second change and request direction regarding the two-PR convention. The stricter repository policy must be respected: this does not block the authorized investigation, but if findings establish a Java-only remediation, obtain direction before proceeding with an application-only PR lifecycle.

The single-execution request removes extra experimental checkpoints; it does not remove mandatory human review, approval, and merge boundaries.

## Lifecycle and Validation

The canonical 16-step lifecycle applies. If both repositories need meaningful changes, later execution must use coordinated branches and Draft PRs, apply exactly one justified CICD release label, validate the feature branch with actual workflow/job/step logs, and stop for human CICD review and merge. Only after an immutable release exists may the application caller adopt it and undergo fresh validation. Never change the unselected Build Pipeline or merge PRs directly.

Later validation must establish genuine test success (expected tests execute, zero failures/errors, Gradle succeeds, and reports agree), and verify failure propagation with actual logs. Use a controlled, isolated negative test where feasible; ensure temporary test changes are excluded from the final PR. Confirm existing scans, quality gates, permissions, triggers, and unrelated behavior remain intact. Workflow green status alone is insufficient.

## Conflicts and Gaps

- No governing instruction file was missing. The only noted policy tension is the conditional application-only PR case above.
- No current local test-result reports were found. The latest completed Java PR Pipeline evidence is historical: [run 44217333120](https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44217333120) used Java SHA `9337fe41103302e4f88fd1aca81addba22e84b9d`, not current `main`. Its logs report **5 tests completed, 3 failed** and `BUILD FAILED`, while the `Java Test` step and `CI / Unit_Tests` job concluded success. The merged PR record corroborates this. This is historical evidence only and does not establish current test behavior.
- No tests were run, workflows triggered, files modified, branches created, or PRs changed during this read-only verification. Fresh test evidence is a later execution baseline, not a context blocker.

## Decision

The governing instructions are accessible, the PR Pipeline investigation is authorized, and the current main refs are synchronized. Preserve the existing CICD prompt edits and avoid the stale linked worktree paths. The conditional Java-only PR restriction must be honored if that outcome arises.

STATUS: CONTEXT VERIFIED — READY FOR EXERCISE 4
