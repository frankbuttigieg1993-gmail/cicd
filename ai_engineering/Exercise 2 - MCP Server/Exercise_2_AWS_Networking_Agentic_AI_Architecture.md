# Exercise 2 — AWS Networking Troubleshooting

## Agentic AI Architecture: Components, Execution Locations and Responsibilities

### Executive summary

Exercise 2 used a **hybrid, MCP-enabled agentic AI troubleshooting architecture**: GitHub Copilot Agent Mode in VS Code, a remotely hosted large language model (LLM), a locally launched AWS Networking MCP Server, and IAM-governed access to AWS APIs. The LLM reasoned about the troubleshooting request; the Copilot agent and harness coordinated tool use; the MCP server retrieved infrastructure evidence; and AWS IAM enforced permissions.

The component locations below describe the setup documented during the exercise. The precise model label and internal distribution of Copilot orchestration were not independently verified from runtime diagnostics.

## 1. Architecture component inventory

| # | Component | Provider | Execution location | Role |
|---|---|---|---|---|
| 1 | Human operator | User | Local | Defines troubleshooting objectives, reviews findings and authorises remediation. |
| 2 | Visual Studio Code | Microsoft | Local Windows PC | Hosts the editor, Copilot interface and MCP integration. |
| 3 | GitHub Copilot Chat | GitHub | Local VS Code extension | Conversational interface for prompts and results. |
| 4 | GitHub Copilot AI Agent | GitHub | Orchestrated primarily through VS Code, with remote model services | Pursues the investigation using iterative reasoning and tools; not necessarily a standalone process. |
| 5 | Large Language Model (LLM) | Model provider via GitHub Copilot | Remote cloud infrastructure | Interprets requests, selects tools and analyses evidence. Earlier notes refer to a “GPT-6 Luna” label; the precise model was not independently verified. |
| 6 | GitHub Copilot Agent Harness | GitHub / VS Code | Local integration with supporting cloud services | Coordinates model requests, tool availability, invocations and returned results. |
| 7 | MCP Client | VS Code / Copilot | Local Windows PC | Connects to the MCP server, discovers its tools and invokes them. |
| 8 | `uvx` | Astral | Local Windows PC | Resolves and launches the Python-based MCP server package. |
| 9 | AWS Networking MCP Server | AWS Labs | Local Windows PC | Exposes AWS networking investigation tools through MCP. AWS provides the software; it is not hosted in AWS in this configuration. |
| 10 | AWS SDK for Python (Boto3) | AWS | Local MCP server process | Calls AWS APIs using available credentials. |
| 11 | AWS credentials/profile | Configured AWS identity source | Local configuration or credential provider | Supplies the identity used for AWS requests. |
| 12 | AWS IAM | AWS | AWS Cloud | Authorises or denies API operations for that identity. |
| 13 | AWS EC2 APIs | AWS | AWS Cloud | Returns information from operations such as `DescribeSecurityGroups`, `DescribeInstances` and `DescribeRouteTables`. |
| 14 | AWS networking resources | AWS | AWS Cloud | VPCs, subnets, security groups, routes, ACLs, gateways and instances under investigation. |
| 15 | MCP tool responses | AWS MCP server / AWS APIs | Returned through local MCP connection and Copilot context | Structured evidence for the LLM to interpret. |

**Agent versus harness:** The *agent* refers to the AI-driven system pursuing the objective. The *harness* is the software coordinating model requests, tool calls and results. They are related concepts, not necessarily separate installed executables.

## 2. Execution environments

| Environment | Components | Responsibility |
|---|---|---|
| Local Windows PC | VS Code, Copilot Chat integration, local agent tooling, MCP client, `uvx`, AWS Networking MCP Server, Boto3 | Interaction, tool orchestration and AWS API requests. |
| Remote AI infrastructure | LLM inference and supporting Copilot services | Reasoning, tool selection and interpretation of evidence. |
| AWS Cloud | IAM, EC2 APIs and networking resources | Authorisation and authoritative infrastructure data. |

## 3. Example: List AWS security groups

**Example prompt:** “List all security groups in my AWS environment and identify their inbound and outbound rules.”

This is an **illustrative** execution flow, not a transcript of a verified historical tool invocation. Actual MCP tool names depend on the installed server version. AWS API calls are scoped by account, region and credentials; a complete multi-region inventory may require multiple calls.

