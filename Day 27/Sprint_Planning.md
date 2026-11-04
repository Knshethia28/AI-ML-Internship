# Day 27 — Sprint Planning Document

## Project: ShopEase – AI-Powered Multi-Agent E-Commerce Customer Support Assistant

**Domain:** Artificial Intelligence / E-Commerce  
**Complexity:** Moderate  
**Total Duration:** 8 Weeks  
**Sprint Structure:** 4 Sprints of 2 Weeks Each

---

# 1. Sprint Planning Document

## 1.1 Project Overview

ShopEase is an AI-powered e-commerce customer support assistant designed to help customers resolve common shopping-related queries through an organized multi-agent workflow.

The system uses a LangGraph-based architecture consisting of five specialized agents: Coordinator, Research, Analyzer, Writer and Critic. Each agent performs a specific responsibility, allowing customer queries to be processed through a structured sequence of operations.

The existing application uses a local JSON knowledge base containing support articles. The Research Agent retrieves relevant information, the Analyzer Agent extracts important points, the Writer Agent prepares a customer-friendly response, and the Critic Agent evaluates the generated response before it is returned.

The project also includes a command-line interface and a FastAPI backend that exposes endpoints for interacting with the assistant.

The proposed development plan focuses on improving the existing system through Retrieval-Augmented Generation (RAG), external LLM integration, improved response evaluation and basic read-only order-status lookup.

The objective is to develop a more capable and reliable customer support assistant while maintaining the modular multi-agent architecture of the existing ShopEase project.

## 1.2 Project Requirements

### Functional Requirements

| ID | Requirement | Description |
|---|---|---|
| FR01 | Customer Query Input | Customers can submit e-commerce-related questions through the application. |
| FR02 | Query Coordination | The Coordinator Agent identifies the query and directs it through the appropriate workflow. |
| FR03 | Knowledge Retrieval | The Research Agent retrieves relevant information from the available support knowledge base. |
| FR04 | Query Analysis | The Analyzer Agent extracts important information and identifies whether the available knowledge is sufficient. |
| FR05 | Response Generation | The Writer Agent prepares clear and relevant customer support responses. |
| FR06 | Response Evaluation | The Critic Agent evaluates generated responses and determines whether revision or human assistance is required. |
| FR07 | Revision Workflow | The system supports a controlled revision process when a generated response does not satisfy evaluation criteria. |
| FR08 | Order Status Lookup | Customers can request basic order-status information through a read-only lookup mechanism. |
| FR09 | API Access | The application exposes endpoints through FastAPI for submitting queries and checking application health. |
| FR10 | Conversation Logging | The system records relevant workflow information and communication logs for review and debugging. |

### Non-Functional Requirements

- **Performance:** Customer queries should be processed within a reasonable response time.
- **Usability:** The application should provide simple and understandable interaction through its available interface.
- **Reliability:** Invalid inputs, missing information and application errors should be handled appropriately.
- **Response Quality:** Generated responses should be relevant, understandable and grounded in available support information.
- **Security:** API configuration, credentials and sensitive information should be protected.
- **Maintainability:** Agents and application components should have clearly separated responsibilities.
- **Scalability:** The architecture should allow future expansion of the knowledge base and additional customer support capabilities.
- **Testability:** Individual agents, workflow transitions and API endpoints should be testable independently.

## 1.3 Proposed System Architecture

ShopEase follows a modular multi-agent architecture in which different agents handle specific stages of customer query processing.

The existing system uses Python and LangGraph to coordinate the agents, a JSON-based knowledge base for retrieving support information, and FastAPI for exposing application functionality through HTTP endpoints.

The proposed architecture extends this existing foundation by introducing semantic retrieval through RAG, external LLM integration and a basic read-only order lookup mechanism.

### Architecture Components

| Component | Responsibility |
|---|---|
| Customer Interface | Provides an interface through which customers can submit queries and receive responses. The existing command-line interface can be used, with the FastAPI documentation interface available for API interaction. |
| FastAPI Backend | Receives customer requests, validates inputs using Pydantic and coordinates communication with the ShopEase workflow. |
| LangGraph Workflow | Controls the execution order of agents, manages state transitions and supports conditional routing and revision loops. |
| Coordinator Agent | Receives the customer query, identifies the required processing path and coordinates the workflow. |
| Research Agent | Searches the support knowledge base and retrieves relevant articles or information. |
| Analyzer Agent | Processes retrieved information, extracts important points and determines whether sufficient information is available. |
| Writer Agent | Generates clear and customer-friendly responses using the available information and LLM integration. |
| Critic Agent | Evaluates the generated response, checks whether it satisfies defined criteria and determines whether revision or human assistance is necessary. |
| Knowledge Base | Stores structured e-commerce support articles in JSON format. It acts as the primary source of information for customer support responses. |
| Vector Store | Stores embeddings generated from support articles and enables semantic retrieval based on the meaning of customer queries. |
| Order Lookup Module | Provides basic read-only access to sample order records to answer supported order-status queries. |
| External LLM Service | Supports natural-language understanding and response generation through an external language model API. |
| Logging and Monitoring | Records application activity, workflow execution details, errors and communication logs for debugging and evaluation. |

