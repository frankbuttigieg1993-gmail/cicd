---
name: github-actions-development
description: Develop and validate reusable GitHub Actions workflows and composite actions, including coordinated integration with a consuming Java/Gradle repository. Use for creating new actions, troubleshooting CI/CD runs, validating cross-repository workflow references, and preparing pull requests while preserving existing shared pipelines.
---

# GitHub Actions development runbook

Follow the applicable repository `AGENTS.md` instructions and the user's explicit file allowlist. This Skill is procedural guidance, not a permission grant.

## 1. Establish scope
1. Read task acceptance criteria and repository instructions in both repositories.
2. List **allowed files**, **protected files**, target branches, and expected validation runs before making changes.
3. If an implementation requires editing a protected file, stop and request approval; do not reinterpret the task.

## 2. Inspect references
1. Read existing reusable workflows and composite actions to learn conventions.
2. Inspect the Java application's Gradle wrapper and existing workflow references without changing them.
3. Check GitHub reusable-workflow syntax and how a composite action in `cicd` is resolved when the caller repository is checked out.

## 3. Implement in `cicd`
1. Create a feature branch from `main`.
2. Create only the authorised new `.github/workflows/ai-generated.yml` and `.github/actions/ai-generated/action.yml`.
3. Use `workflow_call`, least-privilege permissions, explicit shells, and minimal inputs.
4. Keep existing shared workflows unchanged.
5. Validate syntax and push the feature branch.

## 4. Integrate in `java_application`
1. Create a separate feature branch from `main`.
2. Create only the authorised `.github/workflows/ai-generated.yml` caller.
3. Reference the `cicd` feature ref for the lab; record the eventual immutable-ref migration.
4. Validate the caller's inputs, triggers, and permissions; push the branch.

## 5. Run and diagnose
1. Attempt the requested manual dispatch where GitHub supports it for the workflow/ref.
2. If feature-branch dispatch is unavailable, report the platform constraint; use only an authorised alternative trigger.
3. Inspect the actual workflow run, including evidence that the new composite action executed.
4. Diagnose failures and iterate **only inside allowed files**; do not bypass required checks or edit unrelated pipelines.
5. Distinguish mandatory relevant failures from unrelated optional failures; report both.

## 6. Prepare PRs and report
1. Open separate PRs against `main` for each repository; cross-link them.
2. Include changed-file lists, run URLs/IDs, job conclusions, outstanding failures, and the temporary cross-repo ref dependency.
3. Never merge. Report COMPLETE only when the requested end-to-end run succeeded and both PRs exist; otherwise state the precise limitation.
