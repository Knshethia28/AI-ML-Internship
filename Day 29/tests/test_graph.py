import unittest
from unittest.mock import patch

from agents import CriticAgent, ResearchAgent
from graph import route_after_critic, run_workflow


class LangGraphWorkflowTests(unittest.TestCase):

    def test_late_order_query(self):
        result = run_workflow("My order delivery is late")

        self.assertEqual(result["status"], "completed")
        self.assertIn("Late or delayed orders", result["answer"])

        agents = {e["agent"] for e in result["trace"]}
        self.assertTrue({
            "Coordinator", "Research Agent",
            "Analyzer", "Writer", "Critic"
        }.issubset(agents))

    def test_return_query(self):
        result = run_workflow("How do I return a damaged item?")

        self.assertTrue(result["research_results"])
        self.assertIn("Returns and refunds", result["answer"])

    def test_unsupported_query(self):
        result = run_workflow("Explain quantum entanglement")

        self.assertEqual(result["research_results"], [])
        self.assertTrue(result["analysis"]["needs_human_help"])
        self.assertIn("customer support", result["answer"].lower())

    def test_empty_query(self):
        with self.assertRaises(ValueError):
            run_workflow("   ")

    def test_revision_routing(self):
        state = {
            "error": "",
            "status": "running",
            "critique": {
                "approved": False,
                "issues": ["Improve the response"]
            },
            "revision_count": 0,
            "max_revisions": 1
        }

        self.assertEqual(route_after_critic(state), "revise")

    def test_revision_limit(self):
        state = {
            "error": "",
            "status": "running",
            "critique": {
                "approved": False,
                "issues": ["Still needs review"]
            },
            "revision_count": 1,
            "max_revisions": 1
        }

        self.assertEqual(route_after_critic(state), "finalize")

    def test_actual_revision_loop(self):
        rejected = {
            "approved": False,
            "issues": ["Improve the response"]
        }
        approved = {
            "approved": True,
            "issues": []
        }

        with patch.object(
            CriticAgent, "run",
            side_effect=[rejected, approved]
        ) as critic:

            result = run_workflow(
                "My order delivery is late",
                max_revisions=1
            )

        self.assertEqual(critic.call_count, 2)
        self.assertEqual(result["revision_count"], 1)
        self.assertEqual(result["status"], "completed")

    def test_error_handling(self):
        with patch.object(
            ResearchAgent, "run",
            side_effect=RuntimeError("Simulated failure")
        ):
            result = run_workflow("My order delivery is late")

        self.assertEqual(result["status"], "failed")
        self.assertIn("Research Agent failed", result["error"])
        self.assertIn("customer support", result["answer"].lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)