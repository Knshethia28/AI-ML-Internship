"""Agent responsibilities for the ShopEase customer-support workflow."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from conversation import (
    detect_product_attribute,
    is_product_follow_up,
    resolve_product_reference,
)
from knowledge_base import load_articles, search_articles
from product_catalog import search_products


@dataclass
class SharedState:
    """State shared between the agents during one customer request."""
    user_query: str
    contextual_query: str = ""
    conversation_history: list[dict[str, Any]] = field(default_factory=list)
    product_context: list[dict[str, Any]] = field(default_factory=list)
    active_product: dict[str, Any] | None = None
    product_follow_up: dict[str, Any] | None = None
    research_results: list[dict[str, Any]] = field(default_factory=list)
    product_results: list[dict[str, Any]] = field(default_factory=list)
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
        query = state.contextual_query or state.user_query

        # Check if the query is a follow-up inquiry referencing previously retrieved products
        if is_product_follow_up(state.user_query, state.product_context):
            product = resolve_product_reference(state.user_query, state.product_context, state.active_product)
            attribute = detect_product_attribute(state.user_query)
            if product:
                state.active_product = product
                state.product_follow_up = {"product": product, "attribute": attribute}
                state.product_results = [product]
                state.record(
                    self.name,
                    "resolve_context",
                    f"Resolved follow-up reference to '{product.get('title')}' for attribute '{attribute}' from stored product context."
                )
            else:
                state.product_results = []
            # Product follow-ups only search articles if the query also touches support policies
            articles = search_articles(query, self.articles) if any(
                w in state.user_query.casefold() for w in ("return", "refund", "cancel", "ship", "delivery", "track", "order")
            ) else []
        else:
            articles = search_articles(query, self.articles)
            products = search_products(query)
            state.product_results = products
            if products:
                state.active_product = products[0]
                state.product_context = products

        state.research_results = articles
        state.record(
            self.name,
            "retrieve",
            f"Retrieved {len(articles)} local support article(s) and "
            f"{len(state.product_results)} product(s) from the demonstration catalogue."
        )
        return articles


class AnalyzerAgent:
    name = "Analyzer"

    def run(self, state: SharedState):
        points = [article.get("content", "") for article in state.research_results]
        sources = [article.get("title", "Untitled article") for article in state.research_results]
        has_follow_up = bool(state.product_follow_up and state.product_follow_up.get("product"))
        needs_help = not points and not state.product_results and not has_follow_up

        if needs_help:
            summary = "No relevant support article or product result was found."
            confidence = "low"
            category = _category(state.contextual_query or state.user_query)
        elif has_follow_up:
            prod = state.product_follow_up["product"]
            attr = state.product_follow_up.get("attribute", "details")
            summary = f"Product context resolved for {prod.get('title')} regarding {attr}."
            confidence = "high"
            category = "Products"
        elif state.product_results:
            summary = f"Found {len(state.product_results)} matching product(s)."
            confidence = "high" if len(state.product_results) > 1 else "medium"
            category = "Products"
        else:
            summary = " ".join(points)
            confidence = "high" if len(points) > 1 else "medium"
            category = _category(state.contextual_query or state.user_query)

        analysis = {
            "summary": summary,
            "key_points": points,
            "sources": sources,
            "confidence": confidence,
            "needs_human_help": needs_help,
            "category": category,
        }
        state.analysis = analysis
        state.record(
            self.name, "analyze",
            f"Prepared {len(points)} support point(s) and "
            f"{len(state.product_results)} product result(s); "
            f"category={analysis['category']}."
        )
        return analysis


def _category(query: str) -> str:
    text = query.casefold()
    mapping = {
        "Orders": ("order", "delivery", "shipment", "tracking", "dispatch", "late"),
        "Returns & refunds": ("return", "refund", "damaged", "wrong item", "exchange"),
        "Products": (
            "product", "phone", "laptop", "tablet", "price", "stock",
            "available", "rating", "rated", "category", "first one",
            "second one", "first product"
        ),
        "Cancellations": ("cancel", "cancellation"),
        "Account & support": ("account", "password", "login", "support", "representative"),
    }
    for category, terms in mapping.items():
        if any(term in text for term in terms):
            return category
    return "General enquiry"


class WriterAgent:
    name = "Writer"

    def run(self, state: SharedState, revision_note: str = ""):
        analysis = state.analysis
        sections = []

        if state.product_follow_up and state.product_follow_up.get("product"):
            product = state.product_follow_up["product"]
            attr = state.product_follow_up.get("attribute", "details")
            title = product.get("title", "this product")
            price = product.get("price", 0)
            rating = product.get("rating", 0)
            category = product.get("category", "General")
            stock = product.get("stock", 0)
            desc = product.get("description", "").strip()
            stock_text = f"{stock} in stock" if stock > 0 else "Currently out of stock"

            if attr == "price":
                sections.append(f"The price of the {title} is ${price:.2f}.")
            elif attr == "rating":
                sections.append(f"The {title} has a rating of {rating} out of 5 stars.")
            elif attr == "category":
                sections.append(f"The {title} belongs to the {category} category.")
            elif attr == "stock":
                sections.append(f"The {title} has {stock_text} in our demo catalogue.")
            elif attr == "brand":
                brand = product.get("brand") or "ShopEase"
                sections.append(f"The {title} is made by {brand}.")
            else:
                detail_lines = [f"Here are more details about the {title}:"]
                if desc:
                    detail_lines.append(f"- Description: {desc}")
                detail_lines.append(f"- Price: ${price:.2f}")
                detail_lines.append(f"- Rating: {rating} / 5")
                detail_lines.append(f"- Category: {category}")
                detail_lines.append(f"- Availability: {stock_text}")
                sections.append("\n".join(detail_lines))

            sections.append(
                "Catalogue note: product details come from DummyJSON demonstration data "
                "and do not represent a real ShopEase inventory."
            )
        elif state.product_results:
            sections.append("Here are matching products from the ShopEase demo catalogue:")
            for product in state.product_results:
                stock_text = (
                    f"{product['stock']} in stock"
                    if product["stock"] > 0 else "Currently out of stock"
                )
                sections.append(
                    f"- {product['title']} — ${product['price']:.2f}. "
                    f"{stock_text}. Category: {product['category']}."
                )
            sections.append(
                "Catalogue note: product details come from DummyJSON demonstration data "
                "and do not represent a real ShopEase inventory."
            )

        if state.research_results:
            sections.append("Here is the relevant ShopEase support guidance:")
            for article in state.research_results:
                sections.append(f"- {article['content']}")
            sections.append(
                "Reference article(s): " + ", ".join(analysis.get("sources", [])) + "."
            )

        if analysis.get("needs_human_help"):
            sections.append(
                "I couldn't find a reliable answer in the available support information. "
                "You can request human support from ShopEase customer support using the Support option, and include your "
                "order number if the question is order-related."
            )
        elif (state.product_follow_up or state.product_results) and not state.research_results:
            sections.append(
                "Would you like help comparing any of these products?"
            )
        else:
            sections.append(
                "If these steps do not resolve the issue, you can request human support."
            )

        draft = "\n\n".join(sections)
        if revision_note:
            draft += f"\n\nReview adjustment: {revision_note}"
        state.draft = draft
        state.record(self.name, "draft", "Prepared a response from retrieved support and catalogue data.")
        return draft


class CriticAgent:
    name = "Critic"

    def run(self, state: SharedState):
        issues = []
        if not state.draft.strip():
            issues.append("Draft is empty.")
        if state.research_results and "Reference article(s):" not in state.draft:
            issues.append("Add the source article names to the response.")
        if state.analysis.get("needs_human_help") and "human support" not in state.draft.lower():
            issues.append("Offer human support for an unsupported query.")
        result = {"approved": not issues, "issues": issues}
        state.critique = result
        state.record(self.name, "review", "Approved draft." if not issues else f"Requested {len(issues)} revision(s).")
        return result


class CoordinatorAgent:
    """Compatibility wrapper retained for earlier project entry points."""
    name = "Coordinator"

    def __init__(self, max_revisions: int = 1):
        self.max_revisions = max_revisions
        self.researcher = ResearchAgent()
        self.analyzer = AnalyzerAgent()
        self.writer = WriterAgent()
        self.critic = CriticAgent()

    def run(self, query: str):
        state = SharedState(user_query=query.strip(), contextual_query=query.strip())
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
            "research_results": state.research_results, "product_results": state.product_results,
            "analysis": state.analysis, "critique": state.critique,
            "revision_count": state.revision_count, "trace": state.trace,
        }