### System Architecture Flow

The system operates through two main processes: knowledge-base preparation and customer query processing.

**A. Knowledge Base Preparation and Indexing**

The existing ShopEase application uses a local JSON knowledge base. The proposed RAG extension introduces an additional indexing process so that support articles can also be retrieved using semantic similarity.

```text
          SUPPORT ARTICLES
                 |
                 v
          JSON KNOWLEDGE BASE
                 |
                 v
          ARTICLE PROCESSING
                 |
                 v
          TEXT PREPROCESSING
                 |
                 v
        EMBEDDING GENERATION
          (Embedding Model)
                 |
                 v
             VECTOR STORE
          (Stored Embeddings)
```

1. Support articles are maintained in the existing JSON knowledge base.
2. The article-processing module reads the available articles and prepares their content for indexing.
3. The embedding model converts the article content into numerical vector representations.
4. The generated embeddings are stored in a vector store along with references to their corresponding support articles.
5. The indexed information can subsequently be used by the Research Agent during customer query processing.
6. The existing keyword-based retrieval mechanism can be retained as a fallback where appropriate.

**B. Customer Query and Response Processing**

```text
                  CUSTOMER
                      |
                      v
              CUSTOMER INTERFACE
                      |
                      v
               FASTAPI BACKEND
                      |
                      v
              LANGGRAPH WORKFLOW
                      |
                      v
               COORDINATOR AGENT
                      |
                      v
                RESEARCH AGENT
                      |
             +--------+---------+
             |                  |
             v                  v
       KNOWLEDGE BASE       VECTOR STORE
       (JSON Articles)   (Semantic Retrieval)
             |                  |
             +--------+---------+
                      |
                      v
                ANALYZER AGENT
                      |
                      v
                 WRITER AGENT
                 (LLM Support)
                      |
                      v
                 CRITIC AGENT
                      |
              +-------+-------+
              |               |
              v               v
           APPROVED         REVISION
              |               |
              |               v
              |          WRITER AGENT
              |               |
              |               v
              |          CRITIC AGENT
              |               |
              +-------+-------+
                      |
                      v
              FINAL RESPONSE
                      |
                      v
              CUSTOMER INTERFACE
```

**Additional Order Lookup Flow**

```text
             CUSTOMER QUERY
                    |
                    v
             COORDINATOR AGENT
                    |
                    v
           ORDER-RELATED QUERY?
                    |
                    v
             ORDER LOOKUP MODULE
                    |
                    v
             SAMPLE ORDER DATA
                    |
                    v
            ORDER STATUS RESULT
                    |
                    v
             RESPONSE GENERATION
                    |
                    v
             CRITIC EVALUATION
                    |
                    v
             CUSTOMER RESPONSE
```

**Process Explanation:**

1. **Customer Input:** The customer submits an e-commerce-related query through the available interface.
2. **Request Handling:** FastAPI receives the request, validates the input and passes it to the LangGraph workflow.
3. **Query Coordination:** The Coordinator Agent identifies the nature of the query and determines the appropriate processing path.
4. **Knowledge Retrieval:** The Research Agent searches the existing JSON knowledge base and, after the proposed RAG extension, can also retrieve semantically relevant support articles from the vector store.
5. **Information Analysis:** The Analyzer Agent examines the retrieved information, extracts important points and determines whether the available information is sufficient to prepare a response.
6. **Response Generation:** The Writer Agent prepares a customer-friendly response using the retrieved information. An external LLM can be integrated to improve natural-language generation.
7. **Response Evaluation:** The Critic Agent checks the generated response against defined evaluation criteria.
8. **Revision Handling:** If the response does not satisfy the evaluation criteria, the workflow can route it back to the Writer Agent for revision, subject to a controlled revision limit.
9. **Human Assistance:** If sufficient information is unavailable or the query cannot be handled safely, the system can direct the customer towards human support instead of generating unsupported information.
10. **Order Lookup:** For supported order-related queries, the Order Lookup Module retrieves basic information from sample order records through a read-only operation.
11. **Final Response:** The approved response is returned through the FastAPI backend to the customer interface.
12. **Logging:** Relevant workflow information and communication details are recorded to support debugging, testing and future improvements.

