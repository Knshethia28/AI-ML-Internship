"""LangGraph orchestration for the ShopEase multi-agent support workflow."""
from __future__ import annotations

import logging
import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph

from agents import AnalyzerAgent, CriticAgent, ResearchAgent, SharedState, WriterAgent
from conversation import contextualize_query

logger = logging.getLogger(__name__)


class AgentGraphState(TypedDict):
    user_query: str
    contextual_query: str
    conversation_history: list[dict[str, Any]]
    product_context: list[dict[str, Any]]
    active_product: dict[str, Any] | None
    product_follow_up: dict[str, Any] | None
    research_results: list[dict[str, Any]]
    product_results: list[dict[str, Any]]
    analysis: dict[str, Any]
    draft: str
    critique: dict[str, Any]
    final_answer: str
    revision_count: int
    max_revisions: int
    revision_note: str
    status: str
    error: str
    trace: Annotated[list[dict[str, Any]], operator.add]


def _agent_state(state: AgentGraphState) -> SharedState:
    return SharedState(
        user_query=state["user_query"],
        contextual_query=state.get("contextual_query", state["user_query"]),
        conversation_history=state.get("conversation_history", []),
        product_context=state.get("product_context", []),
        active_product=state.get("active_product"),
        product_follow_up=state.get("product_follow_up"),
        research_results=state.get("research_results", []),
        product_results=state.get("product_results", []),
        analysis=state.get("analysis", {}),
        draft=state.get("draft", ""),
        critique=state.get("critique", {}),
        final_answer=state.get("final_answer", ""),
        revision_count=state.get("revision_count", 0),
        status=state.get("status", "running"),
    )


def _event(agent: str, action: str, details: str):
    return [{"agent": agent, "action": action, "details": details}]


def coordinator_node(state: AgentGraphState):
    history = state.get("conversation_history", [])
    resolved = contextualize_query(state["user_query"], history)

    # Recover product_context from previous turns in history if not already present
    product_context = list(state.get("product_context") or [])
    active_product = state.get("active_product")
    if not product_context and history:
        for item in reversed(history):
            if item.get("role") == "assistant" and item.get("products"):
                product_context = list(item["products"])
                break

    logger.info("Coordinator initialized the workflow")
    return {
        "contextual_query": resolved,
        "product_context": product_context,
        "active_product": active_product,
        "status": "running",
        "error": "",
        "revision_count": 0,
        "revision_note": "",
        "trace": _event(
            "Coordinator", "start",
            "Accepted the request and resolved available conversation context."
        ),
    }


def research_node(state: AgentGraphState):
    logger.info("Research Agent execution started")
    try:
        agent_state = _agent_state(state)
        ResearchAgent().run(agent_state)
        return {
            "research_results": agent_state.research_results,
            "product_results": agent_state.product_results,
            "product_context": agent_state.product_context,
            "active_product": agent_state.active_product,
            "product_follow_up": agent_state.product_follow_up,
            "trace": agent_state.trace,
        }
    except Exception as exc:
        logger.exception("Research Agent execution failed")
        return {
            "error": f"Research Agent failed: {type(exc).__name__}: {exc}",
            "status": "failed",
            "trace": _event("Research Agent", "error", f"{type(exc).__name__}: {exc}"),
        }


def analyzer_node(state: AgentGraphState):
    try:
        agent_state = _agent_state(state)
        AnalyzerAgent().run(agent_state)
        return {"analysis": agent_state.analysis, "trace": agent_state.trace}
    except Exception as exc:
        logger.exception("Analyzer Agent execution failed")
        return {
            "error": f"Analyzer failed: {type(exc).__name__}: {exc}",
            "status": "failed",
            "trace": _event("Analyzer", "error", f"{type(exc).__name__}: {exc}"),
        }


def writer_node(state: AgentGraphState):
    try:
        agent_state = _agent_state(state)
        WriterAgent().run(agent_state, revision_note=state.get("revision_note", ""))
        return {"draft": agent_state.draft, "trace": agent_state.trace}
    except Exception as exc:
        logger.exception("Writer Agent execution failed")
        return {
            "error": f"Writer failed: {type(exc).__name__}: {exc}",
            "status": "failed",
            "trace": _event("Writer", "error", f"{type(exc).__name__}: {exc}"),
        }


