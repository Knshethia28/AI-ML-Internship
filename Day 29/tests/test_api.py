
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



def test_chat_returns_session_and_metadata():
    fake_result = {
        "status": "completed",
        "answer": "Here is the answer.",
        "revision_count": 0,
        "analysis": {
            "category": "Orders",
            "sources": ["Late or delayed orders"],
            "needs_human_help": False,
        },
        "product_results": [],
    }
    with patch("api.run_workflow", return_value=fake_result):
        response = client.post("/chat", json={"query": "My order is late"})

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"]
    assert data["category"] == "Orders"
    assert data["sources"] == ["Late or delayed orders"]


def test_chat_passes_session_history_to_workflow():
    session_id = "context-test-session"
    fake_result = {
        "status": "completed",
        "answer": "Here are the results.",
        "revision_count": 0,
        "analysis": {"category": "Products", "sources": [], "needs_human_help": False},
        "product_results": [],
    }
    with patch("api.run_workflow", return_value=fake_result) as workflow:
        first = client.post("/chat", json={"query": "Show me laptops", "session_id": session_id})
        second = client.post("/chat", json={"query": "What about a cheaper one?", "session_id": session_id})

    assert first.status_code == 200
    assert second.status_code == 200
    history = workflow.call_args_list[1].kwargs["conversation_history"]
    assert workflow.call_args_list[1].args[0] == "What about a cheaper one?"
    assert history[0] == {"role": "user", "content": "Show me laptops"}
    assert history[-1]["role"] == "assistant"


def test_support_request_validates_and_records_ticket():
    with patch(
        "api.create_escalation",
        return_value={
            "ticket_id": "SE-TEST1234",
            "status": "Pending",
            "created_at": "2026-11-06T00:00:00+00:00",
        },
    ):
        response = client.post(
            "/support",
            json={"query": "My parcel has not arrived", "email": "test@example.com"},
        )
    assert response.status_code == 200
    assert response.json()["ticket_id"] == "SE-TEST1234"


def test_support_request_rejects_invalid_email():
    response = client.post(
        "/support",
        json={"query": "My parcel has not arrived", "email": "not-an-email"},
    )
    assert response.status_code == 422



def test_customer_interface_is_served():
    response = client.get("/app")
    assert response.status_code == 200
    assert "ShopEase Assistant" in response.text


def test_frontend_assets_are_served():
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert ".app-shell" in response.text



def test_session_history_endpoint_returns_saved_messages():
    session_id = "history-read-test"
    with patch("api.run_workflow", return_value={
        "status": "completed",
        "answer": "Please check your order details.",
        "revision_count": 0,
        "analysis": {"category": "Orders", "sources": [], "needs_human_help": False},
        "product_results": [],
    }):
        client.post("/chat", json={"query": "My order is late", "session_id": session_id})
    response = client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    assert response.json()["messages"][0]["content"] == "My order is late"
    assert response.json()["messages"][1]["role"] == "assistant"


def test_product_follow_up_conversation_flow_and_session_isolation():
    session_a = "session-product-flow-a"
    session_b = "session-product-flow-b"

    mock_products = [
        {
            "id": 121,
            "title": "iPhone 5s",
            "description": "An Apple smartphone with Retina display and Touch ID.",
            "price": 199.99,
            "rating": 4.15,
            "stock": 40,
            "category": "smartphones",
            "thumbnail": "https://example.com/5s.jpg",
            "brand": "Apple",
        },
        {
            "id": 124,
            "title": "iPhone X",
            "description": "Apple flagship with Super Retina OLED screen.",
            "price": 899.99,
            "rating": 4.44,
            "stock": 25,
            "category": "smartphones",
            "thumbnail": "https://example.com/x.jpg",
            "brand": "Apple",
        },
    ]

    def mock_search(query, limit=6):
        if "phones" in query.lower() or "smartphone" in query.lower():
            return mock_products
        return []

    with patch("agents.search_products", side_effect=mock_search):
        # 1. User asks to display products in Session A
        r1 = client.post("/chat", json={"query": "Show me some phones.", "session_id": session_a})
        assert r1.status_code == 200
        assert "iPhone 5s" in r1.json()["answer"]

        # 2. Follow-up: price of the first one
        r2 = client.post("/chat", json={"query": "What is the price of the first one?", "session_id": session_a})
        assert r2.status_code == 200
        data2 = r2.json()
        assert "$199.99" in data2["answer"]
        assert "iPhone 5s" in data2["answer"]
        assert not data2["needs_human_help"]

        # 3. Follow-up: rating of that phone using pronoun "its"
        r3 = client.post("/chat", json={"query": "What is its rating?", "session_id": session_a})
        assert r3.status_code == 200
        data3 = r3.json()
        assert "4.15" in data3["answer"]
        assert "iPhone 5s" in data3["answer"]
        assert not data3["needs_human_help"]

        # 4. Follow-up: tell me more about that phone
        r4 = client.post("/chat", json={"query": "Tell me more about that phone.", "session_id": session_a})
        assert r4.status_code == 200
        data4 = r4.json()
        assert "Retina display" in data4["answer"]
        assert "$199.99" in data4["answer"]
        assert not data4["needs_human_help"]

        # 5. Follow-up: what about its category
        r5 = client.post("/chat", json={"query": "What about its category?", "session_id": session_a})
        assert r5.status_code == 200
        data5 = r5.json()
        assert "smartphones" in data5["answer"]
        assert not data5["needs_human_help"]

        # 6. Support-policy query in the same session routes to knowledge base
        r6 = client.post("/chat", json={"query": "How do I return a damaged item?", "session_id": session_a})
        assert r6.status_code == 200
        data6 = r6.json()
        assert "Returns and refunds" in data6["answer"]
        assert "return" in data6["answer"].lower()
        assert not data6["needs_human_help"]

        # 7. Session Isolation: Session B with no products should not leak Session A's context
        r_iso = client.post("/chat", json={"query": "What is the price of the first one?", "session_id": session_b})
        assert r_iso.status_code == 200
        data_iso = r_iso.json()
        # Session B has no product context, so it must trigger human support fallback
        assert data_iso["needs_human_help"] is True
        assert "customer support" in data_iso["answer"].lower()
        assert "iPhone 5s" not in data_iso["answer"]
