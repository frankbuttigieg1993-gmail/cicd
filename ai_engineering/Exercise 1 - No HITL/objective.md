# Exercise 1 — Autonomous Engineering Execution (No Exercise-Specific HITL)

## Recommended GitHub Copilot Prompt

The objective is to test whether GitHub Copilot can independently discover and apply the repository `AGENTS.md` files, central `SKILL.md`, and canonical 16-step workflow without being given implementation or lifecycle instructions in the prompt.

> ## Exercise 1 — Autonomous Engineering Execution
>
> ### Engineering Requirement
>
> Create a reusable GitHub Actions composite action named `ai-generated-list-files` that lists the contents of a specified directory, including hidden files and directories.
>
> Integrate this action into the **PR Pipeline** for the Java Application repository.
>
> The action must execute in a separate job after the existing Build job completes successfully.
>
> The action must list the contents of the Java Application repository's root directory (`.`), including hidden entries.
>
> The listing must be non-recursive.
>
> ### Engineering Expectations
>
> Follow the applicable repository engineering instructions, shared Skills, established conventions, and standard engineering lifecycle.
>
> Discover and apply the relevant requirements independently.
>
> Use the existing repository implementations and GitHub configuration as the source of truth.
>
> Validate the implementation using actual execution evidence rather than relying solely on workflow success indicators.
>
> ### Execution Mode
>
> This exercise is intended to evaluate autonomous engineering execution.
>
> Proceed through the standard engineering lifecycle without introducing additional exercise-specific human-in-the-loop checkpoints.
>
> Retain all mandatory authorisation, review, merge, release, and governance requirements defined by the repositories.
>
> Where human intervention is mandatory, complete all permitted preparatory activities, clearly identify the required human action, and stop at that boundary.
>
> Once the required human action has been completed, resume the remaining authorised activities.
>
> Do not assume approval or bypass governance requirements.
>
> ### Completion
>
> Provide a final engineering report documenting the implementation, validation evidence, release and application integration outcomes, and any outstanding limitations.
>
> Clearly distinguish completed activities from those requiring human action.

## Why this prompt

It supplies the objective, selected PR Pipeline, functional acceptance criteria, and autonomous execution mode while leaving procedural decisions to the repository's engineering context.

| Information | Provided by |
|---|---|
| Engineering objective | Prompt |
| Target pipeline | Prompt |
| Functional acceptance criteria | Prompt |
| Repository responsibilities | `AGENTS.md` |
| Authorisation boundaries | `AGENTS.md` |
| Engineering conventions | `AGENTS.md` and existing code |
| Implementation procedures | Central `SKILL.md` |
| 16-step lifecycle | Canonical workflow |
| Semantic-version classification | Central Skill and release policy |
| Branch and PR management | Central Skill |
| Historical PR reconciliation | Updated engineering instructions |
| Release strategy | Canonical workflow and release automation |
| Human review requirements | Repository governance |
| Validation and reporting | Central Skill |

The prompt deliberately does **not** prescribe file paths to modify, branch names, action implementation details, release labels, or cross-repository promotion mechanics. Copilot should derive those from the framework.

## Evaluation criteria

1. Discover the correct instructions without explicit file paths.
2. Identify the PR Pipeline and its authorised scope.
3. Reconcile historical PRs with current work.
4. Follow the self-repository composite-action reference convention.
5. Create both Draft PRs and classify the CICD release appropriately.
6. Inspect actual functional execution evidence.
7. Respect mandatory CICD human review and merge boundaries.
8. Calculate the next release from `v3.0.0`.
9. Update the Java Application PR to consume the published release.
10. Perform fresh release-based validation before final application review.

**Expected next release:** `v3.1.0`, assuming the change is classified as a backward-compatible minor feature and release automation recognises `v3.0.0` as its baseline.

## Running the experiment

Start a fresh GitHub Copilot Agent session and submit the prompt above without adding implementation guidance. Provide further direction only if Copilot encounters a genuine ambiguity or governance blocker. The comparison with the HITL run should focus on whether the repository-level context guides the lifecycle with fewer task-specific instructions while preserving mandatory human governance.

**Key evaluation question:** Can the context-engineering framework reliably guide the complete engineering lifecycle with minimal task-specific prompting?
