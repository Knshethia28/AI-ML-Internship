# Day 27 — Project Planning Tasks

## 1. Plan One Complete AI Project

### Project Title: ShopEase – AI-Powered Multi-Agent E-Commerce Customer Support Assistant

**Domain:** Artificial Intelligence / E-Commerce  
**Project Complexity:** Moderate

### Project Overview

ShopEase is a multi-agent AI-powered customer support assistant designed to help customers resolve common e-commerce queries through a coordinated workflow of specialized agents.

The system accepts customer queries, retrieves relevant information from a knowledge base, analyses the retrieved content, generates a response and evaluates the response before presenting it to the customer.

The existing prototype uses Python and LangGraph to coordinate five specialized agents: Coordinator, Research, Analyzer, Writer and Critic. It includes a local JSON knowledge base, a command-line interface and a FastAPI backend.

The planned project focuses on improving this foundation by introducing Retrieval-Augmented Generation (RAG), external LLM integration and selected customer-service tools such as order-status lookup. These additions aim to make the system more informative, context-aware and useful for practical e-commerce support.

### Problem Statement

E-commerce customers frequently need assistance with order delays, delivery information, returns, refunds and product-related queries. Traditional support systems may depend on static FAQs or require customers to navigate several pages to find relevant information.

A basic automated chatbot may also provide incomplete or unsupported answers when it cannot retrieve suitable information.

ShopEase aims to address these limitations through a multi-agent workflow that retrieves relevant information, analyses it and generates responses based on available sources. Future integration with order-management tools can further allow the system to retrieve specific customer information instead of relying only on general support articles.

### Project Objectives

- Accept and process customer queries through a conversational interface.
- Retrieve relevant information from an e-commerce support knowledge base.
- Coordinate specialized agents using LangGraph.
- Analyse retrieved information before generating a response.
- Generate clear, relevant and source-supported customer responses.
- Evaluate generated responses and handle unsupported queries appropriately.
- Integrate RAG to improve information retrieval from a larger collection of documents.
- Support selected customer-service operations through backend tools.
- Provide API access for integration with a frontend or other applications.

### Project Scope

**Features included:**
- Multi-agent workflow using LangGraph.
- Customer query processing.
- Knowledge-base search and information retrieval.
- Response analysis and generation.
- Critic-based response evaluation.
- Revision handling for responses that fail evaluation.
- Command-line interaction.
- FastAPI endpoints for customer queries and application health checks.
- Retrieval-Augmented Generation using embeddings and vector search.
- External LLM integration for improved language understanding and response generation.
- Basic order-status lookup through a backend tool.
- Error handling, logging and testing.

**Features outside the initial scope:**
- Complete e-commerce shopping and checkout functionality.
- Payment processing and financial transactions.
- Autonomous refund approvals or financial decisions.
- Training a custom large language model.
- Advanced recommendation and demand-prediction systems.
- Voice-based customer support.
- Enterprise-scale infrastructure and large-scale deployment.

### Proposed Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Agent Workflow | LangGraph |
| Backend API | FastAPI |
| Knowledge Base | JSON and structured support documents |
| Retrieval System | RAG, embeddings and vector search |
| AI Integration | External LLM API |
| Data Storage | JSON initially; database integration for future expansion |
| Testing | Pytest |
| Version Control | Git and GitHub |
| Deployment | Docker and cloud hosting provider (to be selected) |

### Expected Outcome

The expected outcome is an improved ShopEase customer support application that can process customer queries through a coordinated multi-agent workflow, retrieve relevant information from its knowledge base and generate useful responses.

The planned system will extend the existing prototype with semantic document retrieval, external LLM integration and a basic order-status lookup capability.

The project will also include API integration, testing, error handling, documentation and deployment planning within an eight-week schedule.

---

## 2. Sprint Planning Exercise

The project is divided into four sprints, with each sprint lasting two weeks. Each sprint focuses on a specific stage of development and produces an output required for the following stage.