### Data Storage and External Services

The architecture uses the existing JSON knowledge base along with an additional vector-storage component for the proposed RAG functionality.

- **JSON Knowledge Base:** Stores structured customer support articles, including information about orders, delivery, returns and other common e-commerce issues.
- **Vector Store:** Stores embeddings generated from support articles and enables semantic retrieval based on the meaning of customer queries.
- **Sample Order Data:** Stores basic sample order information for demonstrating read-only order-status lookup.
- **Communication Logs:** Store relevant query-processing and agent communication information for debugging and evaluation.

External AI services support the proposed natural-language processing capabilities:

- **LLM API:** Used by the Writer Agent to generate more natural and context-aware customer responses. It may also support selected query-understanding tasks.
- **Embedding Model:** Converts support articles and customer queries into numerical vector representations for semantic retrieval.

The existing Python and LangGraph implementation will remain the foundation of the application. The exact LLM provider, embedding model and vector-store implementation will be finalized during development.

**Note:** The existing ShopEase application already contains the multi-agent workflow, JSON knowledge base, command-line interface and FastAPI backend. RAG, external LLM integration and the extended order lookup functionality represent planned improvements and should not be considered implemented until they have been developed and tested.

## 1.4 Proposed Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Programming Language | Python | Core application development and agent implementation |
| Agent Workflow | LangGraph | Agent coordination, workflow execution and conditional routing |
| Backend | FastAPI | API development and request handling |
| Data Validation | Pydantic | Request validation and structured data handling |
| Knowledge Storage | JSON | Storage of customer support articles |
| Semantic Search | Embeddings and Vector Store | Similarity-based retrieval of relevant support information |
| AI Integration | External LLM API | Natural-language response generation |
| Testing | Pytest | Unit, workflow and API testing |
| Logging | Python Logging | Application activity and error tracking |
| Containerization | Docker | Consistent application packaging and execution |
| Version Control | Git and GitHub | Source code management and collaboration |
| Deployment | Cloud hosting provider | Application hosting and accessibility |

The exact LLM provider, embedding model and vector-store implementation will be selected during project development.

## 1.5 Team Roles and Workflow

### Proposed Team Roles

| Team Role | Responsibilities |
|---|---|
| Project Coordinator / Backend Integrator | Coordinate development activities, track sprint progress and integrate the different application components. |
| Agent Workflow Developer | Maintain the LangGraph workflow, agent communication, state management and conditional routing. |
| AI / LLM Developer | Integrate the external LLM API and improve natural-language response generation. |
| Knowledge Retrieval Developer | Improve knowledge-base retrieval and implement embeddings, vector search and RAG functionality. |
| Testing / API Developer | Handle FastAPI integration, testing, error handling, documentation and deployment verification. |

These are proposed responsibilities for a five-member team. Individual assignments can be made according to team members' skills and sprint requirements.

### Team Workflow

1. **Sprint Planning:** Define the sprint objective, select tasks and assign responsibilities.
2. **Task Assignment:** Divide larger development activities into smaller, manageable tasks.
3. **Daily Stand-ups:** Discuss completed work, upcoming tasks and any blockers.
4. **Git Collaboration:** Work using separate feature branches to reduce conflicts between team members.
5. **Code Review:** Review code changes and verify compatibility before merging.
6. **Integration:** Combine completed agents, APIs and supporting modules and check their interactions.
7. **Sprint Review:** Demonstrate completed functionality and evaluate progress against the sprint objectives.
8. **Sprint Retrospective:** Identify difficulties and improvements that can be applied in the next sprint.

A shared task board can use the following statuses:

`To Do → In Progress → In Review → Testing → Done`

## 1.6 Sprint-wise Task Plan

