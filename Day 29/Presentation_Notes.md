# ShopEase — Presentation Notes

*10-minute speaking guide*

**Suggested duration:** Approximately 10 minutes. Keep the live application demonstration ready separately; these notes support the slides rather than replace the demo.

## 0:00–0:45 | Opening and Problem

Introduce ShopEase as an AI-inspired, multi-agent customer-support demo for an e-commerce setting.

Explain the problem: customers frequently ask about products, delivery, returns and support. ShopEase provides a single chat interface to make these interactions easier to navigate.

## 0:45–1:30 | Project Objectives

Briefly explain the main objectives:

- Retrieve relevant product and support information.
- Handle short follow-up questions using conversation context.
- Generate structured responses through a multi-agent workflow.
- Provide an escalation option when available information is insufficient.

## 1:30–2:45 | Architecture Overview

Walk through the application flow:

**Browser Interface → FastAPI Backend → LangGraph Workflow → Response**

Explain that the workflow uses shared state and separates information retrieval, analysis, response writing and review.

Mention the two information sources:
- Local JSON support knowledge base.
- DummyJSON mock product catalogue.

## 2:45–4:00 | Multi-Agent Workflow

Introduce the five components:

1. **Coordinator:** Manages the workflow.
2. **Research Agent:** Retrieves relevant information.
3. **Analyzer:** Evaluates the query and retrieved information.
4. **Writer:** Prepares the response.
5. **Critic:** Reviews the generated response.

Explain that separating responsibilities makes the workflow modular and easier to maintain.

**Important technical clarification:** The current agents use deterministic Python rules rather than an LLM API.

## 4:00–4:45 | Data Sources and Memory

Explain that product information comes from DummyJSON, while predefined support articles are stored locally in JSON.

Describe session context briefly: the API retains a limited number of recent messages in memory and uses the previous user question to interpret common follow-ups.

## 4:45–5:30 | Escalation and Interface

Explain that customers can submit support requests through the interface.

The backend generates a ticket ID and stores a Pending record in a local JSON file.

Clarify that this is a demonstration queue, not a direct connection to real support staff.

## 5:30–8:00 | Live Demonstration

Demonstrate the following scenarios using the exact tested flows:

1. **Support query:** Ask about a return, refund or delivery policy.
2. **Product search:** Retrieve sample product information.
3. **Follow-up question:** Ask a related question within the same session.
4. **Support escalation:** Submit a support request and show the generated ticket information.

Keep the interactions concise and explain what happens behind the interface.

Avoid demonstrating unverified scenarios.

## 8:00–8:45 | Testing and Limitations

Briefly mention the testing areas:

- Agents and graph workflow.
- API functionality.
- Conversation context.
- Knowledge-base retrieval.
- Product-data parsing.
- Support escalation.

Discuss the current limitations honestly:

- Product information uses mock data.
- The knowledge base is small and keyword-based.
- Conversation history is maintained in memory.
- Tickets are stored locally.
- No LLM API is currently integrated.

## 8:45–9:30 | Challenges and Future Scope

Discuss two key challenges:

- Avoiding unsupported answers when relevant information is unavailable.
- Interpreting follow-up questions using limited conversation context.

Mention realistic future improvements:

- Semantic information retrieval.
- Database-based persistence.
- Real helpdesk integration.
- Authentication and stronger security.
- End-to-end testing.

## 9:30–10:00 | Closing

Conclude:

"ShopEase demonstrates a modular customer-support workflow that combines product retrieval, a local support knowledge base, conversation context and human-support escalation.

Although the current implementation is a demonstration rather than a production-ready system, it provides a foundation that can be extended with real data sources, persistent storage and more advanced AI capabilities.

Thank you. I would be happy to answer your questions."

---

# Delivery Tips

- Use the architecture slide to explain the flow rather than reading every box.
- Keep the demonstration limited to four clear scenarios.
- Explain the user benefit before discussing implementation details.
- Be transparent about the deterministic agents and simulated integrations.
- If a live API call fails, explain that DummyJSON provides external mock data and move to the local support-article scenario.
- Keep an eye on time, especially during the live demonstration.