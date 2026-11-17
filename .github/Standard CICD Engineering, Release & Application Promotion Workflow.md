# Standard CICD Engineering, Release & Application Promotion Workflow

This 16-step process describes the standard engineering lifecycle for a central CICD repository and its consuming application repositories. It uses one semantic version for the entire CICD repository, immutable release tags created on merged commits, and evidence-based validation.

1. **Requirements Analysis and Pipeline Selection:** GitHub Copilot analyses the user prompt, identifies the target pipeline (PR or Build), confirms the authorised change scope and reads the applicable `AGENTS.md` and `SKILL.md` files.

2. **Repository Convention Discovery and Planning:** Inspect existing composite actions, reusable workflows and application caller workflows. Identify established engineering conventions, define acceptance criteria and prepare the implementation and validation plan.

3. **Create CICD Feature Branch:** Create a feature branch from `main` in the CICD repository. Implement the composite action and reusable workflow changes, following existing conventions and using self-repository action references (`$/.github/actions/...`).

4. **Create Application Feature Branch:** Create a corresponding feature branch from `main` in the affected application repository. Temporarily update its caller workflow to reference the CICD feature branch.

5. **Perform Local Validation:** Validate YAML syntax, composite-action metadata, workflow dependencies, repository references and relevant functionality. Confirm that changes follow existing conventions and do not affect unrelated workflows.

6. **Create Both Draft PRs:** Create cross-referenced Draft PRs targeting `main` in both repositories. Document implementation details, acceptance criteria, temporary references, cross-repository dependencies and the validation plan.

7. **Classify the CICD Release and Apply the PR Label:** Copilot evaluates the change and applies **exactly one** semantic-version label to the CICD Draft PR:
   - `release:patch` — Backward-compatible bug fix.
   - `release:minor` — New backward-compatible functionality.
   - `release:major` — Breaking change.

   Copilot must document the reason for its classification. If the appropriate classification is ambiguous, it must request clarification rather than guessing.

8. **Execute End-to-End Feature-Branch Validation:** Run the application PR Pipeline against the CICD feature branch. Inspect workflow, job and step statuses, retrieve actual execution logs and verify the functionality against acceptance criteria. Investigate failures, remediate authorised issues and record evidence in both PRs.

9. **Promote CICD PR to Ready for Review:** Once the required validation and governance conditions are satisfied, update the CICD PR with supporting evidence, confirm the final reference strategy and transition it from Draft to Ready for Review. Request the required human review.

10. **Review and Merge CICD PR:** Obtain the required human approval and merge the CICD PR through the approved GitHub process. GitHub's native auto-merge may be used where configured and authorised.

11. **Automatically Create the Semantic-Version Release:** After the CICD PR merges, the release pipeline reads the PR's release label, determines the next semantic version, creates an **immutable tag on the actual merged commit** representing the entire CICD repository, and publishes the GitHub Release.

12. **Update the Application Draft PR:** Automatically update the application caller workflow to reference the newly published CICD version (e.g., `@v2.3.0`) instead of the temporary feature branch. Commit and push the change to trigger the application PR Pipeline again.

13. **Execute Final Application Validation:** Validate the application against the released CICD version. Inspect workflow, job and step statuses, retrieve actual execution logs, verify functionality and confirm no temporary feature-branch references remain. Document the final evidence in the application PR.

14. **Promote Application PR to Ready for Review:** Once applicable validation and governance requirements are satisfied, transition the application PR from Draft to Ready for Review and request review from the designated reviewer (`frankbuttigieg-93`).

15. **Final Human Review and Merge:** The human reviewer evaluates the application changes, CICD release version, execution evidence and outstanding findings. Once approved, merge the application PR through the established GitHub process.

16. **Final Reporting and Cleanup:** Record the CICD release version, PR URLs, commit SHAs, validation results, execution logs and final outcomes. Remove temporary feature branches when no longer referenced. Preserve immutable release tags and supporting evidence.

## Important governance requirement

Every CICD PR that triggers semantic-version release automation **MUST have exactly one valid release classification label before being promoted to Ready for Review**.

The `cicd/AGENTS.md` file should establish this policy. The `github-actions-development/SKILL.md` file should describe how the agent analyses the change, selects the label, applies it to the PR and verifies that GitHub recorded it.

For the `ai-generated-list-files` exercise, `release:minor` is the appropriate classification when the change adds backward-compatible functionality.

## Key architectural principle

**Requirements → Convention Discovery → Implement → Draft PRs → Release Classification → Feature-Branch Validation → CICD Review & Merge → Immutable Semantic Release → Application Adoption → Final Validation → Application Review & Merge → Evidence & Cleanup.**
