
from calculator_tool import calculator
from web_search_tool import web_search
from database_tool import database_tool
from file_reader_tool import file_reader
from date_tool import date_tool
from data_analyzer_tool import data_analyzer_tool
from tool_dispatcher import call_tool


def run_test(name, result, expected_success):
    """Print a readable test outcome."""

    passed = result.get("success") is expected_success
    status = "PASS" if passed else "FAIL"

    print(f"[{status}] {name}")

    if not passed:
        print("       Unexpected result:", result)

    return passed


def main():
    print("\n" + "=" * 48)
    print("             TOOL ERROR TESTS")
    print("=" * 48)

    tests = [
        (
            "Calculator division by zero",
            calculator(10, 0, "divide"),
            False
        ),
        (
            "Calculator unsupported operation",
            calculator(10, 5, "power"),
            False
        ),
        (
            "Empty web search query",
            web_search(""),
            False
        ),
        (
            "Missing file",
            file_reader("missing_file.txt"),
            False
        ),
        (
            "Invalid date",
            date_tool("difference", "2026-15-40", "2026-10-27"),
            False
        ),
        (
            "Unsupported date action",
            date_tool("invalid_action"),
            False
        ),
        (
            "Missing CSV file",
            data_analyzer_tool("missing_file.csv"),
            False
        ),
        (
            "Unknown dispatcher tool",
            call_tool("unknown_tool", {}),
            False
        ),
        (
            "Invalid dispatcher arguments",
            call_tool("calculator", {"a": 10}),
            False
        ),
        (
            "Unsupported database action",
            database_tool("delete"),
            False
        ),
    ]

    passed_count = 0

    for name, result, expected in tests:
        if run_test(name, result, expected):
            passed_count += 1

    print("-" * 48)
    print(f"Tests passed: {passed_count}/{len(tests)}")
    print("=" * 48)


if __name__ == "__main__":
    main()
