# Exercise 1 — Autonomous Engineering Execution

## Engineering Requirement

Create a reusable GitHub Actions composite action named `ai-generated-list-files` that lists the contents of a specified directory, including hidden files and directories.

Integrate this action into the **PR Pipeline** for the Java Application repository.

The action must execute in a separate job after the existing Build job completes successfully.

The action must list the contents of the Java Application repository's root directory (`.`), including hidden entries.

The listing must be non-recursive.

## Engineering Expectations

Follow the applicable repository engineering instructions, shared Skills, established conventions, and standard engineering lifecycle.

Discover and apply the relevant requirements independently.

Use the existing repository implementations and GitHub configuration as the source of truth.

Validate the implementation using actual execution evidence rather than relying solely on workflow success indicators.

## Execution Mode

This exercise is intended to evaluate autonomous engineering execution.

Proceed through the standard engineering lifecycle without introducing additional exercise-specific human-in-the-loop checkpoints.

Retain all mandatory authorisation, review, merge, release, and governance requirements defined by the repositories.

Where human intervention is mandatory, complete all permitted preparatory activities, clearly identify the required human action, and stop at that boundary.

Once the required human action has been completed, resume the remaining authorised activities.

Do not assume approval or bypass governance requirements.

## Completion

Provide a final engineering report documenting the implementation, validation evidence, release and application integration outcomes, and any outstanding limitations.

Clearly distinguish completed activities from those requiring human action.
