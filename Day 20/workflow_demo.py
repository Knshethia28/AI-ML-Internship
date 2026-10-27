
from data_analyzer_tool import data_analyzer_tool
from calculator_tool import calculator


def student_analysis_workflow(file_path, target_score):
    """Chain the Data Analyzer and Calculator tools."""

    print("\n" + "=" * 55)
    print("          STUDENT ANALYSIS WORKFLOW")
    print("=" * 55)

    # Step 1: Analyze the CSV dataset.
    print("\n[STEP 1] Analyzing the dataset...")

    analysis = data_analyzer_tool(file_path)

    if not analysis["success"]:
        print("Workflow stopped:", analysis["error"])
        return {"success": False, "error": analysis["error"]}

    print("Dataset:", analysis["file"])
    print("Rows:", analysis["rows"])

    # Step 2: Extract the average marks from the analysis.
    marks_summary = analysis["numeric_summary"].get("marks")

    if not marks_summary or marks_summary["mean"] is None:
        error = "The dataset has no usable numeric 'marks' column."
        print("Workflow stopped:", error)
        return {"success": False, "error": error}

    average_marks = marks_summary["mean"]

    print("\n[STEP 2] Average marks calculated.")
    print(f"Average marks: {average_marks:.2f}")

    # Step 3: Pass the average to the Calculator tool.
    print("\n[STEP 3] Calling Calculator tool...")

    calculation = calculator(
        average_marks,
        target_score,
        "subtract"
    )

    if not calculation["success"]:
        print("Workflow stopped:", calculation["error"])
        return {"success": False, "error": calculation["error"]}

    difference = calculation["result"]

    # Step 4: Display the final outcome.
    print("\n" + "-" * 55)
    print("                 WORKFLOW RESULT")
    print("-" * 55)
    print(f"Average marks : {average_marks:.2f}")
    print(f"Target score  : {target_score:.2f}")
    print(f"Difference    : {difference:.2f}")

    if difference >= 0:
        print("Outcome       : Average meets or exceeds the target.")
    else:
        print("Outcome       : Average is below the target.")

    print("=" * 55)

    return {
        "success": True,
        "average_marks": average_marks,
        "target_score": target_score,
        "difference": difference
    }


if __name__ == "__main__":
    result = student_analysis_workflow(
        "sample_data/students.csv",
        target_score=80
    )
