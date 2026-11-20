# Exercise 3 — Agent EKS Networking Troubleshooting

> **Status:** Complete for the six recorded troubleshooting investigations.  
> **Source:** *Exercise 3 - Agentic EKS Networking Troubleshooting.pdf* (27 pages; notes dated 13 November 2026).  
> **Evidence note:** This is a retrospective summary of the supplied notes, not an independent rerun or verification of AWS resources. Example API calls and interaction steps describe the architecture rather than a verbatim tool trace.

## 1. Executive summary

Exercise 3 evaluated whether GitHub Copilot, using **both Kubernetes and AWS MCP integrations**, could investigate networking failures affecting workloads in Amazon EKS, distinguish Kubernetes-level restrictions from AWS networking restrictions, and identify the actual root cause. It also compared the agent's investigation **without** repository instructions against an investigation **with `AGENTS.md` and a troubleshooting Skill**.

The recorded work covered three failure types: **Kubernetes NetworkPolicy**, **AWS security group**, and **AWS network ACL (NACL)**. Each was tested in two configurations, yielding **six investigations**. The notes report **six correct root-cause identifications out of six**. The configured-agent runs generally produced more comprehensive explanations, explicit evidence and verification or remediation guidance, but did **not** consistently finish faster. These observations are encouraging, not proof of statistical reliability or that instructions alone caused the differences.

The solution also demonstrated a hybrid architecture: a remote LLM accessed through GitHub Copilot; local VS Code/Copilot tooling; a **Kubernetes MCP Server deployed inside EKS** and reached via local port-forwarding; and a **separate AWS MCP Server running locally**. Read-only Kubernetes RBAC, MCP read-only configuration and AWS permissions formed important operational boundaries. The final notes mark Exercise 3 complete, while identifying **OPA/Gatekeeper admission-policy testing as an optional, uncompleted extension**.

## 2. Objective and evaluation questions

**Primary objective:** Determine whether an MCP-enabled AI agent can diagnose networking failures between EKS workloads and AWS-hosted endpoints using live Kubernetes and AWS configuration evidence, rather than relying solely on generic networking knowledge.

**Secondary objective:** Compare diagnostic correctness, investigation quality, operational reporting and execution time **with versus without** `AGENTS.md` and a reusable troubleshooting Skill.

The exercise asked whether Copilot could:

- Establish the intended connectivity baseline before introducing a controlled failure.
- Inspect Kubernetes resources and AWS networking configuration through distinct MCP integrations.
- Identify the actual enforcement layer (Kubernetes NetworkPolicy, security group or NACL).
- Distinguish a suspicious configuration from a rule that actually blocks traffic, including precedence and return-path considerations.
- Provide evidence-based conclusions and actionable remediation/verification guidance while respecting access controls.

## 3. Architecture and execution locations

| Component | Provider / technology | Execution location | Role |
|---|---|---|---|
| Human operator | Exercise participant | Local workstation | Defines scenarios, establishes failures, reviews evidence and controls changes/remediation. |
| VS Code | Microsoft | Local Windows PC | Hosts the interaction and MCP client configuration. |
| GitHub Copilot Chat | GitHub | Local VS Code integration | Receives prompts and displays agent findings. |
| GitHub Copilot agent | GitHub | Orchestrated through VS Code, with remote services | Performs iterative investigation and coordinates model/tool interactions. |
| LLM | Model accessed through Copilot | Remote model infrastructure | Interprets requests, selects relevant diagnostic tools and reasons over results. Exact model is not established by these notes. |
| Copilot agent harness | Copilot / VS Code | Local integration and supporting remote services | Manages the agent loop, tool invocation and result delivery. Not necessarily a separate standalone process. |
| MCP client | VS Code / Copilot | Local Windows PC | Connects to both MCP endpoints and invokes advertised tools. |
| Kubernetes MCP Server | Helm-deployed Kubernetes MCP implementation | **Inside Amazon EKS** (`ai-troubleshooting` namespace) | Provides Kubernetes API inspection and policy/workload diagnostics. |
| Kubernetes MCP connection | HTTP via `kubectl port-forward` | Local tunnel to EKS service | Exposes the in-cluster MCP endpoint to the local client (recorded as `8080:8080`). |
| AWS MCP Server | AWS tooling / MCP integration | **Local Windows PC** | Exposes AWS networking diagnostic operations through AWS APIs. |
| Kubernetes API | Kubernetes / EKS | AWS-hosted EKS control plane | Supplies workload, namespace, service, NetworkPolicy and RBAC information. |
| Kubernetes RBAC | Kubernetes | EKS cluster | Restricts what the in-cluster MCP service account can access. |
| AWS SDK / API access | AWS | Local AWS MCP process to AWS cloud APIs | Retrieves EC2/VPC networking configuration and related evidence. |
| AWS IAM | AWS | AWS Cloud | Authorises or denies AWS API operations made with the configured credentials. |
| EKS VPC CNI network policy agent | AWS EKS add-on | EKS nodes | Enforces Kubernetes NetworkPolicy when enabled/configured. |
| Security groups and NACLs | AWS VPC | AWS Cloud | Apply AWS-side network traffic restrictions to the relevant interfaces/subnets. |
| EC2 test endpoint | AWS EC2 | AWS Cloud | Destination used for cross-subnet pod-to-EC2 TCP connectivity tests. |

