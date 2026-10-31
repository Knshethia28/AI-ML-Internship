
import json
import pytest

from knowledge_base import load_articles, search_articles


@pytest.fixture
def sample_articles():
    return [
        {
            "id": "KB002",
            "title": "Late orders",
            "content": "Customers can track delayed delivery orders.",
            "keywords": "late delivery tracking"
        },
        {
            "id": "KB001",
            "title": "Late delivery support",
            "content": "Contact support for delayed orders.",
            "keywords": "delivery assistance"
        },
        {
            "id": "KB003",
            "title": "Returns and refunds",
            "content": "Damaged items can be returned.",
            "keywords": "return refund damaged"
        }
    ]


# ---------------- LOAD ARTICLES TESTS ----------------

def test_load_articles_successfully(tmp_path, sample_articles):
    file_path = tmp_path / "knowledge_base.json"
    file_path.write_text(json.dumps(sample_articles), encoding="utf-8")

    result = load_articles(file_path)

    assert len(result) == 3
    assert result[0]["id"] == "KB002"


def test_load_articles_rejects_non_list_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text('{"title": "Invalid"}', encoding="utf-8")

    with pytest.raises(ValueError, match="JSON list"):
        load_articles(file_path)


def test_load_articles_missing_file(tmp_path):
    file_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_articles(file_path)


def test_load_articles_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid json}", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_articles(file_path)


# ---------------- SEARCH ARTICLES TESTS ----------------

def test_search_matches_relevant_articles(sample_articles):
    results = search_articles("late delivery", sample_articles)

    assert len(results) == 2
    assert all(article["id"] in ["KB001", "KB002"] for article in results)


def test_search_is_case_insensitive_and_ignores_punctuation(sample_articles):
    results = search_articles("LATE, DELIVERY!", sample_articles)

    assert len(results) == 2


def test_search_requires_at_least_two_matching_words(sample_articles):
    results = search_articles("late", sample_articles)

    assert results == []


def test_search_returns_empty_for_unmatched_query(sample_articles):
    results = search_articles("quantum physics", sample_articles)

    assert results == []


def test_search_handles_empty_query(sample_articles):
    results = search_articles("   ", sample_articles)

    assert results == []


def test_search_ranks_articles_and_respects_limit(sample_articles):
    results = search_articles("late delivery support", sample_articles, limit=2)

    assert len(results) == 2
    assert results[0]["id"] == "KB001"
    assert results[1]["id"] == "KB002"


def test_search_zero_limit_returns_empty_list(sample_articles):
    results = search_articles("late delivery", sample_articles, limit=0)

    assert results == []
