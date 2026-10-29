# ShopEase Multi-Agent Research Assistant — Day 22

A beginner-friendly Python demonstration of a coordinated five-agent workflow. The agents are separate Python classes with explicit responsibilities; they are **not** five independently trained AI models. Retrieval and review are deterministic and use a small local JSON knowledge base, so no API key, internet connection, or paid service is needed.

## Agents

1. **Coordinator** — initializes shared state, controls execution order, limits review retries, and returns the final result.
2. **Research Agent** — searches local help articles using keyword overlap and records retrieved articles.
3. **Analyzer** — converts retrieved articles into key points, source titles, a confidence label, and a flag for human assistance.
4. **Writer** — formats the analyzed information into a customer-facing answer and names its reference articles.
5. **Critic** — checks for an empty draft, missing source names, or missing escalation guidance; returns approval or issues.

## Requirements

- Python 3.10 or later recommended
- No third-party packages required

## Run in VS Code terminal

```bash
cd Linkific_Day_22_Multi_Agent_Project
python main.py "My order delivery is late"
```

Try a return question:

```bash
python main.py "How do I return a damaged item?" --output outputs/return_question.json
```

If no question is provided, the program prompts for one. A structured JSON result is written to `output.json` by default. It includes the final answer, research results, analysis, critique, revision count, timestamps, and an execution trace.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Shared state and communication

`SharedState` is the shared workspace. Each agent receives the state object and writes its output to a named field (`research_results`, `analysis`, `draft`, or `critique`). The coordinator invokes agents in sequence and adds trace events, making communication and dependencies inspectable.

## Workflow and limitations

The flow is Coordinator → Research Agent → Analyzer → Writer → Critic. If the Critic finds an issue, the Coordinator can request a Writer revision up to the configured limit. Unsupported queries receive a safe response directing the customer to support instead of fabricating an answer. This is a workflow prototype, not a production customer-service system: keyword matching is simple, the articles are fictional sample data, and no live order/account systems are connected.
