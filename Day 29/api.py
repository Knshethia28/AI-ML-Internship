"""FastAPI application for the ShopEase customer-support demo."""
from __future__ import annotations

import os
import re
import threading
import uuid
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from escalations import create_escalation
from graph import run_workflow
from knowledge_base import load_articles
from logging_config import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

APP_NAME = os.getenv("APP_NAME", "ShopEase Customer Support")
APP_ENV = os.getenv("APP_ENV", "development")
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title=APP_NAME,
    description="ShopEase customer support with LangGraph, support articles, product lookup and session context.",
    version="2.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# In-memory sessions are intentionally lightweight for a single-process demo.
# They reset when the server restarts; escalation tickets are persisted to JSON.
_SESSIONS: dict[str, list[dict[str, str]]] = {}
_SESSION_LOCK = threading.Lock()
MAX_HISTORY_MESSAGES = 12
MAX_SESSIONS = 500


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    session_id: str | None = Field(default=None, max_length=80)

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str):
        if not value.strip():
            raise ValueError("Query cannot be empty or contain only whitespace.")
        return value.strip()


class ChatResponse(BaseModel):
    answer: str
    status: str
    revision_count: int
    session_id: str
    category: str
    sources: list[str]
    products: list[dict]
    needs_human_help: bool


class EscalationRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=2000)
    name: str = Field(default="", max_length=100)
    email: str = Field(default="", max_length=254)
    session_id: str = Field(default="", max_length=80)

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str):
        if not value.strip():
            raise ValueError("Please describe the issue.")
        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        value = value.strip()
        if value and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Enter a valid email address or leave the field blank.")
        return value


@app.get("/")
def home():
    return {"message": f"Welcome to {APP_NAME}", "status": "running", "interface": "/app"}


@app.get("/app", include_in_schema=False)
def customer_interface():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": APP_NAME, "environment": APP_ENV}


@app.get("/ready")
def readiness_check():
    try:
        articles = load_articles()
        if not articles:
            raise ValueError("Knowledge base contains no articles.")
        return {"status": "ready", "knowledge_base": "available", "article_count": len(articles)}
    except Exception:
        logger.exception("Readiness check failed")
        raise HTTPException(
            status_code=503,
            detail="Service is not ready. Knowledge base is unavailable."
        )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or uuid.uuid4().hex
    with _SESSION_LOCK:
        session_data = _SESSIONS.get(session_id)
        if isinstance(session_data, dict):
            history = list(session_data.get("messages", []))
            product_context = list(session_data.get("products", []))
            active_product = session_data.get("active_product")
        elif isinstance(session_data, list):
            history = list(session_data)
            product_context = []
            active_product = None
        else:
            history = []
            product_context = []
            active_product = None

    try:
        result = run_workflow(
            request.query,
            conversation_history=history,
            product_context=product_context,
            active_product=active_product,
        )
        if result["status"] not in {"completed", "completed_with_review_warning"}:
            raise HTTPException(status_code=500, detail="Unable to process the customer query.")

        answer = result["answer"]
        new_products = result.get("product_results", [])
        is_follow_up = bool(result.get("product_follow_up"))

        # Preserve product context: if this turn was a follow-up, retain previous product_context
        # so subsequent follow-ups can continue querying the catalogue set.
        if is_follow_up:
            preserved_products = product_context or new_products
        else:
            preserved_products = new_products if new_products else product_context

        updated_active = result.get("active_product") or active_product

        new_history = history + [
            {"role": "user", "content": request.query},
            {"role": "assistant", "content": answer, "products": new_products},
        ]
        with _SESSION_LOCK:
            if session_id not in _SESSIONS and len(_SESSIONS) >= MAX_SESSIONS:
                oldest = next(iter(_SESSIONS))
                _SESSIONS.pop(oldest, None)
            _SESSIONS[session_id] = {
                "messages": new_history[-MAX_HISTORY_MESSAGES:],
                "products": preserved_products,
                "active_product": updated_active,
            }

        analysis = result.get("analysis", {})
        return ChatResponse(
            answer=answer,
            status=result["status"],
            revision_count=result.get("revision_count", 0),
            session_id=session_id,
            category=analysis.get("category", "General enquiry"),
            sources=analysis.get("sources", []),
            products=new_products,
            needs_human_help=bool(analysis.get("needs_human_help", False)),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error while processing customer request")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@app.post("/support")
def request_human_support(request: EscalationRequest):
    try:
        ticket = create_escalation(
            name=request.name,
            email=request.email,
            query=request.query,
            session_id=request.session_id,
        )
        return {
            "message": "Your support request has been recorded.",
            "ticket_id": ticket["ticket_id"],
            "status": ticket["status"],
            "created_at": ticket["created_at"],
        }
    except Exception:
        logger.exception("Could not save support escalation")
        raise HTTPException(status_code=500, detail="Could not save the support request. Please try again.")


@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    with _SESSION_LOCK:
        session_data = _SESSIONS.get(session_id)
        if isinstance(session_data, dict):
            messages = list(session_data.get("messages", []))
        elif isinstance(session_data, list):
            messages = list(session_data)
        else:
            messages = []
    return {"session_id": session_id, "messages": messages}


@app.delete("/sessions/{session_id}")
def clear_session(session_id: str):
    with _SESSION_LOCK:
        existed = _SESSIONS.pop(session_id, None) is not None
    return {"cleared": existed}


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=APP_ENV.lower() == "development",
    )
