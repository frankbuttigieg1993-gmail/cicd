---
name: github-actions-development
description: Develop and validate GitHub Actions composite actions and reusable workflows across cicd and consuming application repositories; manage cross-repository Draft PRs, semantic-version release labels, immutable CICD releases, post-release application adoption, functional log verification, and review handoff.
---

# GitHub Actions development - versioned release runbook

## Human quick reference

Read `cicd/.github/Standard CICD Engineering, Release & Application Promotion Workflow.md` at the start of every relevant task. Its 16-step sequence is the canonical workflow; this Skill describes **how** to execute it. This is the only shared CI/CD execution Skill; consuming application repositories use their own `AGENTS.md` policies rather than duplicate Skills. The applicable `AGENTS.md` files define **policy** and take precedence for repository-specific authorisation and safety. Do not substitute a previous conversation summary for the actual file.

| Stage | Steps | Result |
|---|---|---|
| Select, discover, plan | 1-2 | Scope, acceptance criteria, conventions |
| Implement and locally test | 3-5 | Branches, minimal changes, local checks |
| Draft PRs and label | 6-7 | Cross-linked Draft PRs; exactly one release label |
| Validate unreleased CICD | 8 | Workflow/job/step logs and functional evidence |
| CICD review, merge, release | 9-11 | Human-reviewed CICD merge; immutable tag on merged SHA |
| Application adoption and final test | 12-13 | Application caller pinned to new tag; fresh logs |
| Application review and handoff | 14-16 | Review request, human merge, final report |

## Phase A - Steps 1-2: selection, discovery and plan

1. For existing-pipeline integration, require explicit PR Pipeline or Build Pipeline selection **before repository/tool operations**. If absent, report `BLOCKED - AWAITING USER INPUT` and stop. Treat selection as authorisation for the selected CICD workflow; PR Pipeline selection also covers narrowly necessary `java_application/.github/workflows/pr.yml` caller edits. Other existing workflow edits require file-specific approval.
2. Read the latest applicable `AGENTS.md` files, this Skill, and the canonical workflow document at its exact path. Check for conflicts and missing files.
3. Identify testable acceptance criteria, target pipeline, expected directory or other inputs, cross-repository caller, dependencies and release consumers. Do not invent requirements.
4. Inspect at least two comparable composite actions where available and relevant workflows. Summarise conventions for `action.yml`, `shell`, inline `run`, Gradle wrapper, checkout paths, job ordering and error handling. Explain deviations.
5. Plan minimal authorised changes and tests. Preserve unrelated work; check branch divergence before branching. Never manufacture a dummy second PR.

## Phase B - Steps 3-5: branches, implementation and local validation

1. Create task branches from verified `main` baselines in each meaningfully affected repository; use isolated worktrees to preserve unrelated local changes where needed. Never push directly to `main`.
2. Implement the smallest change. Prefer inline Bash commands and `./gradlew` conventions. For <=10 executable shell lines, a separate helper script requires explicit approval unless the governing policy explicitly permits an exception.
3. For internal composite actions referenced from a CICD reusable workflow, prefer verified self-repository syntax `uses: $/.github/actions/<action-path>` so actions track the workflow's CICD revision. Do not add permanent checkout or `cicd-ref` inputs solely for testing. Verify correct resolution in the actual execution environment.
4. For PR Pipeline integration, temporarily point the authorised application caller to the matching CICD feature branch; preserve unrelated workflow configuration. Do not alter the unselected Build Pipeline.
5. Validate YAML, composite metadata, dependencies, workflow-call compatibility, permissions, action references, Gradle/tests as appropriate, and `git diff --check`. Record results.

## Phase C - Steps 6-8: Draft PRs, release label, feature validation

1. Commit and push only task changes. Create cross-linked **Draft** PRs in CICD and affected application repository/repositories before final integration validation. Target `main`; record temporary refs, acceptance criteria and planned evidence.
2. Classify CICD change: `release:patch` (backward-compatible fix), `release:minor` (backward-compatible feature), or `release:major` (breaking change). Apply **exactly one** label to the CICD PR and verify via GitHub that it is present. Explain rationale; if ambiguous, request clarification. Do not assume the release workflow will infer the label.
3. Execute the application PR pipeline against the CICD feature branch. Identify run URL/ID, latest application SHA, workflow, jobs and executing steps. Inspect **actual logs**, not just success status. Compare output to acceptance criteria and known expected contents/artifacts, including hidden entries for listing tasks.
4. Classify failures and remediate only authorised, task-related causes. Never weaken scans, bypass checks, or call skipped/absent checks successful. Document accepted pre-existing findings separately from new regressions. Update evidence in both Draft PRs.

## Phase D - Steps 9-11: CICD review, merge and release

1. Verify feature-branch evidence, CICD required checks, exactly one release label, and that internal action references will remain valid after branch deletion. Confirm CICD PR has no temporary internal action references; promote **CICD PR only** to Ready for Review when applicable conditions are met.
2. Request review from `frankbuttigieg-93` if GitHub permits. The agent MUST NOT directly approve or merge. Wait for a human-authorised merge or separately authorised GitHub auto-merge; do not claim that the agent can wait indefinitely in the background.
3. Once the merge is observed, confirm the actual CICD merged SHA and the release workflow result. Verify the published immutable semantic-version tag points to that SHA, represents the whole CICD repository, and is protected against moving or deletion. Do not create/move tags or install automation unless authorised for the task. If release automation fails, report the blocker rather than inventing a tag.

## Phase E - Steps 12-13: application adoption and final verification

1. Once the new tag is published, update only the affected application Draft PR caller from the temporary CICD feature ref to the new immutable release tag (e.g. `@v2.3.0`). Use configured cross-repository automation where available; otherwise perform an authorised change or report that automation is not configured. Do not silently change unrelated applications.
2. Push the application feature branch and confirm a fresh PR validation run actually starts (token identity and event rules can affect triggers). Confirm the released reusable workflow and its self-repository actions resolve.
3. Inspect workflow/job/step conclusions and actual executing logs. Compare expected vs observed functional results on the latest application SHA. Confirm no temporary feature refs remain in the intended merged application workflow. Record links, tag and CICD merged SHA, application SHA, relevant logs and accepted limitations in the application PR.

## Phase F - Steps 14-16: review, merge handoff and report

1. Only after applicable application checks and release-based functional verification pass, promote the application PR to Ready for Review and request `frankbuttigieg-93` where permitted. A reviewer request is not an approval.
2. Human reviewers approve and merge through GitHub governance; the agent never directly merges or bypasses rulesets. Do not claim merge completion without observing it.
3. Report both PR URLs, branch names, changed files, release label and rationale, immutable release tag and merged SHA, latest application SHA, workflow runs, job/step statuses, inspected logs, expected-vs-observed outcomes, reviewer status, known findings and remaining blockers. Delete temporary branches only when explicitly authorised and no refs depend on them.

## State and safety rules

- `BLOCKED - AWAITING USER INPUT`: missing/ambiguous pipeline or release classification.
- `BLOCKED - AWAITING USER APPROVAL`: out-of-scope existing workflow change.
- `IN DEVELOPMENT`: Draft PR or validation/release transition pending.
- `UNVERIFIED`: required functional evidence unavailable; do not promote.
- `READY FOR HUMAN REVIEW`: the applicable PR's own promotion gate passed.
- A green workflow does not establish functional correctness. A CICD release does not establish that an application adopted it. Keep these gates separate.
- A request for a supervised execution may add task-specific checkpoints; do not treat those as permanent requirements of the standard process.