**Important distinction from Exercise 2:** The Kubernetes MCP Server was deployed **in EKS**, not simply run locally. Its endpoint was accessed through a local port-forward. The AWS MCP Server was the locally running integration.

### Conceptual interaction

```text
Human operator
    |
    v
VS Code / GitHub Copilot Chat (Windows PC)
    |
    v
Copilot agent + harness <----> Remote LLM
    |
    v
Local MCP client
    |                         |
    | HTTP via port-forward   | Local AWS MCP integration
    v                         v
Kubernetes MCP Server        AWS MCP Server
(in EKS namespace)           (Windows PC)
    |                         |
Kubernetes API / RBAC        AWS APIs / IAM
    |                         |
EKS pods, policies,          VPC, security groups,
services, nodes              NACLs, subnets, EC2
    \_________________________/
                  |
         Evidence returned to
         Copilot for analysis
```

## 4. Environment and preparation

The notes record the following preparation work:

1. Create the `EKS-DEV` cluster and configure access.
2. Obtain the Kubernetes MCP Server Helm chart and adapt its values for the exercise.
3. Create the `ai-troubleshooting` namespace and a read-only Kubernetes RBAC service account.
4. Configure the MCP server for read-only use, render the Helm manifest, and deploy it to EKS.
5. Inspect pods, services and server logs; connect Copilot using a local `kubectl port-forward` to the MCP service.
6. Test MCP connectivity and guardrails.
7. Enable EKS VPC CNI NetworkPolicy enforcement and policy event logging for the Kubernetes policy scenarios.
8. Establish known-good network connectivity before introducing each controlled failure.

The source includes operational commands and setup screenshots. This report intentionally does **not** reproduce privileged identity-mapping or broad cluster-admin commands as reusable setup recommendations. Their presence in historical setup notes does not establish that those privileges were required for the agent's read-only troubleshooting role.

## 5. Scenarios and results

| Test | Failure introduced | Agent context | Reported diagnosis | Recorded time |
|---|---|---|---|---:|
| **3A** | Kubernetes NetworkPolicy blocks intended traffic | Without `AGENTS.md` / Skill | Correct | **67 s** |
| **3B** | Same Kubernetes NetworkPolicy scenario | With `AGENTS.md` / Skill | Correct | **56 s** |
| **3C-A** | AWS security group prevents required TCP traffic | Without `AGENTS.md` / Skill | Correct | **80 s** |
| **3C-B** | Same security-group scenario | With `AGENTS.md` / Skill | Correct | **131 s** |
| **3D-A** | AWS NACL denies pod-to-EC2 traffic | Without `AGENTS.md` / Skill | Correct | Not reliably captured in readable notes |
| **3D-B** | Same NACL scenario | With `AGENTS.md` / Skill | Correct | Notes report approximately **20 seconds more** than 3D-A; exact totals not established |

### Scenario 3A / 3B — Kubernetes NetworkPolicy

A working baseline was established in the `network-lab` namespace using test workloads. A NetworkPolicy was then introduced to block the expected traffic. Copilot investigated the Kubernetes-side configuration through the Kubernetes MCP integration. Both versions correctly identified the NetworkPolicy as the cause. The instructed run was recorded as **56 seconds**, compared with **67 seconds** without instructions.

**Outcome:** Correct root-cause identification in both runs. The configured run was faster in this particular test; one pair of runs does not establish a general speed advantage.

### Scenario 3C-A / 3C-B — AWS security group

The experiment established pod-to-EC2 TCP connectivity, then removed the destination security group's relevant inbound allowance. The agent needed to correlate Kubernetes workload/network information with AWS-side rules and determine which restriction was actually effective.

Both runs correctly identified the security-group issue. The configured run was more thorough: it documented relevant resources and why they were or were not responsible, and provided more specific remediation guidance. The notes also highlight that Copilot examined a potentially restrictive NACL rule but considered **rule precedence** before treating it as the actual blocker.

**Outcome:** Both correct. The instructed run took **131 seconds**, versus **80 seconds** without instructions. The improvement was principally **reporting completeness and operational evidence**, not speed or diagnostic correctness.

### Scenario 3D-A / 3D-B — AWS network ACL

A dedicated subnet, NACL and EC2 destination were prepared. The source EKS pod was tested against the EC2 endpoint on TCP 443, with working connectivity established first. A NACL deny was then introduced for the relevant source traffic and the blocked connectivity was verified.

Both agent configurations identified the NACL restriction. The instructed run included a fuller cross-layer investigation, reviewing source/destination network controls and **return traffic**, which matters because AWS NACLs are stateless. The notes state that the instructed run required three additional agent steps and approximately 20 additional seconds.

