"""Day 22 agent logic, reused without changing its responsibilities."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from knowledge_base import load_articles, search_articles


@dataclass
class SharedState:
    """Compatibility state used by the original Day 22 agents."""
    user_query: str
    research_results: list[dict[str, Any]] = field(default_factory=list)
    analysis: dict[str, Any] = field(default_factory=dict)
    draft: str = ""
    critique: dict[str, Any] = field(default_factory=dict)
    final_answer: str = ""
    trace: list[dict[str, Any]] = field(default_factory=list)
    revision_count: int = 0
    status: str = "initialized"

    def record(self, agent: str, action: str, details: str) -> None:
        self.trace.append({"agent": agent, "action": action, "details": details})


class ResearchAgent:
    name = "Research Agent"

    def __init__(self, articles=None):
        self.articles = articles if articles is not None else load_articles()

    def run(self, state: SharedState):
        results = search_articles(state.user_query, self.articles)
        state.research_results = results
        state.record(self.name, "retrieve", f"Retrieved {len(results)} matching local article(s).")
        return results


class AnalyzerAgent:
    name = "Analyzer"

    def run(self, state: SharedState):
        if not state.research_results:
            analysis = {
                "summary": "No matching article was found in the local knowledge base.",
                "key_points": [], "sources": [], "confidence": "low",
                "needs_human_help": True,
            }
        else:
            points = [article.get("content", "") for article in state.research_results]
            analysis = {
                "summary": " ".join(points),
                "key_points": points,
                "sources": [article.get("title", "Untitled article") for article in state.research_results],
                "confidence": "medium" if len(points) == 1 else "high",
                "needs_human_help": False,
            }
        state.analysis = analysis
        state.record(self.name, "analyze",
                     f"Prepared {len(analysis['key_points'])} key point(s); confidence={analysis['confidence']}.")
        return analysis


class WriterAgent:
    name = "Writer"

    def run(self, state: SharedState, revision_note: str = ""):
        analysis = state.analysis
        if analysis.get("needs_human_help"):
            draft = (
                "I couldn't find a matching answer in the available ShopEase help articles. "
                "Please contact ShopEase customer support with your order number so a team member can check the case."
            )
        else:
            bullets = "\n".join(f"- {point}" for point in analysis.get("key_points", []))
            sources = ", ".join(analysis.get("sources", []))
            draft = (
                "Here is the guidance available for your question:\n\n"
                f"{bullets}\n\n"
                f"Reference article(s): {sources}.\n"
                "If these steps do not resolve the issue, contact ShopEase customer support and include your order number."
            )
        if revision_note:
            draft += f"\n\nRevision note addressed: {revision_note}"
        state.draft = draft
        state.record(self.name, "draft", "Created a response grounded in Analyzer output.")
        return draft


class CriticAgent:
    name = "Critic"

    def run(self, state: SharedState):
        issues = []
        draft = state.draft.strip()
        if not draft:
            issues.append("Draft is empty.")
        if state.research_results and "Reference article(s):" not in draft:
            issues.append("Add the source article names to the response.")
        if state.analysis.get("needs_human_help") and "customer support" not in draft.lower():
            issues.append("Escalate the unsupported query to customer support.")
        result = {"approved": not issues, "issues": issues}
        state.critique = result
        state.record(self.name, "review",
                     "Approved draft." if result["approved"] else f"Requested {len(issues)} revision(s).")
        return result


class CoordinatorAgent:
    """Kept for compatibility with the original Day 22 project; Day 23 uses graph.py."""
    name = "Coordinator"

    def __init__(self, max_revisions: int = 1):
        self.max_revisions = max_revisions
        self.researcher = ResearchAgent()
        self.analyzer = AnalyzerAgent()
        self.writer = WriterAgent()
        self.critic = CriticAgent()

    def run(self, query: str):
        state = SharedState(user_query=query.strip())
        state.record(self.name, "start", "Created shared state and accepted the user query.")
        self.researcher.run(state)
        self.analyzer.run(state)
        revision_note = ""
        while True:
            self.writer.run(state, revision_note)
            critique = self.critic.run(state)
            if critique["approved"] or state.revision_count >= self.max_revisions:
                break
            state.revision_count += 1
            revision_note = "; ".join(critique["issues"])
            state.record(self.name, "revise", f"Starting revision {state.revision_count}.")
        state.final_answer = state.draft
        state.status = "completed" if critique["approved"] else "completed_with_review_warning"
        state.record(self.name, "finish", f"Workflow ended with status={state.status}.")
        return {
            "query": state.user_query, "answer": state.final_answer, "status": state.status,
            "research_results": state.research_results, "analysis": state.analysis,
            "critique": state.critique, "revision_count": state.revision_count,
            "trace": state.trace,
        }
