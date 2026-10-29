import unittest
from agents import AnalyzerAgent, CoordinatorAgent, CriticAgent, ResearchAgent, SharedState, WriterAgent


class MultiAgentWorkflowTests(unittest.TestCase):
    def test_research_finds_late_order_article(self):
        state = SharedState("My order delivery is late")
        results = ResearchAgent().run(state)
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], "KB-001")

    def test_analyzer_flags_no_results_for_human_help(self):
        state = SharedState("question about an unrelated topic")
        ResearchAgent().run(state)
        analysis = AnalyzerAgent().run(state)
        self.assertTrue(analysis["needs_human_help"])
        self.assertEqual(analysis["confidence"], "low")

    def test_writer_includes_sources_when_found(self):
        state = SharedState("How do I return a damaged item?")
        ResearchAgent().run(state)
        AnalyzerAgent().run(state)
        draft = WriterAgent().run(state)
        self.assertIn("Reference article(s):", draft)
        self.assertIn("Returns and refunds", draft)

    def test_critic_approves_grounded_draft(self):
        state = SharedState("How can I track my late order?")
        ResearchAgent().run(state)
        AnalyzerAgent().run(state)
        WriterAgent().run(state)
        critique = CriticAgent().run(state)
        self.assertTrue(critique["approved"])
        self.assertEqual(critique["issues"], [])

    def test_coordinator_runs_agents_and_returns_trace(self):
        result = CoordinatorAgent().run("My order is late")
        agent_names = {event["agent"] for event in result["trace"]}
        self.assertTrue({"Coordinator", "Research Agent", "Analyzer", "Writer", "Critic"}.issubset(agent_names))
        self.assertIn(result["status"], {"completed", "completed_with_review_warning"})
        self.assertTrue(result["answer"])

    def test_unknown_query_escalates_safely(self):
        result = CoordinatorAgent().run("Explain quantum entanglement")
        self.assertTrue(result["analysis"]["needs_human_help"])
        self.assertIn("customer support", result["answer"].lower())


if __name__ == "__main__":
    unittest.main()
