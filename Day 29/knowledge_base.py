"""Load, validate, and search the local ShopEase knowledge base."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(__file__).parent / "data" / "knowledge_base.json"
REQUIRED_FIELDS = ("id", "title", "content", "keywords")
KB_STOP_WORDS = {
    "a", "an", "the", "and", "or", "is", "it", "its", "are", "was", "were",
    "be", "been", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "can", "could", "will", "would", "how", "do", "does", "did",
}


def _validate_article(article: Any, index: int) -> dict[str, Any]:
    """Validate the required fields of one knowledge-base article."""
    if not isinstance(article, dict):
        raise ValueError(f"Article at index {index} must be a JSON object.")

    for field in REQUIRED_FIELDS:
        value = article.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Article at index {index} must contain a non-empty string "
                f"for '{field}'."
            )

    return article


def load_articles(path: str | Path = DEFAULT_PATH) -> list[dict[str, Any]]:
    """Load articles from JSON and validate their structure and required fields."""
    with Path(path).open("r", encoding="utf-8") as file:
        articles = json.load(file)

    if not isinstance(articles, list):
        raise ValueError("Knowledge base must contain a JSON list of articles.")

    validated_articles = [
        _validate_article(article, index)
        for index, article in enumerate(articles)
    ]

    return validated_articles


def _tokenize(text: str) -> set[str]:
    """Return distinct whole-word tokens, ignoring case and punctuation."""
    return set(re.findall(r"\b\w+\b", text.casefold()))


def search_articles(
    query: str,
    articles: list[dict[str, Any]],
    limit: int = 3,
) -> list[dict[str, Any]]:
    """Return the highest-scoring articles using whole-word keyword matching."""
    if limit < 0:
        raise ValueError("Search limit cannot be negative.")

    if limit == 0 or not isinstance(query, str) or not query.strip():
        return []

    query_words = {
        word for word in _tokenize(query)
        if len(word) > 2 and word not in KB_STOP_WORDS
    }

    if not query_words:
        return []

    ranked = []

    for article in articles:
        searchable_text = " ".join(
            str(article.get(field, ""))
            for field in ("title", "content", "keywords")
        )
        article_words = _tokenize(searchable_text)
        score = len(query_words.intersection(article_words))

        # Preserve the existing minimum of two matching query words.
        if score >= 2:
            ranked.append((score, article))

    ranked.sort(key=lambda item: (-item[0], str(item[1].get("id", ""))))
    return [article for _, article in ranked[:limit]]
