"""Small session-context helpers for follow-up customer questions."""
from __future__ import annotations

import re
from typing import Any

FOLLOW_UP_CUES = re.compile(
    r"\b(it|its|they|them|that|those|these|this one|the other|"
    r"cheaper|more expensive|what about|how about|and what|does it|"
    r"is it|can i|will it|how much|which one|"
    r"first one|second one|third one|fourth one|fifth one|last one|"
    r"first product|second product|1st one|2nd one|3rd one|"
    r"that phone|this phone|that laptop|this laptop|that product|this product|"
    r"its price|its rating|its category|its description|about that)\b",
    re.IGNORECASE,
)

ORDINAL_PATTERNS: list[tuple[re.Pattern, int]] = [
    (re.compile(r"\b(?:the\s+)?(?:1st|first)(?:\s+(?:one|product|phone|laptop|item))?\b", re.IGNORECASE), 0),
    (re.compile(r"\b(?:the\s+)?(?:2nd|second)(?:\s+(?:one|product|phone|laptop|item))?\b", re.IGNORECASE), 1),
    (re.compile(r"\b(?:the\s+)?(?:3rd|third)(?:\s+(?:one|product|phone|laptop|item))?\b", re.IGNORECASE), 2),
    (re.compile(r"\b(?:the\s+)?(?:4th|fourth)(?:\s+(?:one|product|phone|laptop|item))?\b", re.IGNORECASE), 3),
    (re.compile(r"\b(?:the\s+)?(?:5th|fifth)(?:\s+(?:one|product|phone|laptop|item))?\b", re.IGNORECASE), 4),
    (re.compile(r"\b(?:the\s+)?(?:6th|sixth)(?:\s+(?:one|product|phone|laptop|item))?\b", re.IGNORECASE), 5),
    (re.compile(r"\b(?:the\s+)?last(?:\s+(?:one|product|phone|laptop|item))?\b", re.IGNORECASE), -1),
    (re.compile(r"\b(?:number|#)\s*1\b", re.IGNORECASE), 0),
    (re.compile(r"\b(?:number|#)\s*2\b", re.IGNORECASE), 1),
    (re.compile(r"\b(?:number|#)\s*3\b", re.IGNORECASE), 2),
]

SUPPORT_POLICY_PATTERNS = re.compile(
    r"\b(return|refund|exchange|cancel|cancellation|dispatch|shipped|tracking|track|shipment|courier|delivery status|late order|delayed order|payment failed|failed transaction|chargeback|billing issue|change delivery address|update shipping address)\b",
    re.IGNORECASE,
)

PRODUCT_ATTRIBUTE_PATTERNS: dict[str, re.Pattern] = {
    "price": re.compile(r"\b(price|cost|how much|pricing|how much is|expensive|cheap|rate)\b", re.IGNORECASE),
    "rating": re.compile(r"\b(rating|ratings|rated|stars?|review|reviews|score)\b", re.IGNORECASE),
    "category": re.compile(r"\b(category|type of product|which category|department)\b", re.IGNORECASE),
    "stock": re.compile(r"\b(stock|available|availability|in stock|how many left|quantity)\b", re.IGNORECASE),
    "brand": re.compile(r"\b(brand|maker|manufacturer|who makes)\b", re.IGNORECASE),
    "details": re.compile(r"\b(tell me more|describe|description|details|specs|specification|specifications|features|more about|what is it|about that|info|information)\b", re.IGNORECASE),
}


def contextualize_query(query: str, history: list[dict] | None = None) -> str:
    """Attach the latest user turn only when the new message looks like a follow-up."""
    if not history or not FOLLOW_UP_CUES.search(query):
        return query.strip()

    previous_user = next(
        (str(item.get("content", "")).strip()
         for item in reversed(history)
         if item.get("role") == "user" and item.get("content")),
        ""
    )
    if not previous_user:
        return query.strip()
    return f"{previous_user} {query.strip()}"


def is_product_follow_up(query: str, product_context: list[dict[str, Any]] | None = None) -> bool:
    """Check whether query is an inquiry about previously retrieved products."""
    if not product_context:
        return False

    is_support = bool(SUPPORT_POLICY_PATTERNS.search(query))
    has_attr = any(pat.search(query) for pat in PRODUCT_ATTRIBUTE_PATTERNS.values())
    has_ordinal = any(pat.search(query) for pat, _ in ORDINAL_PATTERNS)

    # Route clear support policy questions to the knowledge base
    if is_support and not (has_attr or has_ordinal):
        return False

    if has_ordinal:
        return True

    product_refs = re.compile(
        r"\b(it|its|that phone|this phone|that product|this product|that one|this one|the phone|the product|the item|that|this)\b",
        re.IGNORECASE,
    )
    if product_refs.search(query) and has_attr:
        return True

    query_lower = query.casefold()
    for product in product_context:
        title = product.get("title", "").casefold()
        if title and title in query_lower:
            return True

    if has_attr and (product_refs.search(query) or any(term in query_lower for term in ("phone", "product", "item", "laptop", "tablet"))):
        return True

    return False


def resolve_product_reference(
    query: str,
    product_context: list[dict[str, Any]],
    active_product: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Resolve references like 'it', 'that phone', 'the first one' from stored product context."""
    if not product_context:
        return None

    # 1. Check ordinal references (e.g. 'first one', 'second', 'last')
    for pattern, idx in ORDINAL_PATTERNS:
        if pattern.search(query):
            if idx == -1:
                return product_context[-1]
            if 0 <= idx < len(product_context):
                return product_context[idx]

    # 2. Check product title or brand match
    query_lower = query.casefold()
    for product in product_context:
        title = product.get("title", "").casefold()
        brand = product.get("brand", "").casefold()
        if title and title in query_lower:
            return product
        if brand and len(brand) > 2 and brand in query_lower:
            return product

    # 3. Check pronouns / demonstratives
    pronoun_pattern = re.compile(
        r"\b(it|its|that|this|that phone|this phone|that product|this product|that one|this one|the phone|the product|the item)\b",
        re.IGNORECASE,
    )
    if pronoun_pattern.search(query):
        if active_product:
            return active_product
        return product_context[0]

    # 4. If query asks for an attribute and product_context exists
    for attr_pattern in PRODUCT_ATTRIBUTE_PATTERNS.values():
        if attr_pattern.search(query):
            if active_product:
                return active_product
            return product_context[0]

    return active_product or product_context[0]


def detect_product_attribute(query: str) -> str:
    """Determine what attribute (price, rating, category, stock, details) is requested."""
    for attr, pattern in PRODUCT_ATTRIBUTE_PATTERNS.items():
        if pattern.search(query):
            return attr
    return "details"


def classify_query(query: str) -> str:
    text = query.casefold()
    categories = {
        "Orders": ("order", "delivery", "shipment", "tracking", "dispatch", "late"),
        "Returns & refunds": ("return", "refund", "damaged", "wrong item", "exchange"),
        "Products": (
            "product", "phone", "laptop", "tablet", "price", "stock",
            "available", "rating", "rated", "category", "first one",
            "second one", "first product", "details"
        ),
        "Cancellations": ("cancel", "cancellation"),
        "Account & support": ("account", "password", "login", "support", "representative"),
    }
    for category, terms in categories.items():
        if any(term in text for term in terms):
            return category
    return "General enquiry"
