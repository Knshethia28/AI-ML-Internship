# ShopEase — AI-Powered Customer Support Demo

ShopEase is a lightweight customer-support demo built around the existing LangGraph multi-agent workflow. Customers can ask support questions, search a demonstration product catalogue, continue a conversation with session context, and create a human-support ticket.

> **Demo-data notice:** Product information is retrieved from [DummyJSON](https://dummyjson.com/docs/products), a public mock-data API. It is not a live ShopEase inventory. Support articles are sample guidance stored locally. Human-support requests are saved as demo tickets; no real support team is connected.

## Features

- **Multi-agent workflow:** Coordinator, Research, Analyzer, Writer and Critic agents orchestrated with LangGraph.
- **Support knowledge base:** Searches local JSON help articles and returns the article titles used.
- **Product lookup:** Searches DummyJSON when a customer asks about products. Results include the demo price, category, rating and stock count.
- **Conversation context:** Keeps the most recent turns for each browser session and uses the previous customer question to interpret common follow-ups such as "What about a cheaper one?"
- **Human-support escalation:** Saves a support request with a ticket ID and pending status in `data/escalations.json`.
- **Web interface:** Responsive chat UI built with plain HTML, CSS and JavaScript. No frontend framework or build step is required.
- **REST API:** FastAPI endpoints and interactive API documentation.
- **Tests:** Pytest coverage for the workflow, API, knowledge-base search, conversation context, product parsing and ticket creation.

## Project structure

```text
ShopEase/
├── agents.py
├── api.py
├── conversation.py
├── escalations.py
├── graph.py
├── knowledge_base.py
├── logging_config.py
├── main.py
├── product_catalog.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── README.md
├── ARCHITECTURE.md
├── data/
│   └── knowledge_base.json
├── static/
│   ├── app.js
│   ├── index.html
│   └── styles.css
└── tests/
    ├── test_api.py
    ├── test_conversation.py
    ├── test_escalations.py
    ├── test_graph.py
    ├── test_knowledge_base.py
    └── test_product_catalog.py
```

## Requirements

- Python 3.10 or newer
- Internet access when product search is used (the rest of the application can still answer from its local support articles if DummyJSON is unavailable)

## Setup on Windows PowerShell

Open PowerShell in the project folder.

### 1. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create local configuration

```powershell
Copy-Item .env.example .env
```

The defaults work for local development. No API key is required for the DummyJSON product catalogue.

### 4. Start ShopEase

```powershell
uvicorn api:app --reload
```

Open **http://127.0.0.1:8000/app** for the customer interface.

Useful URLs:

- Customer interface: http://127.0.0.1:8000/app
- API documentation: http://127.0.0.1:8000/docs
- Service status: http://127.0.0.1:8000/health
- Knowledge-base readiness: http://127.0.0.1:8000/ready

## Try these demo questions

1. `My order delivery is late`
2. `How do I return a damaged item?`
3. `Show me smartphones`
4. `Do you have laptops under $1000?`
5. After asking about laptops, try `What about a cheaper one?` in the same conversation.
6. `I need help with a problem that is not covered`

Use **Contact support** to create a demo support ticket. The interface displays its ticket ID after it is saved.

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome/status |
| GET | `/app` | Customer-facing web interface |
| GET | `/health` | Liveness check |
| GET | `/ready` | Checks the local support knowledge base |
| POST | `/chat` | Runs the support workflow |
| POST | `/support` | Creates a demo human-support ticket |
| GET | `/sessions/{session_id}` | Reads the current in-memory conversation |\n| DELETE | `/sessions/{session_id}` | Clears one in-memory conversation |

Example request:

```json
{
  "query": "How do I return a damaged item?",
  "session_id": null
}
```

The first response returns a `session_id`. Send that same ID with later messages to preserve conversation context.

## How the system works

1. The browser sends a message to FastAPI.
2. FastAPI loads the recent turns for that session.
3. LangGraph runs the multi-agent workflow.
4. The Research Agent searches the local support articles and, for product-related questions, queries DummyJSON.
5. The Analyzer organizes the retrieved information and classifies the query.
6. The Writer prepares a response using retrieved information.
7. The Critic checks that the response is not empty and that support sources or escalation guidance are included.
8. FastAPI returns the answer, source titles, product results and category to the interface.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the component diagram.

## Run tests

```powershell
pip install -r requirements-dev.txt
python -m pytest -v
```

Product API tests use mocked HTTP responses, so the test suite does not depend on DummyJSON being online.

## Data and limitations

- The knowledge base is a small collection of editable sample support articles in `data/knowledge_base.json`.
- Product data comes from DummyJSON and is illustrative only.
- Conversation history is stored in server memory and is cleared when the API process restarts. It is not a permanent chat database.
- Escalation tickets are appended to `data/escalations.json`. This is a local demo queue, not an actual agent-management system.
- No customer login, payment processing, order-system integration or real retailer inventory is implemented.
- The project does not use an LLM API. Its agents coordinate retrieval, analysis, response composition and review using deterministic Python logic. Do not describe the responses as generated by a trained language model.

## Run the command-line workflow (optional)

```powershell
python main.py "My order delivery is late"
```

The command-line entry point prints the response and agent trace. It is optional; the web interface is the main demonstration path.
