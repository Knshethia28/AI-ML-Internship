import io
import json
from unittest.mock import patch

import product_catalog


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_product_query_detection():
    assert product_catalog.is_product_query("Show me smartphones")
    assert not product_catalog.is_product_query("My delivery is late")


def test_search_term_removes_conversational_words():
    assert product_catalog._search_term("Do you have any smartphones under $500?") == "smartphones"


def test_price_limit_is_detected():
    assert product_catalog._price_limit("Show me laptops under $1000") == 1000.0
    assert product_catalog._price_limit("Show me laptops") is None


def test_search_products_normalizes_and_filters_results():
    payload = {
        "products": [
            {
                "id": 1, "title": "Phone A", "description": "A demo phone",
                "price": 399, "rating": 4.5, "stock": 10,
                "category": "smartphones", "thumbnail": "https://example.com/a.jpg"
            },
            {
                "id": 2, "title": "Phone B", "description": "Another demo phone",
                "price": 699, "rating": 4.2, "stock": 0,
                "category": "smartphones", "thumbnail": "https://example.com/b.jpg"
            }
        ]
    }
    with patch("product_catalog.urlopen", return_value=FakeResponse(payload)):
        results = product_catalog.search_products("Show me smartphones under $500")

    assert len(results) == 1
    assert results[0]["title"] == "Phone A"
    assert results[0]["price"] == 399.0
    assert results[0]["stock"] == 10


def test_search_products_skips_non_product_query():
    with patch("product_catalog.urlopen") as mocked:
        assert product_catalog.search_products("My order is delayed") == []
        mocked.assert_not_called()


def test_search_products_handles_api_failure():
    from urllib.error import URLError
    with patch("product_catalog.urlopen", side_effect=URLError("offline")):
        assert product_catalog.search_products("Show me phones") == []



def test_cheaper_follow_up_sorts_lowest_price_first():
    payload = {
        "products": [
            {"id": 1, "title": "Higher", "description": "", "price": 500,
             "rating": 4, "stock": 2, "category": "laptops", "thumbnail": ""},
            {"id": 2, "title": "Lower", "description": "", "price": 300,
             "rating": 4, "stock": 3, "category": "laptops", "thumbnail": ""},
        ]
    }
    with patch("product_catalog.urlopen", return_value=FakeResponse(payload)):
        results = product_catalog.search_products(
            "Show me laptops What about a cheaper one?"
        )
    assert [item["title"] for item in results] == ["Lower", "Higher"]
