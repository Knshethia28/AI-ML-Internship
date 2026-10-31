"""Load and search the local ShopEase knowledge base."""
from __future__ import annotations
import string
import json
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(__file__).parent / "data" / "knowledge_base.json"


def load_articles(path: str | Path = DEFAULT_PATH) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as file:
        articles = json.load(file)
    if not isinstance(articles, list):
        raise ValueError("Knowledge base must contain a JSON list of articles.")
    return articles


def search_articles(query: str, articles: list[dict[str, Any]], limit: int = 3):
    words = {word.lower().strip(string.punctuation) for word in query.split()}
    words = {word for word in words if len(word) > 2}
    ranked = []
    for article in articles:
        searchable = " ".join(str(article.get(key, "")) for key in ("title", "content", "keywords")).lower()
        score = sum(1 for word in words if word in searchable)
        if score >= 2:
            ranked.append((score, article))
    ranked.sort(key=lambda item: (-item[0], str(item[1].get("id", ""))))
    return [article for _, article in ranked[:limit]]
