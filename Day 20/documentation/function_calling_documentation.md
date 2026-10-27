# Function Calling Documentation

## 1. Introduction

Function calling allows a program to invoke a specific function with appropriate arguments to perform a task. A tool exposes a defined operation, accepts inputs, processes them, and returns a result.

In this project, each tool is implemented as a Python function. The functions return structured dictionaries containing a success status and relevant output or error information. Separate display functions format results for terminal output where provided.

The project demonstrates Python-based function invocation and rule-based dispatching. It does not implement native AI-model function calling.

## 2. Tool Function Reference

### 2.1 Calculator

**Module:** `calculator_tool.py`

**Function:** `calculator(a, b, operation)`

Supported operations include `add`, `subtract`, `multiply`, `divide`, and `modulo`.

Example:

```python
from calculator_tool import calculator

result = calculator(25, 5, "multiply")
print(result)
```

The function returns the calculation result or a structured error for unsupported operations and division by zero.

### 2.2 Web Search

**Module:** `web_search_tool.py`

**Function:** `web_search(query, open_browser=False)`

Example:

```python
from web_search_tool import web_search

result = web_search("Python function calling")
print(result)
```

The function generates a Google search URL and can optionally open it in a browser. It does not retrieve or summarize search results.

### 2.3 Database Tool

**Module:** `database_tool.py`

**Function:** `database_tool(action, student_id=None, name=None, marks=None)`

Supported actions include adding, viewing, and searching student records.

Example:

```python
from database_tool import database_tool

result = database_tool("view")
print(result)
```

The tool uses SQLite to store and retrieve student records.

### 2.4 File Reader

**Module:** `file_reader_tool.py`

**Function:** `file_reader(file_path)`

Example:

```python
from file_reader_tool import file_reader

result = file_reader("sample_data/students.csv")
print(result)
```

The function reads a supported text or CSV file and returns its content or an error.

### 2.5 Weather Tool

**Module:** `weather_tool.py`

**Function:** `weather_tool(city)`

Example:

```python
from weather_tool import weather_tool

result = weather_tool("Mumbai")
print(result)
```

The tool uses Open-Meteo geocoding and forecast services. An internet connection is required, and the tool may return an error if a request fails.

### 2.6 Email Tool

**Module:** `email_tool.py`

**Function:** `email_tool(recipient, subject, message)`

Example:

```python
from email_tool import email_tool

result = email_tool(
    "student@example.com",
    "Daily Task Update",
    "The daily task has been completed."
)
print(result)
```

The function validates the supplied details and prepares a draft. It does not connect to an email service or send messages.

### 2.7 Date Tool

**Module:** `date_tool.py`

**Function:** `date_tool(action, date1=None, date2=None)`

Example:

```python
from date_tool import date_tool

result = date_tool("difference", "2026-10-01", "2026-10-27")
print(result)
```

The supported actions retrieve the current date/time or calculate the absolute difference in days between two dates.

### 2.8 Data Analyzer

**Module:** `data_analyzer_tool.py`

**Function:** `data_analyzer_tool(file_path, group_by=None, value_column=None)`

Example:

```python
from data_analyzer_tool import data_analyzer_tool

result = data_analyzer_tool("sample_data/students.csv")
print(result)
```

The tool uses Pandas to analyze CSV data, report dataset dimensions and column information, identify missing values, and calculate numeric statistics. Optional grouping can calculate averages by category when the specified columns exist.

## 3. Central Tool Dispatcher

**Module:** `tool_dispatcher.py`

The dispatcher stores the supported functions in a dictionary named `TOOLS`. The `call_tool()` function accepts a tool name and a dictionary of arguments, then invokes the corresponding function.

Example:

```python
from tool_dispatcher import call_tool

result = call_tool(
    "calculator",
    {"a": 25, "b": 5, "operation": "multiply"}
)

print(result)
```

The dispatcher checks whether the tool exists, validates the argument structure, catches relevant invocation errors, and returns a structured result.

## 4. Error Handling

Error handling prevents common failures from terminating the program unexpectedly.

Examples demonstrated by the project include:

- Division by zero.
- Unsupported calculator operations.
- Empty web search queries.
- Missing files and CSV files.
- Invalid dates and unsupported date actions.
- Unknown tool names.
- Invalid dispatcher arguments.
- Unsupported database actions.

The `test_tools.py` script tested 10 error scenarios, and the reported terminal output confirmed that all 10 passed.

## 5. Function Calling vs. Tool Chaining

**Function calling** invokes a function to perform a specific operation with supplied arguments.

**Tool chaining** connects multiple operations so that the output of one operation becomes an input to another.

The dispatcher demonstrates rule-based function invocation. The student analysis workflow demonstrates tool chaining by passing the CSV analyzer's average marks to the Calculator.

## 6. Limitations

- Web Search generates a search URL rather than extracting search results.
- Email Tool creates drafts rather than sending emails.
- Weather Tool requires internet access and depends on the external weather service.
- Data Analyzer requires Pandas and a readable CSV file.
- The dispatcher relies on predefined tool names and argument dictionaries.

## 7. Conclusion

The project demonstrates modular tool creation, function invocation, structured results, error handling, and sequential tool chaining. These components provide a foundation for integrating tools into larger applications or a future AI-driven function-calling system.