def critic_node(state: AgentGraphState):
    try:
        agent_state = _agent_state(state)
        CriticAgent().run(agent_state)
        return {"critique": agent_state.critique, "trace": agent_state.trace}
    except Exception as exc:
        logger.exception("Critic Agent execution failed")
        return {
            "error": f"Critic failed: {type(exc).__name__}: {exc}",
            "status": "failed",
            "trace": _event("Critic", "error", f"{type(exc).__name__}: {exc}"),
        }


def route_after_node(state: AgentGraphState):
    return "finalize" if state.get("error") or state.get("status") == "failed" else "continue"


def route_after_critic(state: AgentGraphState):
    if state.get("error") or state.get("status") == "failed":
        return "finalize"
    if state.get("critique", {}).get("approved"):
        return "finalize"
    if state.get("revision_count", 0) < state.get("max_revisions", 1):
        return "revise"
    return "finalize"


def revision_node(state: AgentGraphState):
    issues = state.get("critique", {}).get("issues", [])
    next_revision = state.get("revision_count", 0) + 1
    return {
        "revision_count": next_revision,
        "revision_note": "; ".join(issues),
        "trace": _event(
            "Coordinator", "revise",
            f"Routing back to Writer for revision {next_revision}: {'; '.join(issues)}"
        ),
    }


def finalize_node(state: AgentGraphState):
    if state.get("error") or state.get("status") == "failed":
        answer = (
            "Sorry, the ShopEase support workflow could not complete this request because "
            "an internal agent encountered an error. Please contact ShopEase customer support or request human support."
        )
        status = "failed"
    else:
        answer = state.get("draft", "")
        status = (
            "completed"
            if state.get("critique", {}).get("approved")
            else "completed_with_review_warning"
        )
    return {
        "final_answer": answer,
        "status": status,
        "trace": _event("Coordinator", "finish", f"Workflow ended with status={status}."),
    }


def build_graph():
    builder = StateGraph(AgentGraphState)
    for name, node in (
        ("coordinator", coordinator_node),
        ("research", research_node),
        ("analyzer", analyzer_node),
        ("writer", writer_node),
        ("critic", critic_node),
        ("revision", revision_node),
        ("finalize", finalize_node),
    ):
        builder.add_node(name, node)

    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "research")
    builder.add_conditional_edges("research", route_after_node, {"continue": "analyzer", "finalize": "finalize"})
    builder.add_conditional_edges("analyzer", route_after_node, {"continue": "writer", "finalize": "finalize"})
    builder.add_conditional_edges("writer", route_after_node, {"continue": "critic", "finalize": "finalize"})
    builder.add_conditional_edges("critic", route_after_critic, {"revise": "revision", "finalize": "finalize"})
    builder.add_edge("revision", "writer")
    builder.add_edge("finalize", END)
    return builder.compile()


def run_workflow(
    query: str,
    max_revisions: int = 1,
    conversation_history: list[dict[str, Any]] | None = None,
    product_context: list[dict[str, Any]] | None = None,
    active_product: dict[str, Any] | None = None,
):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("The user query cannot be empty.")
    if max_revisions < 0:
        raise ValueError("max_revisions cannot be negative.")

    # Recover product_context from history if not supplied explicitly
    if not product_context and conversation_history:
        for item in reversed(conversation_history):
            if item.get("role") == "assistant" and item.get("products"):
                product_context = list(item["products"])
                break

    initial_state: AgentGraphState = {
        "user_query": query.strip(),
        "contextual_query": query.strip(),
        "conversation_history": conversation_history or [],
        "product_context": product_context or [],
        "active_product": active_product,
        "product_follow_up": None,
        "research_results": [],
        "product_results": [],
        "analysis": {},
        "draft": "",
        "critique": {},
        "final_answer": "",
        "revision_count": 0,
        "max_revisions": max_revisions,
        "revision_note": "",
        "status": "initialized",
        "error": "",
        "trace": [],
    }
    result = build_graph().invoke(initial_state)
    return {
        "query": result["user_query"],
        "contextual_query": result.get("contextual_query", query),
        "answer": result.get("final_answer", ""),
        "status": result.get("status", "unknown"),
        "research_results": result.get("research_results", []),
        "product_results": result.get("product_results", []),
        "product_context": result.get("product_context", []),
        "active_product": result.get("active_product"),
        "product_follow_up": result.get("product_follow_up"),
        "analysis": result.get("analysis", {}),
        "critique": result.get("critique", {}),
        "revision_count": result.get("revision_count", 0),
        "error": result.get("error", ""),
        "trace": result.get("trace", []),
    }
