# CICD — Reusable GitHub Actions Platform

This repository hosts reusable GitHub Actions workflows and composite actions consumed by application repositories, including the [Java Application](https://github.com/frankbuttigieg1993-gmail/java_application). Changes to shared workflows can affect multiple callers; follow repository governance and the established release lifecycle.

## Repository layout

| Path | Purpose |
|---|---|
| `.github/workflows/` | Reusable workflows and CICD automation |
| `.github/actions/` | Composite actions and supporting resources |
| `.github/skills/github-actions-development/SKILL.md` | Reusable implementation, validation and release procedures |
| `AGENTS.md` | Repository governance, authorisation, restrictions and human review boundaries. |
| `.github/Standard CICD Engineering, Release & Application Promotion Workflow.md` | Canonical 16-step lifecycle |
| `ai_engineering/` | Framework explanations, experiments, results and evidence |

## Integration and releases

Applications consume published reusable workflows using a versioned reference, for example:

```yaml
uses: frankbuttigieg1993-gmail/cicd/.github/workflows/java-build-pr.yml@v3.1.0
```

Treat the version above as an **observed Exercise 1 release**, not a permanent requirement for future integrations. Follow the current release process, semantic-version classification, immutable-release verification and application-adoption validation. Use feature-branch references only as permitted for temporary integration testing.

## Engineering governance and onboarding

Start with [`AGENTS.md`](AGENTS.md), the [central Skill](.github/skills/github-actions-development/SKILL.md), and the [canonical lifecycle](.github/Standard%20CICD%20Engineering%2C%20Release%20%26%20Application%20Promotion%20Workflow.md). These files govern different concerns: **what** is permitted, **how** to execute and **when** to hand off. Repository settings, required checks, reviewers and release protections remain authoritative enforcement mechanisms.

For the architecture and completed HITL/No-HITL experiment evidence, see [`ai_engineering/README.md`](ai_engineering/README.md).

## Validation and security

Relevant repository workflows and actions include build/test, dependency review, CodeQL, Semgrep, secrets scanning and other security checks. Validate changes using actual workflow/job/step logs, not green status indicators alone. Preserve unrelated known findings and follow the required approval and remediation processes.

### GitHub Code Quality configuration

The original setup notes for the Java Application repository are retained here for reference:

- [Code Quality settings](https://github.com/frankbuttigieg1993-gmail/java_application/settings/code-quality)
- [Security and Quality results](https://github.com/frankbuttigieg1993-gmail/java_application/security/quality)
- [Security-related GitHub Actions](https://github.com/frankbuttigieg1993-gmail/java_application/actions/new?category=security&query=code+scanning)

Tools previously considered: GitHub CodeQL, Snyk, SonarQube, Semgrep and Codacy. This list is informational; it is not an assertion that each tool is installed or enabled.

## Engineering experiments

Exercise 1 HITL reached Java PR Ready for Review after seven additional checkpoints. Exercise 1 No-HITL completed both repository merges and final verification with no additional exercise-specific checkpoints. See the [experiment comparison](ai_engineering/Exercise_1_Comparison.md) for evidence, limitations and the differences in starting baselines.
