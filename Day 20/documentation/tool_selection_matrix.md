# Tool Selection Matrix

## 1. Objective

The Tool Selection Matrix maps common user requests to the appropriate Python tool. It identifies each tool's purpose, required inputs, expected output, and selection criteria.

## 2. Available Tools

| No. | Tool | Main Purpose | Required Inputs | Expected Output |
|---:|---|---|---|---|
| 1 | Calculator | Performs arithmetic operations | Two numbers and an operation | Expression, result, or error |
| 2 | Web Search | Generates a Google search URL | Search query | Search URL and status |
| 3 | Database Tool | Adds, views, and searches student records | Action and relevant student details | Database records or status |
| 4 | File Reader | Reads text or CSV file content | File path | File content or error |
| 5 | Weather Tool | Retrieves weather information | City name | Weather data or API error |
| 6 | Email Tool | Validates and prepares an email draft | Recipient, subject, message | Draft details or validation error |
| 7 | Date Tool | Retrieves the current date/time or calculates date differences | Action and, when needed, two dates | Formatted date/time or day difference |
| 8 | Data Analyzer | Analyzes CSV datasets | File path and optional grouping parameters | Dataset information and statistics |

## 3. Tool Selection Criteria

- **Arithmetic requests:** Select the Calculator when the user requests addition, subtraction, multiplication, division, or modulo.
- **Online information requests:** Select Web Search when a search URL needs to be generated or optionally opened in a browser.
- **Record management requests:** Select the Database Tool for supported student-record operations.
- **File content requests:** Select File Reader when the user wants to read a supported text or CSV file.
- **Weather requests:** Select Weather Tool when the user specifies a city and requests current weather information.
- **Email preparation requests:** Select Email Tool when the user wants an email draft prepared. This tool does not send emails.
- **Date requests:** Select Date Tool for the current date/time or the difference between two dates.
- **Dataset analysis requests:** Select Data Analyzer for CSV summaries, missing-value counts, numeric statistics, and supported group averages.

## 4. Dispatcher and Workflow Selection

The `tool_dispatcher.py` module maps supported tool names to Python functions through a predefined dictionary. The `call_tool()` function invokes the selected function with the supplied arguments.

The dispatcher provides rule-based invocation. It does not independently understand natural-language requests or use an AI model to select tools.

The `workflow_demo.py` module demonstrates tool chaining by analyzing student marks, extracting the average, and passing that value to the Calculator for comparison with a target score.

## 5. Conclusion

Selecting a tool according to the requested operation helps keep functions modular and reusable. The selection matrix also clarifies input requirements, expected outputs, and limitations, making tool invocation easier to document, test, and maintain.
