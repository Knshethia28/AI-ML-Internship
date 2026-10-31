
# ShopEase – AI-Powered Customer Support System

ShopEase is an AI-powered customer support application built using Python and LangGraph. It processes customer queries through a multi-agent workflow and retrieves relevant information from a local JSON knowledge base.

The project includes a command-line interface, REST API, automated tests, application logging, environment-based configuration, and Docker deployment support.

## Features

- Multi-agent customer support workflow using LangGraph.
- Local knowledge-base search for relevant support articles.
- REST API built with FastAPI.
- Input validation using Pydantic.
- Automated unit and API tests using Pytest.
- Application logging to both console and log files.
- Environment variable configuration using `.env`.
- Docker-based application deployment.
- Liveness and readiness monitoring endpoints.

## Project Structure

```text
Day 24/
│
├── agents.py
├── api.py
├── graph.py
├── knowledge_base.py
├── logging_config.py
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── knowledge_base.json
│
├── tests/
│   ├── test_api.py
│   ├── test_graph.py
│   └── test_knowledge_base.py
│
├── logs/
│   └── app.log
│
└── outputs/
    ├── communication_log.json
    └── README.txt
```

## Technologies Used

- Python – Core programming language.
- LangGraph – Multi-agent workflow orchestration.
- FastAPI – REST API development.
- Pydantic – Request validation and response models.
- Pytest – Automated testing.
- Python Logging – Application monitoring and debugging.
- Python-dotenv – Environment variable management.
- Docker – Containerization and deployment.

## Installation and Setup

### 1. Clone or open the project

Navigate to the project directory:

```powershell
cd "Day 24"
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Example configuration:

```env
APP_NAME=ShopEase Customer Support API
APP_ENV=development
LOG_LEVEL=INFO
HOST=127.0.0.1
PORT=8000
```

The `.env` file contains local configuration and should not be committed to version control.

## Running the Application

### Command-Line Interface

```powershell
python main.py
```

### REST API

```powershell
python api.py
```

Once the API starts, access:

- API documentation: http://127.0.0.1:8000/docs
- Home endpoint: http://127.0.0.1:8000/
- Health endpoint: http://127.0.0.1:8000/health
- Readiness endpoint: http://127.0.0.1:8000/ready

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Displays the application welcome message. |
| GET | `/health` | Checks whether the API is running. |
| GET | `/ready` | Checks whether the knowledge base is available. |
| POST | `/chat` | Processes a customer-support query. |

### Example Chat Request

```json
{
  "query": "I have received a damaged item"
}
```

### Example Response

```json
{
  "answer": "Here is the guidance available for your question...",
  "status": "completed",
  "revision_count": 0
}
```

## Testing

The project uses Pytest for automated testing.

Run all tests:

```powershell
python -m pytest -v
```

Run individual test files:

```powershell
pytest tests/test_graph.py -v
pytest tests/test_knowledge_base.py -v
pytest tests/test_api.py -v
```

The test suite covers workflow behaviour, knowledge-base loading and searching, API endpoints, input validation, and error handling.

## Logging

The application uses Python's built-in logging module.

Logs are:
- Displayed in the terminal.
- Stored in `logs/app.log`.
- Configurable through the `LOG_LEVEL` environment variable.

Supported logging levels include DEBUG, INFO, WARNING, ERROR, and CRITICAL.

## Docker Deployment

### 1. Build the Docker image

```powershell
docker build -t shopease-api .
```

### 2. Run the container

```powershell
docker run -d --name shopease-container --env-file .env -e HOST=0.0.0.0 -e APP_ENV=production -p 8000:8000 shopease-api
```

### 3. Check the running container

```powershell
docker ps
```

### 4. View container logs

```powershell
docker logs shopease-container
```

### 5. Stop the container

```powershell
docker stop shopease-container
```

### 6. Remove the container

```powershell
docker rm shopease-container
```

## Monitoring

The application provides two monitoring endpoints:

- **Liveness (`/health`):** Confirms that the API process is responding.
- **Readiness (`/ready`):** Attempts to load the knowledge base and verifies that articles are available.

The readiness endpoint returns HTTP 503 if the knowledge base cannot be loaded or contains no articles.

## Production Readiness

The project includes automated tests, structured logging, environment-based configuration, API input validation, health checks, and Docker deployment support.

These features improve maintainability and deployment readiness. Additional production measures, such as authentication, HTTPS, centralized monitoring, metrics collection, and automated deployment pipelines, can be considered for future improvements.

## Future Improvements

- Add authentication and authorization.
- Introduce centralized log management.
- Add API performance metrics and alerting.
- Implement automated CI/CD pipelines.
- Deploy the application to a cloud platform.
