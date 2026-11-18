# Exercise 1 Evidence Index

This register links source artifacts and external evidence. **Historical Markdown reports are not authoritative replacements for raw PR/run metadata.** The screenshot assets were deliberately excluded from the supplied compact repository ZIP; their availability in a cloned repository must be checked separately.

## HITL

| Evidence | Location |
|---|---|
| CICD PR #7 | https://github.com/frankbuttigieg1993-gmail/cicd/pull/7 |
| Java PR #52 | https://github.com/frankbuttigieg1993-gmail/java_application/pull/52 |
| CICD release `v2.2.0` | https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v2.2.0 |
| CICD release workflow | https://github.com/frankbuttigieg1993-gmail/cicd/actions/runs/44014320065 |
| Java released-version validation | https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44016664579 |
| CICD merge SHA | `1c0e8e3021c35de606b0df685d5fdd6374c66b78` |
| Original Copilot transcript | `Exercise 1 - HITL/Exercise 1 - HITL.md` and `.json` |
| Historical report | `Exercise 1 - HITL/Exercise_1_HITL_Full_Historical_Report.md` |
| Results | `Exercise 1 - HITL/RESULTS.md` |

**HITL final recorded Java state:** Ready for Review; merge not confirmed in the historical record.

## No-HITL

| Evidence | Location |
|---|---|
| CICD PR #8 | https://github.com/frankbuttigieg1993-gmail/cicd/pull/8 |
| Java PR #58 | https://github.com/frankbuttigieg1993-gmail/java_application/pull/58 |
| CICD release `v3.1.0` | https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v3.1.0 |
| CICD merge/release SHA | `e7ecad9de8694095e2ea99d1f3ce77d23fc4b5b7` |
| Java merge SHA | `864bf2e8152be77ec596dcce1a9dafc77a1ad86d` |
| Feature-branch validation | https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44210309429 |
| Released-version validation | https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44217333120 |
| Post-merge CICD validation | https://github.com/frankbuttigieg1993-gmail/cicd/actions/runs/44216639087 |
| Context verification prompt | `Exercise 1 - No HITL/Exercise_1_Read_Only_Context_Verification_Prompt.md` |
| Execution prompt | `Exercise 1 - No HITL/Exercise_1_No_HITL_Execution_Prompt.md` |
| Steps 1–7 assessment | `Exercise 1 - No HITL/Exercise_1_No_HITL_Steps_1_to_7_Full_Verbatim_Review.md` |
| Step 8 onward assessment | `Exercise 1 - No HITL/Exercise_1_No_HITL_Step_8_Onwards_Verbatim.md` |
| Final completion assessment | `Exercise 1 - No HITL/Exercise_1_No_HITL_Final_Completion_Review_Verbatim.md` |

## Known findings

- Java Unit Tests: GitHub check success despite underlying Gradle report of **3 failures among 5 tests**.
- Java CodeQL: **2 reported findings** and failed policy enforcement during exercise validation.
- These are documented observations, not a declaration that findings were remediated, waived or accepted under formal governance.

## Screenshot portability

The historical Markdown reports contain relative image references such as `screenshots/OneNote_Page_01.png` and No-HITL screenshot filenames. Those assets were excluded from the compact ZIP provided for this update. **Do not assume the links work in a fresh clone.**

To make the archive portable, either:

1. Extract the original historical-report ZIPs with their `screenshots/` directories beside the corresponding Markdown reports; or
2. Store evidence in a separately maintained archive and update the Markdown image paths and this index to point to its stable location.

Keep original image files unmodified. Do not commit sensitive screenshots without checking repository visibility and information-handling rules.
