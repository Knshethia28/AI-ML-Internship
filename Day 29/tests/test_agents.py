from unittest.mock import patch

from agents import AnalyzerAgent, CriticAgent, ResearchAgent, SharedState, WriterAgent


def test_research_agent_retrieves_support_and_product_data():
    articles = [{
        "id": "KB-TEST",
        "title": "Returns",
        "content": "Open the order details to start a return.",
        "keywords": "return refund item",
    }]
    products = [{"id": 7, "title": "Demo Phone", "price": 299.0, "stock": 4, "category": "phones"}]
    state = SharedState(user_query="Show me a phone and explain return item", contextual_query="Show me a phone and explain return item")
    with patch("agents.search_products", return_value=products):
        ResearchAgent(articles=articles).run(state)
    assert state.research_results == articles
    assert state.product_results == products


def test_analyzer_does_not_escalate_when_relevant_data_exists():
    state = SharedState(
        user_query="Show me a phone",
        research_results=[],
        product_results=[{"title": "Demo Phone"}],
    )
    analysis = AnalyzerAgent().run(state)
    assert analysis["needs_human_help"] is False
    assert analysis["category"] == "Products"


def test_writer_uses_retrieved_product_and_article_information():
    state = SharedState(
        user_query="Show me a phone",
        research_results=[{
            "title": "Returns",
            "content": "Open the order details to start a return.",
        }],
        product_results=[{
            "title": "Demo Phone", "price": 299.0, "stock": 4, "category": "phones"
        }],
        analysis={"sources": ["Returns"], "needs_human_help": False},
    )
    answer = WriterAgent().run(state)
    assert "Demo Phone" in answer
    assert "Returns" in answer
    assert "DummyJSON demonstration data" in answer


def test_critic_approves_grounded_response():
    state = SharedState(
        user_query="Show me a phone",
        research_results=[{"title": "Returns", "content": "Return guidance."}],
        analysis={"sources": ["Returns"], "needs_human_help": False},
        draft="Return guidance. Reference article(s): Returns.",
    )
    result = CriticAgent().run(state)
    assert result["approved"] is True
