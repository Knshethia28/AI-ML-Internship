
from calculator_tool import calculator
from web_search_tool import web_search
from database_tool import database_tool
from file_reader_tool import file_reader
from weather_tool import weather_tool
from email_tool import email_tool
from date_tool import date_tool
from data_analyzer_tool import data_analyzer_tool


TOOLS = {
    "calculator": calculator,
    "web_search": web_search,
    "database": database_tool,
    "file_reader": file_reader,
    "weather": weather_tool,
    "email": email_tool,
    "date": date_tool,
    "data_analyzer": data_analyzer_tool,
}


def call_tool(tool_name, arguments):
    """Select a registered tool and call it with supplied arguments."""

    if tool_name not in TOOLS:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
            "available_tools": list(TOOLS.keys())
        }

    if not isinstance(arguments, dict):
        return {
            "success": False,
            "error": "Arguments must be provided as a dictionary."
        }

    try:
        result = TOOLS[tool_name](**arguments)

        if not isinstance(result, dict) or "success" not in result:
            return {
                "success": False,
                "error": "Tool returned an unexpected result."
            }

        return result

    except TypeError as error:
        return {
            "success": False,
            "error": f"Invalid arguments for '{tool_name}': {error}"
        }
    except Exception as error:
        return {
            "success": False,
            "error": f"Tool execution failed: {error}"
        }


def display_result(tool_name, result):
    """Display a tool call and its outcome clearly."""

    print("\n" + "=" * 52)
    print("               FUNCTION CALLING")
    print("=" * 52)
    print(f"  Selected tool: {tool_name.replace('_', ' ').title()}")

    if result["success"]:
        print("  Status       : SUCCESS")
        print("-" * 52)

        for key, value in result.items():
            if key == "success":
                continue
            print(f"  {key.replace('_', ' ').title()}: {value}")
    else:
        print("  Status       : FAILED")
        print(f"  Error        : {result['error']}")

        if "available_tools" in result:
            print(f"  Available    : {', '.join(result['available_tools'])}")

    print("=" * 52)


if __name__ == "__main__":
    # Example 1: Calculator tool call
    request = {
        "tool": "calculator",
        "arguments": {
            "a": 25,
            "b": 5,
            "operation": "multiply"
        }
    }

    result = call_tool(request["tool"], request["arguments"])
    display_result(request["tool"], result)

    # Example 2: Data Analyzer tool call
    request = {
        "tool": "data_analyzer",
        "arguments": {
            "file_path": "sample_data/students.csv"
        }
    }

    result = call_tool(request["tool"], request["arguments"])
    display_result(request["tool"], result)

    # Example 3: Error handling for an unknown tool
    request = {
        "tool": "unknown_tool",
        "arguments": {}
    }

    result = call_tool(request["tool"], request["arguments"])
    display_result(request["tool"], result)
