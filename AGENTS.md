# Engineering Agent Instructions — CI/CD and Java Application

## Human quick reference — standard engineering process

**Purpose:** A consistent, auditable process for developing and validating shared GitHub Actions components across `cicd` and `java_application`. This summary is explanatory; the policies below are authoritative.

| Step | What happens | Evidence / outcome |
|---|---|---|
| 1. Select pipeline | User specifies **PR Pipeline** or **Build Pipeline** when integrating with an existing pipeline. PR selection authorises scoped changes to the `cicd` PR workflow and the Java PR caller reference when needed; Build selection authorises the `cicd` build workflow. | Named target; otherwise **BLOCKED - AWAITING USER INPUT** before any tools |
| 2. Discover and plan | Agent interprets requirements, inspects existing actions and workflows, identifies conventions and affected files. | Acceptance criteria, convention findings, change plan |
| 3. Branch | Create task-specific branches from current `main` in both repositories where meaningful changes are required. | Branch names; clean baseline |
| 4. Implement | Make the smallest authorised changes; favour existing inline command patterns. | Scoped diff; no unrelated modifications |
| 5. Local validation | Validate YAML, action references, Gradle/tests and integration. | Local test results |
| 6. Draft PRs | Push branches; create cross-linked **Draft** PRs targeting `main`. | PR links, change summary and validation plan |
| 7. CI validation | Run required PR checks and inspect workflow, job **and step logs**. | Run IDs, statuses, log excerpts, head SHAs |
| 8. Functional verification / remediation | Compare actual output with acceptance criteria; investigate, fix and retest if needed. | Expected vs observed evidence; no unverified success |
| 9. Promote | Only after both applicable PRs pass required checks and functional verification on latest relevant commits, mark **Ready for Review**. | Confirmed PR states |
| 10. Review / handoff | Request review from `frankbuttigieg-93`; report links, evidence and limitations. **Never merge.** | Reviewer request and final report |

**For humans — five questions:** What is the process? (above); what conventions apply? (Engineering standards); what may change? (Authorisation); when is work complete? (Verification and promotion); what if it fails? (Failure handling). A review request is not an approval. The agent does not merge PRs.

## 1. Repository responsibilities

- `frankbuttigieg1993-gmail/cicd` owns reusable workflows and composite actions.
- `frankbuttigieg1993-gmail/java_application` owns application code, Gradle configuration, tests and caller workflows.
- Read applicable instructions in **each** repository; instructions are not automatically inherited across repositories. The `github-actions-development` Skill is the authoritative execution runbook; this file is the authoritative policy.

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
- Preserve all unrelated caller workflow jobs, triggers, permissions, checks and behaviour. Record the temporary feature-branch reference, dependency, intended stable reference and required merge order in both PRs. Do not restore `@main` before the `cicd` change is available there if that would invalidate verification; do not merge automatically.
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
- Keep both applicable PRs Draft while implementation, required checks or functional verification are incomplete, failing, skipped unexpectedly, pending, cancelled or unavailable.
- Promote both to **Ready for Review** only when the latest relevant commits pass mandatory checks **and** actual functional behaviour is verified. Do not promote just because a workflow is green.
- Then request review from `frankbuttigieg-93`. If GitHub refuses (e.g. author cannot review own PR), report the limitation; do not impersonate, self-approve, substitute a reviewer without direction or merge.

### GitHub Actions Reference Management and Production Readiness

The agent MUST ensure that all new or modified GitHub Actions workflows have a safe, maintainable reference strategy before being considered ready for production.

Temporary feature-branch references MAY be used for cross-repository integration testing and PR validation.

However, the agent MUST NOT leave a workflow intended for merging into `main` dependent on a temporary feature branch that may subsequently be deleted.

Before promoting a Draft PR to Ready for Review, the agent MUST:

1. Identify all new or modified references to reusable workflows and composite actions.
2. Distinguish temporary validation references from intended production references.
3. Establish a safe final reference strategy using an appropriate stable reference, immutable commit SHA or local action reference.
4. Ensure that the proposed merged workflow will not depend on temporary feature branches.
5. Document any cross-repository merge dependencies and required reference transitions.
6. Verify that the final reference strategy is technically valid and compatible with the repository's engineering conventions.
7. Revalidate any implementation changes made to establish the final reference strategy.

### PR Promotion Requirements

A Draft PR MUST NOT be promoted to Ready for Review unless:

- Required CI/CD checks have passed.
- The requested functionality has been verified using actual execution evidence.
- The final reference strategy has been established and documented.
- No temporary feature-branch dependency will remain in the intended merged workflow.
- Any required post-merge reference transitions are clearly documented and assigned to the appropriate human release or merge process.

The agent MUST NOT merge pull requests or modify protected branches to resolve reference dependencies.

### Ready for Review vs Ready to Merge

Ready for Review and Ready to Merge are distinct states.

A PR may be marked Ready for Review when:

- Required CI/CD checks have passed.
- Functional verification has succeeded.
- The final reference strategy is established and documented.
- Temporary validation references and required transitions are
  explicitly identified.
- No unresolved implementation or validation failures remain.

A PR MUST NOT be considered Ready to Merge while its proposed
merged contents depend on temporary feature-branch references.

Before merging, all temporary references must be replaced with
approved stable references, and the resulting changes must be
revalidated.

The agent MUST document any required merge order or post-merge
reference transition.

The agent MUST NOT merge pull requests.

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
