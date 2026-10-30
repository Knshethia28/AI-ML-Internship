# Sequence Diagram

## 1. Overview

The sequence diagram represents the communication between the customer, application, and five specialized agents in the ShopEase Customer Support System.

It illustrates how a customer query moves through the workflow before a final response is generated.

## 2. Normal Workflow Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Customer
    participant App as Application
    participant C as Coordinator
    participant R as Research Agent
    participant A as Analyzer
    participant W as Writer
    participant K as Critic
    participant KB as Knowledge Base
    participant Log as Communication Log

    Customer->>App: Submit customer query
    App->>C: Initialize workflow state
    C->>R: Pass customer query
    R->>KB: Search knowledge base
    KB-->>R: Return matching articles
    R-->>A: Pass retrieved information
    A-->>W: Pass analysis and key points
    W-->>K: Submit response draft
    K->>K: Review generated response
    K-->>C: Return approval decision
    C->>Log: Record communication trace
    C-->>App: Return final workflow state
    App-->>Customer: Display final response