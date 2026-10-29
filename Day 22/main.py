"""Run the local ShopEase multi-agent research assistant."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from agents import CoordinatorAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a five-agent local research assistant demo.")
    parser.add_argument("query", nargs="*", help="Question to ask the assistant")
    parser.add_argument("--output", default="output.json", help="Path for the structured workflow output")
    args = parser.parse_args()
    query = " ".join(args.query).strip()
    if not query:
        query = input("Ask the ShopEase Research Assistant a question: ").strip()
    if not query:
        parser.error("A non-empty question is required.")
    result = CoordinatorAgent().run(query)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n=== FINAL ANSWER ===")
    print(result["answer"])
    print(f"\nWorkflow status: {result['status']}")
    print(f"Agents/actions recorded: {len(result['trace'])}")
    print(f"Structured output saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
