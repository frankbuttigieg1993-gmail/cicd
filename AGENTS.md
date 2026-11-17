# Engineering Agent Instructions — CI/CD and Java Application

## Human quick reference — standard 16-step process

The detailed canonical process is `cicd/.github/Standard CICD Engineering, Release & Application Promotion Workflow.md`. This table is a quick reference; repository policy below governs authorisation and completion.

| Step | Activity |
|---|---|
| 1 | Requirements Analysis and Pipeline Selection |
| 2 | Repository Convention Discovery and Planning |
| 3 | Create CICD Feature Branch |
| 4 | Create Application Feature Branch |
| 5 | Perform Local Validation |
| 6 | Create Both Draft PRs |
| 7 | Classify the CICD Release and Apply the PR Label |
| 8 | Execute End-to-End Feature-Branch Validation |
| 9 | Promote CICD PR to Ready for Review |
| 10 | Review and Merge CICD PR |
| 11 | Automatically Create the Semantic-Version Release |
| 12 | Update the Application Draft PR |
| 13 | Execute Final Application Validation |
| 14 | Promote Application PR to Ready for Review |
| 15 | Final Human Review and Merge |
| 16 | Final Reporting and Cleanup |

## 1. Repository responsibilities

- `frankbuttigieg1993-gmail/cicd` owns reusable workflows and composite actions.
- `frankbuttigieg1993-gmail/java_application` owns application code, Gradle configuration, tests and caller workflows.
- Read applicable instructions in **each** repository; instructions are not automatically inherited across repositories. The single `cicd/.github/skills/github-actions-development/SKILL.md` is the authoritative cross-repository execution runbook; no duplicate application Skill is required. This file is the authoritative CICD policy.

## 2. Mandatory pipeline selection and authorisation

For tasks integrating into an existing pipeline, require explicit selection in the **current task or an explicit follow-up** before **any repository reads or other tool operations**:

| Selection | Authorised existing workflow in `cicd` |
|---|---|
| **PR Pipeline** | `.github/workflows/java-build-pr.yml` and narrowly scoped `java_application/.github/workflows/pr.yml` integration |
| **Build Pipeline** | `.github/workflows/java-build-all.yml` |

- Selection **is authorisation** for minimal changes directly necessary for the requested functionality in the selected workflow. **Do not ask for redundant approval.**
- If missing or ambiguous, report **BLOCKED - AWAITING USER INPUT**, ask which pipeline to use and stop **all** execution (including reads, branching, edits, tests, commits, pushes and PRs). Never infer a default from prior tasks.
- If the user explicitly requests both pipelines, clarify that both are intended before modifying both.
- **PR Pipeline** selection also authorises narrowly scoped changes to `java_application/.github/workflows/pr.yml` **only when necessary** for cross-repository integration or validation of the requested feature. This includes temporarily changing the reusable-workflow reference from `@main` to the matching `cicd` feature branch. No second approval is required for that specific change.
- Preserve all unrelated caller workflow jobs, triggers, permissions, checks and behaviour. Record the temporary feature-branch reference, dependency, intended stable reference and required merge order in both PRs. Do not replace the temporary CICD feature ref with a release tag until the release exists; do not merge automatically.
- The unselected `cicd` workflow must remain unchanged. Any **other existing workflow** (including any Java workflow other than the narrowly authorised `pr.yml`) requires separate file-specific authorisation. If needed, stop **all** execution, explain the proposed change and report **BLOCKED - AWAITING USER APPROVAL** until granted.
- Creating a new caller workflow is permissible if task-related and consistent with other boundaries; do not manufacture changes merely to generate a second PR.

## 3. Engineering standards and repository conventions

- Before implementation, inspect at least two comparable existing actions where available. Identify naming, `action.yml` structure, `shell`, inline `run`, Gradle wrapper commands, inputs/outputs, error handling and dependencies. Summarise observed patterns and intended approach in the plan.
- Prefer existing **safe, correct** conventions and the simplest solution. Explain necessary deviations.
- Use `.github/actions/<name>/action.yml`, `runs.using: composite` and an explicit `shell` for each `run` step.
- Prefer one-line inline commands (`ls -alrt`, `./gradlew build`, `./gradlew test`) where appropriate; use the repository's Gradle wrapper. Do not create a helper script for a trivial command.
- For **10 or fewer executable shell-command lines**, keep logic inline; a separate script requires explicit approval. Above 10 lines, a script is optional, not automatic. Correctness, security and maintainability take precedence; never pad commands to exceed the threshold.
- Use `workflow_call` for reusable workflows, least-privilege permissions and correct failure propagation. Verify `needs` ordering, event triggers and checkout paths: `./.github/actions/...` resolves in the checked-out workspace, not automatically in `cicd`.
- Track temporary cross-repository feature-branch refs and document the intended reviewed stable ref. Do not invent immutable SHAs.

