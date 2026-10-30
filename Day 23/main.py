
"""Command-line entry point for the Day 23 LangGraph system."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from graph import run_workflow


def main():
    parser = argparse.ArgumentParser(
        description="Run the ShopEase five-agent LangGraph workflow."
    )

    parser.add_argument(
        "query",
        nargs="*",
        help="Customer question"
    )

    parser.add_argument(
        "--output",
        default="outputs/communication_log.json",
        help="Where to save the interaction log"
    )

    parser.add_argument(
        "--max-revisions",
        type=int,
        default=1,
        help="Maximum number of Writer revisions"
    )

    args = parser.parse_args()

    # Get the customer query
    query = " ".join(args.query).strip()

    if not query:
        query = input(
            "Ask the ShopEase Multi-Agent Assistant: "
        ).strip()

    if not query:
        parser.error("A non-empty question is required.")

    # Execute the LangGraph workflow
    result = run_workflow(
        query,
        max_revisions=args.max_revisions
    )

    # Prepare the communication log from the workflow trace
    trace = result.get("trace", [])

    communication_log = [
        {
            "step": index + 1,
            "agent": event.get("agent", "Unknown"),
            "action": event.get("action", "Unknown"),
            "details": event.get("details", "")
        }
        for index, event in enumerate(trace)
    ]

    # Prepare complete output data
    output_data = {
        "query": result.get("query", query),
        "answer": result.get("answer", ""),
        "status": result.get("status", "unknown"),
        "revision_count": result.get("revision_count", 0),
        "research_results": result.get("research_results", []),
        "analysis": result.get("analysis", {}),
        "critique": result.get("critique", {}),
        "error": result.get("error", ""),
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "communication_log": communication_log
    }

    # Save the communication log and workflow result
    output_path = Path(args.output)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        json.dumps(
            output_data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    # Display final answer
    print("\n=== FINAL ANSWER ===")
    print(output_data["answer"])

    print(f"\nWorkflow status: {output_data['status']}")
    print(f"Revision count: {output_data['revision_count']}")

    # Display agent communication only once
    print("\n=== AGENT COMMUNICATION ===")

    if communication_log:
        for event in communication_log:
            print(
                f"{event['step']}. "
                f"{event['agent']} "
                f"[{event['action']}]: "
                f"{event['details']}"
            )
    else:
        print("No agent communication events recorded.")

    print(
        f"\nCommunication log saved to: "
        f"{output_path.resolve()}"
    )


if __name__ == "__main__":
    main()
