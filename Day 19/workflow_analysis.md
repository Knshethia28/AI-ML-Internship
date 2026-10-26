# Day 19 — LangGraph Workflow Analysis Report

## 1. Objective

Analyze a LangGraph workflow using nodes, graphs, shared state, conditional routing, loops, and memory. Identify a failure scenario and explain how conditional routing and error handling help the workflow recover.

## 2. Workflow Overview

The implemented workflow follows this sequence:

**User → Question → Retriever → LLM → Answer → Memory**

The workflow receives a user's question, searches a small knowledge base for relevant documents, generates an answer using Google Gemini, and stores the question and answer in conversation memory.

### Main Components

- **Question Node:** Receives and stores the user's question in the workflow state.
- **Retriever Node:** Searches the available knowledge base using keyword matching and records the retrieval attempt.
- **LLM Node:** Uses Gemini 3.8 Flash to generate an answer from the retrieved information.
- **Memory Node:** Stores the question and generated or fallback answer in a list.
- **Conditional Routing:** Determines whether the workflow should generate an answer, retry retrieval, or return a fallback response.

## 3. State Management

The workflow uses a shared state to pass information between nodes. Its fields include:

- `question`: The user's input.
- `documents`: The documents retrieved for the question.
- `answer`: The generated or fallback answer.
- `retry_count`: The number of retrieval attempts.
- `memory`: The stored question-and-answer history for the current run.
- `llm_error`: Information associated with an LLM error.

This shared state allows different nodes to access and update the information required for their operations.

## 4. Conditional Routing and Recovery

The retriever checks whether relevant documents have been found.

- If relevant documents are available, the workflow proceeds to the LLM node.
- If no relevant documents are found and retries remain, conditional routing sends the workflow back to the retriever.
- If the retry limit is reached, the workflow returns a fallback answer instead of continuing indefinitely.
- The memory node stores the question and final response.

### Failure Scenario Tested

**Input:** `Explain quantum teleportation`

**Observed result:** The retriever found zero documents, made retry attempts, and eventually returned the fallback response:

> I could not find relevant information. Please try a more specific question.

The question and fallback response were also stored in conversation memory. This test demonstrated that the workflow could handle an unsuccessful retrieval without requiring a relevant document to be present.

## 5. Successful Execution

**Input:** `What is Python?`

The workflow retrieved one document and generated the following response through Gemini:

> Python is a programming language that is used for automation and data analysis.

The final response was displayed, and the question-answer pair was stored in conversation memory. This verified the main workflow path, from question input through retrieval and LLM generation to memory storage.

## 6. Limitations and Observations

- Retrieval uses keyword matching against a small, predefined knowledge base; it is not a semantic search system.
- Memory is maintained in a list for the current run and is not persistent across separate executions.
- Gemini API response times were inconsistent during testing, although a complete successful execution was verified.
- The quality of generated answers depends on the information retrieved and the behavior of the language model.

## 7. Conclusion

The workflow demonstrates how LangGraph nodes, shared state, conditional edges, retry loops, and memory can work together in a question-answering application. The successful question-answer test and the no-document fallback test demonstrate both the normal execution path and a retrieval failure recovery path. Further improvements could include semantic retrieval, persistent memory, and more extensive testing of API failures.