## 4. Change boundaries and security

- Never push to `main`, overwrite unrelated work, edit unrelated pipelines, change secrets/settings/rulesets, deploy infrastructure, disable tests or weaken security scans/checks.
- Preserve existing stages, triggers, dependencies, permissions and checks unless specifically authorised. Pipeline selection authorises **integration**, not unrelated behavioural changes.
- Existing composite actions and governance files (`AGENTS.md`, Skills) are read-only unless the task explicitly authorises their modification. Existing workflows are read-only except the selected `cicd` workflow and, for PR Pipeline tasks, the narrowly authorised `java_application/.github/workflows/pr.yml` integration.
- Create feature branches in both repositories when each has meaningful task-related changes. If only one repository needs a meaningful change, **do not invent one**: report the conflict with the two-PR convention and request direction.
- Tool access and GitHub permissions are enforceable controls; these written rules alone are behavioural guidance.

## 5. Pull request governance

- Push approved branches and create **Draft** PRs targeting `main`, cross-linking related PRs. Include change scope, acceptance criteria, planned validation, run URLs/IDs, head SHAs, evidence and temporary refs.
- Keep each applicable PR Draft while its stage-specific implementation, required checks, or functional verification is incomplete. The application PR remains Draft while the CICD PR is reviewed, merged, released, and the application revalidates the immutable release.
- Promote the CICD PR to **Ready for Review** after successful feature-branch integration evidence and applicable required checks. After human CICD merge and immutable release, promote the application PR separately only after final validation against that release and applicable required checks. Do not promote solely because a workflow is green.
- Then request review from `frankbuttigieg93-png`. If GitHub refuses (e.g. author cannot review own PR), report the limitation; do not impersonate, self-approve, substitute a reviewer without direction or merge.

### GitHub Actions Reference Management and Production Readiness

The agent MUST ensure that all new or modified GitHub Actions workflows have a safe, maintainable reference strategy before being considered ready for production.

Temporary feature-branch references MAY be used for cross-repository integration testing and PR validation.

However, the agent MUST NOT leave a workflow intended for merging into `main` dependent on a temporary feature branch that may subsequently be deleted.

Before promoting a Draft PR to Ready for Review, the agent MUST:

1. Identify all new or modified references to reusable workflows and composite actions.
2. Distinguish temporary validation references from intended production references.
3. Establish a safe final reference strategy using an appropriate stable reference, immutable commit SHA or local action reference.
4. Ensure that the proposed merged workflow will not depend on temporary feature branches.
5. Document CICD-first merge dependencies, immutable tag publication, and application reference transitions.
6. Verify that the final reference strategy is technically valid and compatible with the repository's engineering conventions.
7. Revalidate any implementation changes made to establish the final reference strategy.

### PR Promotion Requirements

A Draft PR MUST NOT be promoted to Ready for Review unless:

- Required CI/CD checks have passed.
- The requested functionality has been verified using actual execution evidence.
- The final reference strategy has been established and documented.
- The intended merged CICD workflow has no temporary internal action references; the application caller must transition to the published immutable CICD tag before its own promotion and merge.
- The post-CICD-merge application reference transition and final validation are documented and assigned to authorised automation or a human operator; they are not claimed complete prematurely.

The agent MUST NOT directly merge pull requests or modify protected branches to resolve reference dependencies. A human or authorised GitHub auto-merge may merge after applicable protections and approvals are satisfied.

## 6. Mandatory execution and functional verification

A green workflow/job/step **does not by itself prove functionality**. For each new or modified feature:

1. Identify the workflow, run ID/URL, head SHA, job and specific executing step.
2. Confirm workflow, job and step ran (not skipped) and record their conclusions.
3. **Retrieve and inspect the actual step/job execution logs**, not just statuses.
4. Confirm the expected command executed; compare observed output with acceptance criteria. For a file-listing action, verify the target directory and expected entries, including hidden files, using a known baseline or appropriate test artifact—not merely plausible-looking output.
5. Capture relevant log excerpts or artifacts and expected-versus-observed results in both relevant PRs and the final report.
6. If logs are insufficient, obtain another appropriate authorised test artifact. Mark **UNVERIFIED** if evidence remains inadequate; leave PRs Draft.

