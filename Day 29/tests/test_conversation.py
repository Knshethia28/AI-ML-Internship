from conversation import (
    classify_query,
    contextualize_query,
    detect_product_attribute,
    is_product_follow_up,
    resolve_product_reference,
)


def test_follow_up_uses_previous_customer_question():
    history = [{"role": "user", "content": "Show me laptops"}]
    assert contextualize_query("What about a cheaper one?", history) == (
        "Show me laptops What about a cheaper one?"
    )


def test_new_topic_does_not_append_old_context():
    history = [{"role": "user", "content": "Show me laptops"}]
    assert contextualize_query("How do I return an item?", history) == (
        "How do I return an item?"
    )


def test_context_without_history_is_unchanged():
    assert contextualize_query("Is it available?", []) == "Is it available?"


def test_query_categories():
    assert classify_query("My order delivery is late") == "Orders"
    assert classify_query("I need a refund") == "Returns & refunds"
    assert classify_query("What is the price of the first one?") == "Products"


def test_product_follow_up_detection():
    products = [
        {"id": 1, "title": "Phone A", "price": 499.0, "category": "smartphones"},
        {"id": 2, "title": "Phone B", "price": 799.0, "category": "smartphones"},
    ]
    assert is_product_follow_up("What is the price of the first one?", products) is True
    assert is_product_follow_up("What is its rating?", products) is True
    assert is_product_follow_up("Tell me more about that phone.", products) is True
    assert is_product_follow_up("What about its category?", products) is True
    assert is_product_follow_up("How do I return a damaged item?", products) is False
    assert is_product_follow_up("What is the price?", []) is False


def test_resolve_product_reference_ordinal():
    products = [
        {"id": 1, "title": "Phone A", "price": 499.0},
        {"id": 2, "title": "Phone B", "price": 799.0},
    ]
    assert resolve_product_reference("What is the price of the first one?", products) == products[0]
    assert resolve_product_reference("What is the price of the second one?", products) == products[1]
    assert resolve_product_reference("Tell me about the last product", products) == products[-1]


def test_resolve_product_reference_pronouns():
    products = [
        {"id": 1, "title": "Phone A", "price": 499.0},
        {"id": 2, "title": "Phone B", "price": 799.0},
    ]
    # When active_product is specified, pronoun resolves to active_product
    assert resolve_product_reference("What is its rating?", products, active_product=products[1]) == products[1]
    # When active_product is None, default is the primary product
    assert resolve_product_reference("What is its rating?", products) == products[0]


def test_detect_product_attributes():
    assert detect_product_attribute("What is the price?") == "price"
    assert detect_product_attribute("How much does it cost?") == "price"
    assert detect_product_attribute("What is its rating?") == "rating"
    assert detect_product_attribute("Tell me more about that phone") == "details"
    assert detect_product_attribute("What about its category?") == "category"
    assert detect_product_attribute("Is it available in stock?") == "stock"
