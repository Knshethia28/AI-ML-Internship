"""Read-only product lookup using the public DummyJSON demonstration API.

DummyJSON is mock catalogue data, not a live retailer inventory system.
"""
from __future__ import annotations

import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://dummyjson.com"
TIMEOUT_SECONDS = 4

PRODUCT_TERMS = {
    "product", "products", "phone", "phones", "smartphone", "smartphones",
    "laptop", "laptops", "computer", "computers", "tablet", "tablets",
    "headphone", "headphones", "earphone", "earphones", "camera", "cameras",
    "watch", "watches", "shoe", "shoes", "beauty", "skincare", "furniture",
    "fragrance", "perfume", "groceries", "grocery", "vehicle", "motorcycle",
    "shirt", "shirts", "dress", "dresses", "bag", "bags", "accessory",
    "accessories", "electronics"
}
STOP_WORDS = {
    "do", "you", "have", "any", "show", "me", "find", "search", "for", "a",
    "an", "the", "some", "i", "want", "need", "looking", "looking", "is",
    "there", "are", "what", "which", "can", "could", "please", "under",
    "below", "less", "than", "over", "above", "more", "price", "cost",
    "cheap", "cheaper", "expensive", "available", "availability", "in",
    "stock", "with", "and", "or", "of", "on", "to", "it", "this", "that",
    "one", "ones", "for", "me", "my", "your", "shop", "ecommerce", "what", "about", "how"
}


def is_product_query(query: str) -> bool:
    words = set(re.findall(r"[a-z]+", query.casefold()))
    return bool(words & PRODUCT_TERMS)


def _search_term(query: str) -> str:
    words = re.findall(r"[a-z0-9]+", query.casefold())
    terms = [word for word in words if word not in STOP_WORDS and not word.isdigit()]
    # Avoid sending a long conversational sentence to the search endpoint.
    return " ".join(terms[:4]) or "product"


def _price_limit(query: str) -> float | None:
    match = re.search(
        r"(?:under|below|less than|up to|maximum|max\.?)\s*[$₹]?\s*(\d+(?:\.\d+)?)",
        query.casefold()
    )
    return float(match.group(1)) if match else None


def search_products(query: str, limit: int = 6) -> list[dict]:
    """Search DummyJSON and return a small, normalized product list.

    Network/API failures are non-fatal: the rest of the support workflow continues.
    """
    if not query or not is_product_query(query):
        return []

    term = _search_term(query)
    url = f"{API_BASE}/products/search?{urlencode({'q': term, 'limit': max(1, min(limit, 20))})}"
    request = Request(url, headers={"User-Agent": "ShopEase-Demo/1.0"})
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        return []

    raw_products = payload.get("products", []) if isinstance(payload, dict) else []
    max_price = _price_limit(query)
    products = []
    for item in raw_products:
        try:
            product = {
                "id": int(item["id"]),
                "title": str(item.get("title", "Unnamed product")),
                "description": str(item.get("description", "")),
                "price": float(item.get("price", 0)),
                "rating": float(item.get("rating", 0)),
                "stock": int(item.get("stock", 0)),
                "category": str(item.get("category", "Uncategorized")),
                "thumbnail": str(item.get("thumbnail", "")),
                "brand": str(item.get("brand") or ""),
            }
        except (TypeError, ValueError, KeyError):
            continue
        if max_price is not None and product["price"] > max_price:
            continue
        products.append(product)
    if "cheaper" in query.casefold() or "lowest price" in query.casefold():
        products.sort(key=lambda item: item["price"])
    elif "more expensive" in query.casefold():
        products.sort(key=lambda item: item["price"], reverse=True)
    return products[:limit]