## 7. Failure handling and completion

- Classify failures (code, test, workflow, action, permissions, external dependency); inspect logs, make the smallest authorised correction, push to the same branch and rerun the necessary checks.
- Do not bypass triggers or required checks. If an authorised run cannot be triggered, report the blocker rather than modifying `main`.
- Report **IN DEVELOPMENT** while Draft PRs are progressing; **BLOCKED - AWAITING USER INPUT** for missing pipeline selection; **BLOCKED - AWAITING USER APPROVAL** for out-of-scope workflow edits (excluding the authorised Java PR caller reference); **BLOCKED** for external constraints; **READY FOR HUMAN REVIEW** only when promotion requirements are satisfied; **FAILED** when the task cannot be completed.
- Final report: both applicable PR URLs, branches, SHAs, changed files, tests, run links, step logs, functional results, reviewer-request outcome, risks and any unresolved limitations. Never claim human approval or merge.

## 8. Versioned CICD release and application adoption policy

- **Canonical process:** Before planning or implementation, read `.github/Standard CICD Engineering, Release & Application Promotion Workflow.md` in this repository. It is the authoritative *sequence* of 16 steps. This `AGENTS.md` remains authoritative for policy; the Skill supplies operational instructions. Report contradictions instead of silently choosing one.
- **Single version:** Release the entire `cicd` repository as one semantic version, not individual actions or workflows. For internal composite actions in CICD reusable workflows, prefer the verified self-repository syntax `uses: $/.github/actions/<path>` where supported. Do not add permanent checkout steps or `cicd-ref` inputs merely to support pre-merge testing.
- **Draft PRs first:** Create cross-referenced Draft PRs in `cicd` and each meaningfully affected application before final feature-branch integration testing. Application callers temporarily reference the matching CICD feature branch. Preserve existing stable version references in unaffected application repositories.
- **Release classification:** Every CICD PR governed by semantic-release automation MUST have **exactly one** of `release:patch`, `release:minor`, `release:major` before promotion to Ready for Review. The agent MUST inspect the diff, select the appropriate classification, apply and verify the label, and record the rationale. If ambiguous, report **BLOCKED - AWAITING USER INPUT**; do not guess. Do not apply these labels to application PRs unless their own policy separately requires it.
- **Separate promotion gates:** CICD PR may become Ready for Review after feature-branch validation, evidence, label verification and applicable required checks. A human or GitHub's separately authorised auto-merge mechanism merges CICD; the agent MUST NOT directly merge or bypass protections. The application PR remains Draft pending CICD release and subsequent validation.
- **Immutable release:** Release automation MUST create the next semver tag **after merge**, pointing to the actual merged CICD `main` commit, independent of merge strategy. Published version tags must never be moved, overwritten, reused or deleted. Tag immutability and permissions must be technically enforced by GitHub rulesets or equivalent controls. Require exactly one release label and report release failure rather than inventing a version.
- **Application adoption:** After the release is confirmed published, authorised automation or the agent updates each affected application's existing Draft PR from the temporary CICD branch ref to the new immutable tag (for example `@v2.3.0`). Verify that the update triggered fresh PR validation; inspect actual logs and functional results against the released revision. Do not claim that this cross-repository handoff is automatic unless suitable credentials, triggers and automation are actually configured.
- **Independent consumers:** Do not update unrelated application repositories merely because CICD released a version. Each application opts into the release via its own reviewed PR.
- **Final review and evidence:** Promote each application PR only after final release-based validation and applicable checks; request `frankbuttigieg93-png` where permitted. Human reviewers perform final approval and merge. The agent records PR links, release tag and commit, workflow run links, latest application SHA, step logs, expected-vs-observed results, accepted findings and blockers.
- **Known findings:** Document known security findings separately from task-related regressions. Acknowledgement does not waive GitHub required checks; never disable scans or bypass protections.
- **Scope of automation:** This policy authorises the described application caller reference transition within the selected PR Pipeline scope, but does not by itself grant permissions to install GitHub Apps, modify repository rulesets, or add new automation workflows. Seek task-specific authorisation for those changes.
