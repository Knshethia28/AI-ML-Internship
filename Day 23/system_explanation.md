# System Explanation

## 1. Introduction

ShopEase Customer Support is a multi-agent workflow prototype developed using Python and LangGraph.

The system divides customer-support operations into specialized tasks performed by five agents: Coordinator, Research Agent, Analyzer, Writer, and Critic.

Each agent performs a specific responsibility, while LangGraph manages communication and workflow execution.

## 2. Problem Statement

Customer-support queries often require information retrieval, analysis, response generation, and quality checking.

Handling all these responsibilities in a single component can make the system difficult to maintain and test.

The proposed system separates these responsibilities into specialized agents and coordinates them through a shared workflow state.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Implements the application and agent logic. |
| LangGraph | Coordinates agents and manages workflow transitions. |
| JSON | Stores the local customer-support knowledge base. |
| unittest | Performs automated testing of workflow functionality. |

## 4. System Architecture

The system consists of five specialized agents.

### 4.1 Coordinator

The Coordinator initializes the customer request, manages workflow progression, and completes the workflow.

### 4.2 Research Agent

The Research Agent searches the local JSON knowledge base and retrieves articles relevant to the customer's query.

### 4.3 Analyzer

The Analyzer examines the retrieved information, extracts important points, and evaluates whether the available information is sufficient.

### 4.4 Writer

The Writer generates a customer-facing response using the information provided by the previous agents.

### 4.5 Critic

The Critic evaluates the generated response and determines whether it should be approved or revised.

## 5. LangGraph Integration

LangGraph is used to represent the agents as individual workflow nodes.

The nodes are connected through defined transitions, allowing information to move between agents in a controlled sequence.

The workflow also uses conditional routing after the Critic:

- Approved responses proceed to finalization.
- Rejected responses can enter the revision path.
- The revision limit prevents unlimited repetitions.

## 6. State Management

A shared state maintains information throughout workflow execution.

It contains:

- Customer query
- Retrieved articles
- Analysis and extracted key points
- Generated response
- Critic feedback
- Approval status
- Revision count
- Workflow status
- Error information
- Agent communication trace

This allows each agent to access the information required for its task.

## 7. Error Handling

The system includes error handling for agent execution failures.

When the Research Agent encounters an exception, the error is captured in the workflow state and the workflow follows its safe finalization path.

The automated tests verify this specific error-handling scenario.

## 8. Practical Execution

The application was executed using the following command:

```powershell
python main.py "My order delivery is late"
```

The system successfully retrieved a relevant article from the local knowledge base, processed the information through the agents, and generated a customer-facing response.

The Critic approved the generated response, and the workflow completed with a revision count of zero.

## 9. Automated Testing

The application was tested using Python's `unittest` framework.

All eight automated tests passed successfully.

| Test Case | Purpose |
|---|---|
| Late-order query | Checks retrieval and response generation for delayed orders. |
| Return query | Checks handling of return-related questions. |
| Unsupported query | Checks responses when relevant information is unavailable. |
| Empty query | Checks handling of empty customer input. |
| Revision routing | Checks conditional routing after Critic evaluation. |
| Actual revision loop | Checks the Writer revision process. |
| Revision limit | Checks that revisions do not continue indefinitely. |
| Error handling | Checks workflow behavior when an error occurs. |

## 10. Application and Limitations

The prototype demonstrates how specialized agents can collaborate through a shared LangGraph workflow.

It uses a local JSON knowledge base and does not connect to a live ShopEase order database, external carrier tracking service, or production customer-support platform.

The implementation demonstrates agent coordination and workflow management in a controlled local environment.

## 11. Conclusion

The ShopEase Customer Support prototype demonstrates the integration of LangGraph with a multi-agent architecture.

It combines information retrieval, analysis, response generation, review, conditional routing, and error handling into a structured workflow.

The project provides a practical example of how complex customer-support operations can be divided into smaller, manageable agent responsibilities.
