# Function Calling Decision Matrix

## Objective

The Function Calling Decision Matrix identifies the appropriate tool for different user requests. Each request is mapped to a tool based on the required operation, input parameters, and expected output.

## Decision Matrix

| No. | User Request | Tool/Function to Call | Reason for Selection |
|---:|---|---|---|
| 1 | Calculate 25 multiplied by 5. | Calculator — `calculator(25, 5, "multiply")` | Performs arithmetic operations and returns the calculated result. |
| 2 | Find information about Python function calling online. | Web Search — `web_search("Python function calling")` | Generates a Google search URL for the requested topic. |
| 3 | Add a student named Aarav with ID 101 and marks 85.5. | Database — `database_tool("add", 101, "Aarav", 85.5)` | Inserts a student record into the SQLite database. |
| 4 | Display all student records. | Database — `database_tool("view")` | Retrieves the available student records from the database. |
| 5 | Read the contents of `sample_data/students.csv`. | File Reader — `file_reader("sample_data/students.csv")` | Reads the specified file and returns its content. |
| 6 | Find the current weather in Mumbai. | Weather — `weather_tool("Mumbai")` | Uses the weather service's geocoding and forecast APIs to retrieve weather data. |
| 7 | Prepare an email about the daily task update. | Email — `email_tool(recipient, subject, message)` | Validates the supplied details and prepares an email draft without sending it. |
| 8 | Find the current date and time. | Date — `date_tool("now")` | Returns the current date and time in the tool's formatted output. |
| 9 | Calculate the average marks and identify the highest and lowest marks in a CSV file. | Data Analyzer — `data_analyzer_tool(file_path)` | Reads the CSV and provides numeric summary statistics. |
| 10 | Calculate the average marks for each department in a CSV file. | Data Analyzer — `data_analyzer_tool(file_path, group_by="department", value_column="marks")` | Groups records by department and calculates the average of the selected numeric column, provided those columns exist. |
| 11 | Find the number of days between two dates. | Date — `date_tool("difference", date1, date2)` | Calculates the absolute difference in days between the supplied dates. |
| 12 | Compare the average student marks with a target score of 80. | Workflow — `student_analysis_workflow(file_path, 80)` | Chains the data analyzer and calculator to compare the dataset average with the target. |
| 13 | Request an unsupported tool through the central dispatcher. | Dispatcher — `call_tool("unknown_tool", {})` | Demonstrates how the dispatcher handles an unrecognized tool name. |
| 14 | Divide 10 by zero. | Calculator — `calculator(10, 0, "divide")` | Demonstrates validation and controlled error handling for division by zero. |

## Tool Selection Rules

1. Identify the main action requested by the user.
2. Select the tool designed for that action.
3. Supply the required arguments using the correct parameter names and data types.
4. Check the returned result and its success status.
5. If a workflow requires multiple operations, call the tools in the required order and pass the relevant output between them.
6. Handle invalid requests, missing inputs, and execution errors without treating them as successful results.

## Conclusion

The decision matrix demonstrates how user requests can be mapped to specialized tools according to their purpose. The central dispatcher provides rule-based tool invocation, while the student analysis workflow demonstrates sequential tool chaining. The current implementation uses explicit Python function calls rather than an AI model autonomously deciding which tool to invoke.
