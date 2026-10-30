# Agent Communication Flow Document

## 1. Overview

The ShopEase Customer Support System uses LangGraph to coordinate five specialized Python agents. Each agent performs a specific responsibility and passes its output through a shared workflow state.

The communication flow is:

**Coordinator → Research Agent → Analyzer → Writer → Critic → Coordinator**

The Coordinator manages workflow execution, while the remaining agents retrieve information, analyze it, generate a response, and review its quality.

## 2. Agents and Responsibilities

| Agent | Responsibility |
|---|---|
| Coordinator | Initializes the customer request and manages workflow progression. |
| Research Agent | Searches the local ShopEase knowledge base for relevant information. |
| Analyzer | Extracts useful information and evaluates whether the retrieved content is sufficient. |
| Writer | Generates a customer-facing response using the analysis. |
| Critic | Reviews the response and decides whether it should be approved or revised. |

## 3. Communication Flow

### Step 1: Request Initialization
The Coordinator receives the customer's query and initializes the shared workflow state.

### Step 2: Information Retrieval
The Research Agent searches the local JSON knowledge base and retrieves relevant articles.

### Step 3: Analysis
The Analyzer processes the retrieved information, extracts key points, and evaluates the available information.

### Step 4: Response Generation
The Writer prepares a customer-facing response using the information provided by the Analyzer and Research Agent.

### Step 5: Quality Review
The Critic evaluates the generated response for relevance and usefulness.

### Step 6: Revision or Approval
- If the response is approved, the workflow proceeds to finalization.
- If rejected and another attempt is available, the workflow follows the revision path.
- If the revision limit is reached, the workflow proceeds to finalization.

### Step 7: Finalization
The Coordinator completes the workflow and the application saves the agent communication trace.

## 4. Shared State Management

The agents communicate through a shared state maintained by LangGraph.

The state contains information such as:

- Customer query
- Retrieved knowledge-base articles
- Extracted key points
- Analysis and confidence information
- Generated response
- Critic feedback and approval decision
- Revision count and revision limit
- Workflow status and error information
- Agent communication trace

This approach allows agents to exchange information without requiring direct calls between every agent.

## 5. Revision Handling

The Critic determines whether the generated response requires revision.

The workflow uses conditional routing:

- Approved response → Finalization
- Rejected response with retries available → Revision
- Rejected response after reaching the revision limit → Finalization

This prevents the workflow from entering an unlimited revision loop.

## 6. Error Handling

The workflow includes error handling for agent execution failures.

When an exception occurs during the tested Research Agent execution, the error is captured in the shared state and the workflow follows a safe finalization path.

## 7. Verified Execution Example

The application was executed using:

`My order delivery is late`

The observed communication sequence was:

1. Coordinator – Initialized the workflow.
2. Research Agent – Retrieved one matching article.
3. Analyzer – Prepared one key point.
4. Writer – Generated a customer response.
5. Critic – Approved the response.
6. Coordinator – Completed the workflow.

**Workflow Status:** completed  
**Revision Count:** 0  
**Retrieved Articles:** 1

The communication log was successfully generated at:

`outputs/communication_log.json`

## 8. Scope and Limitations

- The agents are Python-based components orchestrated through LangGraph.
- The system uses a local JSON knowledge base.
- The implementation does not use five independent LLMs.
- It does not connect to live ShopEase order databases or delivery APIs.
- It provides general customer-support guidance rather than verifying actual order statuses.

## 9. Conclusion

The communication flow demonstrates how LangGraph coordinates specialized agents through shared state, conditional routing, revision handling, and error handling. The implementation provides a working local prototype of a multi-agent customer-support workflow.