| Sprint | Duration | Tasks | Expected Deliverable |
|---|---|---|---|
| Sprint 1 | Weeks 1–2 | Review the existing ShopEase repository, identify current capabilities and limitations, finalize requirements, plan the extended architecture, review agent responsibilities and prepare development tasks. | Reviewed project foundation and finalized development plan |
| Sprint 2 | Weeks 3–4 | Improve knowledge retrieval, prepare support articles for indexing, generate embeddings, implement semantic retrieval and integrate RAG with the Research Agent. | Improved knowledge retrieval with semantic search |
| Sprint 3 | Weeks 5–6 | Integrate an external LLM, improve Writer and Critic Agents, implement basic read-only order lookup and integrate the extended workflow with FastAPI. | Improved multi-agent customer support application |
| Sprint 4 | Weeks 7–8 | Perform unit, workflow and API testing, fix defects, conduct regression testing, prepare deployment configuration, update documentation and complete the final demonstration. | Tested, documented and deployment-ready application |

---

# 2. Task Priority Table

## 2.1 Priority Definitions

| Priority | Meaning |
|---|---|
| P1 – High | Essential for the core functionality, critical dependencies or final project completion. |
| P2 – Medium | Important supporting functionality that improves usability or application quality. |
| P3 – Low | Optional enhancements that can be postponed without blocking the core release. |

## 2.2 Complexity Definitions

| Complexity | Meaning |
|---|---|
| Low | Simple task with clearly defined steps and minimal dependencies. |
| Medium | Task requiring multiple steps or moderate coordination. |
| High | Complex task involving technical uncertainty, workflow integration or several dependencies. |

## 2.3 Detailed Task Priority Table

| ID | Project Task | Sprint | Complexity | Business Value | Priority | Dependencies |
|---|---|---|---|---|---|---|
| T01 | Review existing ShopEase functionality and define project objectives | 1 | Medium | High | P1 | None |
| T02 | Analyse functional and non-functional requirements | 1 | Medium | High | P1 | T01 |
| T03 | Design the extended system architecture and agent workflow | 1 | High | High | P1 | T02 |
| T04 | Review the existing JSON knowledge base and identify retrieval improvements | 1 | Medium | High | P1 | T01 |
| T05 | Review repository structure and development environment | 1 | Low | High | P1 | T01 |
| T06 | Finalize development setup, module responsibilities and integration plan | 1 | Medium | High | P1 | T03, T04, T05 |
| T07 | Improve customer query processing and Coordinator Agent routing | 2 | Medium | High | P1 | T03, T06 |
| T08 | Prepare support articles and generate embeddings | 2 | High | High | P1 | T04, T06 |
| T09 | Implement semantic retrieval and integrate it with the Research Agent | 2 | High | High | P1 | T08 |
| T10 | Integrate RAG results into the existing LangGraph workflow | 2 | High | High | P1 | T07, T09 |
| T11 | Test knowledge retrieval and agent workflow behaviour | 2 | Medium | High | P1 | T07, T09, T10 |
| T12 | Integrate an external LLM API with the Writer Agent | 3 | High | High | P1 | T10 |
| T13 | Improve response evaluation and revision handling in the Critic Agent | 3 | Medium | High | P1 | T12 |
| T14 | Implement basic read-only order-status lookup | 3 | Medium | Medium | P2 | T06, T07 |
| T15 | Improve human-assistance handling and response fallback behaviour | 3 | Medium | Medium | P2 | T12, T13 |
| T16 | Integrate the extended agent workflow with FastAPI | 3 | High | High | P1 | T10, T12, T13 |
| T17 | Execute unit, workflow and API testing | 4 | High | High | P1 | T16 |
| T18 | Fix identified defects and perform regression testing | 4 | Medium | High | P1 | T17 |
| T19 | Prepare application configuration and deployment setup | 4 | High | High | P1 | T18 |
| T20 | Perform deployment verification and smoke testing | 4 | Medium | High | P1 | T19 |
| T21 | Update technical documentation and application setup instructions | 4 | Medium | High | P1 | T16, T19 |
| T22 | Prepare final demonstration and project handover | 4 | Low | High | P1 | T20, T21 |

## 2.4 Basis for Prioritization

- **Existing project foundation:** Reviewing the current ShopEase implementation is important because the proposed improvements must work with the existing agents, workflow and API structure.
- **Core retrieval functionality:** Knowledge-base improvements, embeddings and semantic retrieval receive high priority because the quality of retrieved information directly affects the responses generated by the assistant.
- **Agent workflow dependencies:** Query routing, retrieval, response generation and response evaluation must work together before the extended application can be considered complete.
- **Supporting functionality:** Order-status lookup and improved human-assistance handling provide additional customer support capabilities but are secondary to the core knowledge retrieval and response workflow.
- **Final delivery:** Testing, defect correction, deployment preparation, documentation and demonstration are essential activities and must be completed before the end of Week 8.

---

