# ShopEase Multi-Agent System — Day 23 (LangGraph)

## What this project does
This Day 23 folder extends the Day 22 ShopEase prototype by using LangGraph to orchestrate the same five agents: Coordinator, Research Agent, Analyzer, Writer, and Critic.

The agent logic and local knowledge base are reused. LangGraph manages the workflow, shared state, conditional routing, the Critic-to-Writer revision loop, and finalization.

**Important limitation:** The agents are Python classes using deterministic local keyword retrieval and rules. They are not separate LLMs, and this project does not connect to live ShopEase orders or customer accounts. No API key is needed.

## Folder contents
- `main.py` — command-line runner and communication-log writer
- `agents.py` — reused Day 22 agent logic
- `graph.py` — LangGraph state, nodes, edges, routing, error handling
- `knowledge_base.py` — local JSON article loader and keyword search
- `data/knowledge_base.json` — fictional ShopEase help articles
- `tests/test_graph.py` — basic workflow tests
- `workflow_diagram.mmd` — Mermaid flowchart

## Setup (Windows PowerShell / VS Code terminal)
Open the terminal and move into the Day 23 folder:

```powershell
cd "E:\OneDrive - Indian Oil Corporation Limited\Desktop\AI-ML-Internship\Day 23"
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the project

```powershell
python main.py "My order delivery is late"
```

Try other queries:

```powershell
python main.py "How do I return a damaged item?"
python main.py "Explain quantum entanglement"
```

The complete result and per-agent communication trace are saved to:

`outputs/communication_log.json`

You can choose another output file:

```powershell
python main.py "My order is late" --output outputs/late_order_log.json
```

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Workflow
1. Coordinator initializes the graph state.
2. Research Agent retrieves matching local help articles.
3. Analyzer prepares key points, source names, confidence, and escalation flag.
4. Writer creates a customer-facing draft.
5. Critic approves the draft or identifies issues.
6. If a revision is needed and the retry limit has not been reached, the graph routes back to Writer.
7. Finalize returns the answer and records the workflow status.

## Shared state
`AgentGraphState` is a TypedDict that carries the user query, research results, analysis, draft, critique, final answer, revision count, error information, and trace. The trace uses an append reducer so events from successive nodes are accumulated instead of overwritten.

## Error handling
Each agent node catches ordinary Python exceptions, records the error in the state, and routes to finalization. Finalization returns a safe support-escalation message if a node fails.

## Scope and limitations
- Retrieval is keyword-overlap matching against four fictional local help articles.
- No external LLM, internet search, live order lookup, account access, or ticket creation is implemented.
- The communication log records the actual node execution and state workflow; it does not represent messages exchanged between independent model instances.