| Step | Component | Location | Action |
|---|---|---|---|
| 1 | Human operator | Local | Submits the security-group request. |
| 2 | Copilot Chat | Local | Receives the prompt. |
| 3 | Copilot harness | Local integration / cloud support | Supplies context and available MCP tool definitions to the model. |
| 4 | LLM | Remote | Determines security-group data is needed. |
| 5 | LLM | Remote | Selects an appropriate MCP tool. |
| 6 | Copilot harness | Local integration | Routes the tool invocation. |
| 7 | MCP client | Local | Calls the AWS Networking MCP Server. |
| 8 | AWS Networking MCP Server | Local | Maps the request to an AWS operation. |
| 9 | Boto3 | Local | Makes an AWS API request such as `DescribeSecurityGroups`. |
| 10 | AWS IAM | AWS Cloud | Evaluates the caller's permissions. |
| 11 | EC2 API | AWS Cloud | Returns security-group configuration for the requested scope. |
| 12 | MCP server | Local | Formats and returns the tool result. |
| 13 | MCP client / harness | Local integration | Returns evidence to the model context. |
| 14 | LLM | Remote | Interprets inbound/outbound rules and determines whether further checks are needed. |
| 15 | Copilot Chat | Local | Presents findings and limitations to the user. |

### Illustrative AWS SDK operation

```python
import boto3

ec2 = boto3.client("ec2", region_name="ap-southeast-2")
response = ec2.describe_security_groups()
```

This example illustrates the underlying API call, **not** the exact code used by the MCP server during Exercise 2. An IAM denial prevents the request regardless of the model's intent.

### Illustrative returned configuration

| Security group | Inbound rule | Source | Outbound rule |
|---|---|---|---|
| `sg-web` | TCP 443 | `0.0.0.0/0` | All traffic |
| `sg-app` | TCP 8080 | `sg-web` | All traffic |
| `sg-database` | TCP 5432 | `sg-app` | All traffic |

The agent might infer that the web tier accepts HTTPS, the application tier accepts traffic from the web security group, and the database tier accepts traffic from the application security group. **Security-group rules alone do not establish end-to-end connectivity**: routes, network ACLs, instance associations and other conditions may also matter.

## 4. Agent, harness, MCP and IAM: division of responsibility

| Concept | Meaning | Security-group example |
|---|---|---|
| LLM | Reasoning model | Identifies which network information is relevant. |
| AI Agent | Goal-directed reasoning-and-tool-use system | Investigates connectivity iteratively. |
| Agent Harness | Execution coordination infrastructure | Routes tool calls and feeds results back. |
| MCP Client | Client side of the MCP connection | Invokes an exposed AWS networking tool. |
| MCP Server | Tool provider / external-system adapter | Retrieves AWS networking information. |
| AWS IAM | Independent technical authorisation | Allows or denies the API call. |

### Conceptual agent loop

```text
Human request
    |
    v
Copilot Chat / Agent
    |
    v
Remote LLM -- decides which information is needed
    |
    v
Copilot Harness -> Local MCP Client
    |
    v
Local AWS Networking MCP Server (launched by uvx)
    |
    v
AWS SDK -> AWS API -> IAM authorisation
    |
    v
AWS networking configuration
    |
    v
MCP Server -> MCP Client -> Harness
    |
    v
Remote LLM -- analyses evidence
    |
    +-- More information needed? -> another authorised tool call
    |
    v
Final answer in Copilot Chat
```

## 5. Architectural conclusions

The LLM does not inherently know the live configuration of the AWS environment. It uses MCP tools to obtain current evidence. Copilot supplies the agentic interaction and orchestration; the remote LLM supplies reasoning; the local AWS Networking MCP Server supplies AWS integration; IAM enforces access; and AWS APIs supply infrastructure data.

**Classification:** A **hybrid, MCP-enabled agentic AI troubleshooting architecture** using GitHub Copilot Agent Mode in VS Code, a remote LLM, a locally executed AWS Networking MCP Server and IAM-governed AWS API access.

**Boundary:** The architecture describes the documented Exercise 2 setup and an illustrative security-group query. It does not independently verify the exact model deployment, AWS credential source, or tool-call transcript.