**Outcome:** Both correct. The instructed run improved the completeness and verification detail of the explanation, rather than changing the root-cause result. The exact elapsed times are not transcribed here because they are not reliably legible in the supplied notes.

## 6. Example end-to-end agent investigation: EKS pod cannot reach EC2

This is an **illustrative architecture flow**, consistent with the recorded security-group and NACL tests; it is not a verbatim transcript of a specific run.

| Step | Component | Action |
|---|---|---|
| 1 | Human / Copilot Chat | User asks why a pod cannot connect to an EC2 endpoint on TCP 443. |
| 2 | Remote LLM / Copilot agent | Forms hypotheses involving NetworkPolicy, security groups, NACLs and routes. |
| 3 | Harness / MCP client | Invokes Kubernetes MCP tools to inspect the pod, namespace, relevant NetworkPolicies and service/workload configuration. |
| 4 | In-cluster Kubernetes MCP Server | Reads permitted Kubernetes API resources under its service account's RBAC. |
| 5 | Copilot agent | Correlates pod IP, node/network context and destination information. |
| 6 | Harness / AWS MCP Server | Requests permitted AWS networking details such as security groups, NACLs, subnets and route tables. |
| 7 | AWS IAM / AWS APIs | Authorises and returns configuration information. |
| 8 | Remote LLM | Evaluates which control actually blocks the traffic, including ordered NACL rules and the return path. |
| 9 | Copilot Chat | Reports root cause, evidence, uncertainties and a proposed remediation/verification plan. |
| 10 | Human operator | Reviews any change; re-tests connectivity after authorised remediation. |

The agent's access to a diagnostic tool is **not** equivalent to permission to change the cluster or AWS configuration.

## 7. Guardrails and authority boundaries

| Layer | Control | Purpose |
|---|---|---|
| **1 — Agent instructions** | `AGENTS.md` | Defines investigation scope, expected evidence, restrictions and approval boundaries. |
| **2 — Reusable procedure** | Troubleshooting Skill | Guides systematic cross-layer diagnosis, evidence capture and verification. |
| **3 — Kubernetes technical controls** | Read-only MCP configuration and Kubernetes RBAC | Limits what the Kubernetes MCP service account can do in the cluster. |
| **4 — AWS technical controls** | AWS credentials and IAM policies | Limits AWS API operations available to the AWS MCP integration. |

Kubernetes NetworkPolicy, AWS security groups and NACLs were also **subjects of the diagnostic exercise**: they are traffic-enforcement controls, distinct from permissions granted to the troubleshooting agent.

## 8. Findings and interpretation

**Diagnostic accuracy:** The notes report **6/6 correct root-cause identifications** across the three paired scenarios.

**Cross-platform reasoning:** Copilot used Kubernetes and AWS tool results to distinguish the actual blocking layer. The security-group investigation demonstrated rule-precedence reasoning; the NACL investigation demonstrated return-path awareness.

**Effect of `AGENTS.md` and Skill:** The instructed runs generally yielded more structured, complete and auditable investigations, including specific remediation and verification guidance. They did **not** consistently improve speed: 3B was faster than 3A, whereas 3C-B was slower than 3C-A and 3D-B reportedly required additional time.

**Scope of the claim:** These were a small number of intentionally constructed scenarios, with different instruction conditions. The results support the usefulness of MCP-enabled cross-layer troubleshooting and structured agent context, but do not prove statistical reliability, general performance superiority or causation.

**Security:** The recorded investigations emphasised read-only access and explicit governance. Historical cluster setup and deliberate failure injection were operator-controlled preparation activities, not evidence that the agent should receive unrestricted modification privileges.

**Remaining extension:** OPA/Gatekeeper admission-policy enforcement was discussed in the notes but **not tested** as part of the six completed investigations.

## 9. Final executive assessment

> **Exercise 3 — COMPLETE for the recorded networking troubleshooting scenarios.** GitHub Copilot, connected to Kubernetes and AWS MCP tools, correctly identified the root cause in all six documented investigations across Kubernetes NetworkPolicy, AWS security-group and AWS NACL failures. Adding `AGENTS.md` and a troubleshooting Skill generally improved the structure, evidence and operational usefulness of the responses, without consistently improving diagnostic speed. The experiment demonstrates a practical hybrid, MCP-enabled agentic troubleshooting architecture; its small test set limits broader claims.

## 10. Source and evidence notes

- **Primary source:** *Exercise 3 - Agentic EKS Networking Troubleshooting.pdf*, supplied with this request (27 pages).
- **Architecture and setup:** pp. 1–10 (dual MCP architecture, EKS Helm deployment, read-only controls and port-forwarding).
- **Kubernetes policy tests:** pp. 11–13 (3A and 3B).
- **AWS security-group tests and initial comparison:** pp. 14–19 (3C-A and 3C-B; four-test comparison on p. 19).
- **AWS NACL tests and final assessment:** pp. 19–26 (3D-A and 3D-B; six-test conclusions on p. 25).
- **Evidence limitation:** Some source pages are embedded screenshots rather than selectable text. Where exact timings, tool names or values could not be established confidently, this summary does not invent them.
