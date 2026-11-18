# Exercise 1 --- HITL vs No-HITL Comparison

## Research question

Can the same engineering objective be delivered with fewer human
interventions when GitHub Copilot relies on repository-level context
instead of seven exercise-specific HITL checkpoints, **without weakening
mandatory PR governance or functional verification**?

## Experimental design

  -----------------------------------------------------------------------
  Variable                HITL                    No-HITL
  ----------------------- ----------------------- -----------------------
  Engineering task        Non-recursive           Same task
                          root-directory listing, 
                          including hidden        
                          entries, in separate PR 
                          job after successful    
                          Build                   

  Pipeline                PR Pipeline             PR Pipeline

  Extra exercise approval Seven                   None
  gates                                           

  Mandatory human PR      Retained                Retained
  reviews/merges                                  

  Instruction baseline    Earlier versions;       Updated committed
                          refined during/after    instructions, including
                          run                     historical PR
                                                  reconciliation

  CICD release outcome    `v2.2.0`                Pending; `v3.1.0`
                                                  anticipated for minor

  Application adoption    Java PR #52 adopted     Pending
                          `@v2.2.0`               
  -----------------------------------------------------------------------

**Confounder:** The instructions and governance controls were improved
after the HITL run. Any difference cannot be attributed solely to
removing HITL checkpoints.

## Baselines and observed results

  ---------------------------------------------------------------------------------------------------------------------------------------------------
  Dimension               HITL evidence                                                                  No-HITL evidence
  ----------------------- ------------------------------------------------------------------------------ --------------------------------------------
  CICD starting SHA       Not established in this summary; retrieve from exported session                `2144004d0e206fd3b8325809aa987c7e9569a03b`

  Java starting SHA       Not established in this summary                                                `80dd761` (abbreviated; verify full SHA)

  Published CICD baseline Verify from original session                                                   `v3.0.0`, published and shown immutable

  Current Java CICD ref   Verify original baseline                                                       `@v2.2.0`

  Historical PRs          Previous PRs caused identity confusion                                         Preserved to test updated reconciliation

  CICD PR                 [#7](https://github.com/frankbuttigieg1993-gmail/cicd/pull/7), merged          Pending

  Java PR                 [#52](https://github.com/frankbuttigieg1993-gmail/java_application/pull/52),   Pending
                          Ready for Review at final checkpoint                                           

  Release                 `v2.2.0`                                                                       Pending

  Release validation      CICD merge SHA and tag protection verified after remediation                   Pending

  Functional validation   Actual logs inspected; expected root entries observed                          Pending

  Final application merge Not confirmed                                                                  Pending

  Extra HITL checkpoints  Seven completed                                                                Zero planned
  ---------------------------------------------------------------------------------------------------------------------------------------------------

## Evaluation scorecard

  -----------------------------------------------------------------------
  Capability              HITL                    No-HITL
  ----------------------- ----------------------- -----------------------
  Instruction discovery   Demonstrated            Pending

  Convention discovery    Demonstrated            Pending
  and scoped                                      
  implementation                                  

  Cross-repository Draft  Demonstrated            Pending
  PRs                                             

  Historical PR           Confusion encountered;  Pending behavioural
  reconciliation          instructions improved   test
                          afterward               

  Correct release label   `release:minor`         Pending

  Feature-branch          Demonstrated            Pending
  functional validation                           

  CICD promotion and      Demonstrated            Pending
  authorised merge                                

  Immutable release       Demonstrated after      Pending
  verification            remediation             

  Application adoption    Demonstrated            Pending
  and revalidation                                

  Final application Ready Demonstrated            Pending
  for Review                                      

  Human review boundaries Observed                Pending

  Full autonomous         Not tested              Not assumed; governance
  end-to-end completion                           boundaries remain
  -----------------------------------------------------------------------

## Quantitative measures to record

  -------------------------------------------------------------------------
  Measure             HITL              No-HITL           Collection method
  ------------------- ----------------- ----------------- -----------------
  Exercise-specific   7                 Target 0          Prompt and chat
  approval                                                transcript
  checkpoints                                             

  Mandatory human     Determine from    Pending           PR review and
  approvals/merges    history                             merge events

  Clarification       Count from export Pending           Chat export
  requests                                                

  Avoidable stops     Count from export Pending           Annotated chat
                                                          export

  Manual remediations Count from export Pending           PR history and
                                                          notes

  Implementation      Count from export Pending           Commits and
  correction cycles                                       workflow runs

  Validation attempts Count from GitHub Pending           Run IDs

  Governance          Assess against    Pending           Audit of
  violations          policy                              PRs/settings

  Functional          Passed for file   Pending           Actual step logs
  acceptance          listing                             

  Elapsed time        Reconstruct       Pending           Chat/PR/run
                      timestamps                          timestamps

  Evidence            Assess            Pending           PRs and final
  completeness                                            report
  -------------------------------------------------------------------------

Do not invent counts or times that have not been measured.

## Interpretation rules

A successful workflow status alone is insufficient: compare actual logs
and expected results. Known test and CodeQL findings should be recorded
separately from regressions, without bypassing mandatory checks. A
request for review is not an approval; Ready for Review is not merged.
Distinguish actual improvements from differences in starting baselines,
instructions, GitHub settings and available context.

## Evidence

-   HITL: `Exercise 1 - HITL/Exercise 1 - HITL.md` and `.json`
-   HITL CICD PR:
    https://github.com/frankbuttigieg1993-gmail/cicd/pull/7
-   HITL Java PR:
    https://github.com/frankbuttigieg1993-gmail/java_application/pull/52
-   HITL release:
    https://github.com/frankbuttigieg1993-gmail/cicd/releases/tag/v2.2.0
-   HITL application run:
    https://github.com/frankbuttigieg1993-gmail/java_application/actions/runs/44016664579
-   No-HITL evidence: add after execution

## Conclusion

**Pending.** Do not conclude that the No-HITL approach is superior until
execution evidence and intervention counts have been collected.
