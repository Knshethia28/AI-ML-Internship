
"""LangGraph orchestration for the five ShopEase agents."""
from __future__ import annotations

import logging
import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph

from agents import (
    AnalyzerAgent, CriticAgent, ResearchAgent, SharedState, WriterAgent
)

from logging_config import get_logger

logger = get_logger(__name__)


class AgentGraphState(TypedDict):
    user_query: str
    research_results: list[dict[str, Any]]
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
    """Build the legacy agent state from the LangGraph shared state."""
    return SharedState(
        user_query=state["user_query"],
        research_results=state.get("research_results", []),
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
    logger.info("Coordinator initialized the workflow")

    return {
        "status": "running",
        "error": "",
        "revision_count": 0,
        "revision_note": "",
        "trace": _event(
            "Coordinator",
            "start",
            "Accepted the request and initialized the LangGraph workflow."
        ),
    }


def research_node(state: AgentGraphState):
    logger.info("Research Agent execution started")

    try:
        agent_state = _agent_state(state)
        results = ResearchAgent().run(agent_state)

        logger.info("Research Agent execution completed")

        return {
            "research_results": results,
            "trace": agent_state.trace
        }

    except Exception as exc:
        logger.exception("Research Agent execution failed")

        return {
            "error": f"Research Agent failed: {type(exc).__name__}: {exc}",
            "status": "failed",
            "trace": _event(
                "Research Agent",
                "error",
                f"{type(exc).__name__}: {exc}"
            ),
        }


def analyzer_node(state: AgentGraphState):
    logger.info("Analyzer Agent execution started")

    try:
        agent_state = _agent_state(state)
        analysis = AnalyzerAgent().run(agent_state)

        logger.info("Analyzer Agent execution completed")

        return {
            "analysis": analysis,
            "trace": agent_state.trace
        }

    except Exception as exc:
        logger.exception("Analyzer Agent execution failed")

        return {
            "error": f"Analyzer failed: {type(exc).__name__}: {exc}",
            "status": "failed",
            "trace": _event(
                "Analyzer",
                "error",
                f"{type(exc).__name__}: {exc}"
            ),
        }


def writer_node(state: AgentGraphState):
    revision_count = state.get("revision_count", 0)

    if revision_count > 0:
        logger.info(
            "Writer Agent started revision %s",
            revision_count
        )
    else:
        logger.info("Writer Agent execution started")

    try:
        agent_state = _agent_state(state)
        draft = WriterAgent().run(
            agent_state,
            revision_note=state.get("revision_note", "")
        )

        logger.info("Writer Agent execution completed")

        return {
            "draft": draft,
            "trace": agent_state.trace
        }

    except Exception as exc:
        logger.exception("Writer Agent execution failed")

        return {
            "error": f"Writer failed: {type(exc).__name__}: {exc}",
            "status": "failed",
            "trace": _event(
                "Writer",
                "error",
                f"{type(exc).__name__}: {exc}"
            ),
        }


def critic_node(state: AgentGraphState):
    logger.info("Critic Agent execution started")

    try:
        agent_state = _agent_state(state)
        critique = CriticAgent().run(agent_state)

        logger.info(
            "Critic Agent completed evaluation. Approved: %s",
            critique.get("approved", False)
        )

        return {
            "critique": critique,
            "trace": agent_state.trace
        }

    except Exception as exc:
        logger.exception("Critic Agent execution failed")

        return {
            "error": f"Critic failed: {type(exc).__name__}: {exc}",
            "status": "failed",
            "trace": _event(
                "Critic",
                "error",
                f"{type(exc).__name__}: {exc}"
            ),
        }


def route_after_node(state: AgentGraphState):
    if state.get("error") or state.get("status") == "failed":
        logger.warning("Workflow routing to finalization after an agent failure")
        return "finalize"

    return "continue"


def route_after_critic(state: AgentGraphState):
    if state.get("error") or state.get("status") == "failed":
        logger.warning("Critic failed. Routing workflow to finalization")
        return "finalize"

    if state.get("critique", {}).get("approved"):
        logger.info("Critic approved the response")
        return "finalize"

    if state.get("revision_count", 0) < state.get("max_revisions", 1):
        logger.info("Critic requested a revision")
        return "revise"

    logger.warning("Maximum revision limit reached")
    return "finalize"


def revision_node(state: AgentGraphState):
    issues = state.get("critique", {}).get("issues", [])
    next_revision = state.get("revision_count", 0) + 1

    logger.info(
        "Coordinator initiating revision %s",
        next_revision
    )

    return {
        "revision_count": next_revision,
        "revision_note": "; ".join(issues),
        "trace": _event(
            "Coordinator",
            "revise",
            f"Routing back to Writer for revision {next_revision}: {'; '.join(issues)}"
        ),
    }


def finalize_node(state: AgentGraphState):
    if state.get("error") or state.get("status") == "failed":
        answer = (
            "Sorry, the ShopEase support workflow could not complete this request because an internal agent "
            "encountered an error. Please contact ShopEase customer support and provide your order number."
        )
        status = "failed"

        logger.error("ShopEase workflow finalized with failure")

    else:
        answer = state.get("draft", "")
        approved = state.get("critique", {}).get("approved", False)
        status = "completed" if approved else "completed_with_review_warning"

        if approved:
            logger.info("ShopEase workflow finalized successfully")
        else:
            logger.warning(
                "ShopEase workflow finalized without critic approval"
            )

    return {
        "final_answer": answer,
        "status": status,
        "trace": _event(
            "Coordinator",
            "finish",
            f"Workflow ended with status={status}."
        ),
    }


def build_graph():
    builder = StateGraph(AgentGraphState)

    builder.add_node("coordinator", coordinator_node)
    builder.add_node("research", research_node)
    builder.add_node("analyzer", analyzer_node)
    builder.add_node("writer", writer_node)
    builder.add_node("critic", critic_node)
    builder.add_node("revision", revision_node)
    builder.add_node("finalize", finalize_node)

    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "research")

    builder.add_conditional_edges(
        "research",
        route_after_node,
        {
            "continue": "analyzer",
            "finalize": "finalize"
        }
    )

    builder.add_conditional_edges(
        "analyzer",
        route_after_node,
        {
            "continue": "writer",
            "finalize": "finalize"
        }
    )

    builder.add_conditional_edges(
        "writer",
        route_after_node,
        {
            "continue": "critic",
            "finalize": "finalize"
        }
    )

    builder.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "revise": "revision",
            "finalize": "finalize"
        }
    )

    builder.add_edge("revision", "writer")
    builder.add_edge("finalize", END)

    return builder.compile()


def run_workflow(query: str, max_revisions: int = 1):
    if not query.strip():
        raise ValueError("The user query cannot be empty.")

    if max_revisions < 0:
        raise ValueError("max_revisions cannot be negative.")

    logger.info("Starting ShopEase LangGraph workflow")

    initial_state: AgentGraphState = {
        "user_query": query.strip(),
        "research_results": [],
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

    try:
        result = build_graph().invoke(initial_state)

        logger.info(
            "Workflow execution finished with status: %s",
            result.get("status", "unknown")
        )

        return {
            "query": result["user_query"],
            "answer": result.get("final_answer", ""),
            "status": result.get("status", "unknown"),
            "research_results": result.get("research_results", []),
            "analysis": result.get("analysis", {}),
            "critique": result.get("critique", {}),
            "revision_count": result.get("revision_count", 0),
            "error": result.get("error", ""),
            "trace": result.get("trace", []),
        }

    except Exception:
        logger.exception("Unexpected error during LangGraph execution")
        raise
