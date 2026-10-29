# Multi-Agent Responsibility Matrix

| Agent | Responsibility | Inputs | Outputs | Dependencies | Communication / shared-state fields |
|---|---|---|---|---|---|
| Coordinator | Orchestrates the workflow, controls order and retry limit, packages final result | User query | Final structured result and status | All agents | Creates `SharedState`; reads `critique`; records workflow events in `trace` |
| Research Agent | Retrieves relevant local help articles | `user_query`, local JSON articles | Ranked article list | Knowledge base | Writes `research_results`; records retrieval in `trace` |
| Analyzer | Summarizes retrieved evidence and decides whether human help is needed | `research_results` | Summary, key points, sources, confidence, escalation flag | Research Agent | Writes `analysis`; records analysis in `trace` |
| Writer | Drafts a concise customer-facing answer from analysis | `analysis`, optional revision note | Answer draft | Analyzer | Writes `draft`; records drafting in `trace` |
| Critic | Checks draft for basic completeness and safe escalation | `draft`, `research_results`, `analysis` | Approval flag and list of issues | Writer; Research Agent; Analyzer | Writes `critique`; records review in `trace` |

## Communication flow

The Coordinator passes the same `SharedState` object to the agents. This avoids agents communicating through hidden global variables. The next agent reads the prior agent's named output field. The Critic's result returns control to the Coordinator, which either accepts the draft or requests a bounded Writer revision.
