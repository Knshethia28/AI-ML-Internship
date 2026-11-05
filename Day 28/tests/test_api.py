
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from api import app

client = TestClient(app)


# ---------------- BASIC ENDPOINT TESTS ----------------

def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ---------------- CHAT API TESTS ----------------

def test_chat_successful_response():
    response = client.post(
        "/chat",
        json={"query": "My order delivery is late"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "completed"
    assert data["revision_count"] >= 0
    assert "answer" in data
    assert len(data["answer"]) > 0


@pytest.mark.parametrize(
    "query",
    [
        "",
        "   ",
        "a" * 1001
    ]
)
def test_chat_invalid_queries(query):
    response = client.post(
        "/chat",
        json={"query": query}
    )

    assert response.status_code == 422


def test_chat_missing_query():
    response = client.post(
        "/chat",
        json={}
    )

    assert response.status_code == 422


def test_chat_workflow_failure():
    with patch(
        "api.run_workflow",
        side_effect=RuntimeError("Simulated workflow failure")
    ):
        response = client.post(
            "/chat",
            json={"query": "My order is late"}
        )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "An unexpected error occurred."
    )


def test_chat_workflow_failed_status():
    with patch(
        "api.run_workflow",
        return_value={
            "status": "failed",
            "answer": "Unable to process",
            "revision_count": 0
        }
    ):
        response = client.post(
            "/chat",
            json={"query": "My order is late"}
        )

    assert response.status_code == 500


def test_chat_empty_query_from_workflow():
    with patch(
        "api.run_workflow",
        side_effect=ValueError("Query cannot be empty")
    ):
        response = client.post(
            "/chat",
            json={"query": "My order is late"}
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Query cannot be empty"