# 3. Project Timeline

## 3.1 Eight-Week Project Timeline

| Week | Sprint | Planned Activities | Expected Milestone |
|---|---|---|---|
| Week 1 | Sprint 1 | Review the existing ShopEase repository, inspect the five agents, understand the LangGraph workflow and identify current application capabilities. | Existing project structure and functionality reviewed |
| Week 2 | Sprint 1 | Finalize requirements, identify improvements, prepare the extended architecture, define module responsibilities and finalize the development plan. | Extended project architecture and development plan ready |
| Week 3 | Sprint 2 | Review support articles, prepare knowledge-base content for indexing and implement embedding generation. | Knowledge-base indexing process prepared |
| Week 4 | Sprint 2 | Implement semantic retrieval, integrate retrieval results with the Research Agent and test representative customer queries. | RAG-based knowledge retrieval ready |
| Week 5 | Sprint 3 | Integrate the external LLM API with the Writer Agent and improve response generation and Critic evaluation. | Improved response generation and evaluation |
| Week 6 | Sprint 3 | Implement basic read-only order-status lookup, improve fallback behaviour and integrate the extended workflow with FastAPI. | Extended multi-agent application integrated |
| Week 7 | Sprint 4 | Perform unit, workflow and API testing. Identify defects, improve error handling and execute regression tests. | Tested release candidate |
| Week 8 | Sprint 4 | Prepare deployment configuration, verify application execution, update technical documentation, prepare the final demonstration and complete project handover. | Final project completed and deployment-ready |

## 3.2 Testing Plan

| Testing Type | Purpose | Planned Timing |
|---|---|---|
| Unit Testing | Verify individual agent functions, knowledge retrieval operations and supporting modules. | Sprint 2 onwards; major testing in Week 7 |
| Workflow Testing | Verify agent execution order, state transitions, conditional routing and revision handling. | Sprint 2 onwards; major testing in Week 7 |
| API Testing | Verify FastAPI endpoints, request validation, response formats and error handling. | Sprint 1 onwards; major testing in Week 7 |
| Integration Testing | Verify communication between LangGraph agents, knowledge retrieval, LLM services and the FastAPI backend. | Weeks 6–7 |
| End-to-End Testing | Verify the complete customer query flow from input submission to final response generation. | Week 7 |
| Error Handling Testing | Verify application behaviour for invalid inputs, unavailable information and external service failures. | Weeks 6–7 |
| Regression Testing | Ensure that new changes do not break existing CLI, API or multi-agent functionality. | Weeks 7–8 |
| Smoke Testing | Verify that the deployed application starts correctly and its critical endpoints and workflows function. | Week 8 |

## 3.3 Deployment and Documentation Plan

| Activity | Timeline | Expected Output |
|---|---|---|
| Deployment preparation | Week 7 | Application configuration, environment variables and deployment requirements prepared |
| Container configuration | Week 7 | Docker configuration reviewed and updated where required |
| Application deployment | Week 8 | Backend application deployed with the required configuration |
| Deployment verification | Week 8 | Successful startup, health checks and critical workflow verification |
| Technical documentation | Weeks 7–8 | Architecture overview, agent responsibilities, workflow details and API documentation |
| Setup documentation | Week 8 | Installation instructions, environment configuration and application execution steps |
| User documentation | Week 8 | Instructions for submitting queries and understanding customer support responses |
| Final demonstration | Week 8 | Working ShopEase application demonstrated to the reviewer or team |
| Project handover | Week 8 | Source code, documentation and deployment details handed over |

## 3.4 Definition of Project Completion

The project will be considered complete only when all the following conditions are satisfied:

- The existing ShopEase application has been reviewed and the planned improvements have been integrated.
- The multi-agent workflow operates correctly with the updated knowledge retrieval and response-generation components.
- The planned RAG functionality has been implemented and tested.
- External LLM integration and the improved response evaluation process work as expected.
- The basic read-only order-status lookup functions correctly for supported sample records.
- Required unit, workflow, API and integration tests have been performed.
- Identified critical defects have been resolved and retested.
- The application has been successfully prepared for deployment and its execution has been verified.
- Technical documentation and application setup instructions are ready.
- The final demonstration and project handover are complete.

**Final Deadline: End of Week 8**

The existing ShopEase application provides the foundation for the planned improvements. Development and feature integration are intended to be substantially complete by the end of Week 6. Weeks 7 and 8 are reserved for testing, stabilization, deployment preparation, documentation and handover. No essential release activity is intended to remain pending after Week 8.