| Sprint | Duration | Main Activities | Expected Outcome |
|---|---|---|---|
| Sprint 1 | Weeks 1–2 | Review existing ShopEase functionality, finalize requirements, document architecture, organize project modules and prepare the development environment | Reviewed project foundation and finalized technical plan |
| Sprint 2 | Weeks 3–4 | Implement RAG, prepare support documents, generate embeddings, configure vector search and integrate retrieval with the Research Agent | Improved knowledge retrieval functionality |
| Sprint 3 | Weeks 5–6 | Integrate an external LLM, improve response generation and evaluation, develop basic order-status lookup and connect the components through the API | Enhanced multi-agent customer support application |
| Sprint 4 | Weeks 7–8 | Perform testing, fix defects, verify API behaviour, improve documentation, prepare deployment and complete final demonstration | Tested, documented and deployment-ready application |

### Sprint Execution Approach

- Tasks are selected based on their priority, complexity and dependencies.
- Each sprint begins with planning and assignment of responsibilities.
- Existing modules are reviewed before introducing changes to avoid unnecessary duplication.
- Progress is reviewed regularly through team discussions.
- Completed work is integrated and reviewed before being considered finished.
- At the end of each sprint, the team evaluates the completed work and plans improvements for the next sprint.

The final sprint is specifically allocated to testing, stabilization, documentation and deployment preparation to ensure that the planned project work is completed by the end of Week 8.

---

## 3. Estimate the Effort Required for Each Project Task

Each task is assigned a complexity level based on the effort, technical difficulty and coordination required.

| Complexity | Description |
|---|---|
| Low | Simple tasks with clearly defined requirements and minimal dependencies |
| Medium | Tasks requiring multiple steps, moderate technical effort or coordination |
| High | Complex tasks involving technical uncertainty, integration or multiple dependencies |

| Task ID | Project Task | Sprint | Complexity |
|---|---|---|---|
| T01 | Review existing ShopEase functionality and define project objectives | 1 | Medium |
| T02 | Identify functional and non-functional requirements | 1 | Medium |
| T03 | Review and document the multi-agent architecture and component interactions | 1 | High |
| T04 | Organize support documents and define the knowledge-base structure | 1 | Medium |
| T05 | Review repository structure and development environment | 1 | Low |
| T06 | Finalize module responsibilities and API integration requirements | 1 | Medium |
| T07 | Prepare support documents for Retrieval-Augmented Generation | 2 | Medium |
| T08 | Generate embeddings for support documents | 2 | High |
| T09 | Configure vector storage and semantic retrieval | 2 | High |
| T10 | Integrate RAG retrieval with the existing Research Agent | 2 | High |
| T11 | Test retrieval accuracy and handling of unsupported queries | 2 | Medium |
| T12 | Integrate an external LLM with the response-generation workflow | 3 | High |
| T13 | Improve Writer and Critic agents for response quality and evaluation | 3 | High |
| T14 | Develop a basic order-status lookup tool | 3 | Medium |
| T15 | Integrate the order lookup tool into the multi-agent workflow | 3 | Medium |
| T16 | Connect and verify the complete workflow through FastAPI | 3 | High |
| T17 | Execute unit, API, integration and workflow testing | 4 | High |
| T18 | Fix defects and perform regression testing | 4 | Medium |
| T19 | Prepare Docker configuration and deployment setup | 4 | Medium |
| T20 | Perform deployment verification and smoke testing | 4 | Medium |
| T21 | Prepare technical documentation and API usage instructions | 4 | Medium |
| T22 | Prepare final demonstration and project handover | 4 | Low |

---

## 4. Prioritize Tasks Based on Business Value and Dependencies

Task priorities are assigned by considering their importance to the project's main objectives and whether other tasks depend on their completion.

| Priority | Description |
|---|---|
| P1 – High | Essential tasks required for core functionality or successful project completion |
| P2 – Medium | Important supporting tasks that improve usability, quality or maintainability |
| P3 – Low | Optional enhancements that can be postponed without affecting the core deliverable |

The detailed task-wise priority table, including business value and dependencies, is provided in the separate **Day 27 – Sprint Planning Document**.