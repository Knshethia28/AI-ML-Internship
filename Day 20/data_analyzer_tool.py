
from pathlib import Path
import pandas as pd


def data_analyzer_tool(file_path, group_by=None, value_column=None):
    """Analyze a CSV file and return structured statistics."""

    try:
        path = Path(file_path)

        if not path.is_file():
            return {"success": False, "error": f"File not found: {file_path}"}

        df = pd.read_csv(path)

        if len(df.columns) == 0:
            return {"success": False, "error": "The CSV has no columns."}

        numeric_columns = df.select_dtypes(include="number").columns.tolist()
        summary = {}

        for column in numeric_columns:
            values = df[column].dropna()
            summary[column] = {
                "count": int(values.count()),
                "mean": float(values.mean()) if not values.empty else None,
                "median": float(values.median()) if not values.empty else None,
                "minimum": float(values.min()) if not values.empty else None,
                "maximum": float(values.max()) if not values.empty else None
            }

        result = {
            "success": True,
            "file": path.name,
            "rows": int(len(df)),
            "columns_count": int(len(df.columns)),
            "column_names": df.columns.tolist(),
            "data_types": {
                column: str(dtype) for column, dtype in df.dtypes.items()
            },
            "missing_values": {
                column: int(count)
                for column, count in df.isnull().sum().items()
            },
            "numeric_summary": summary
        }

        if group_by is not None:
            if group_by not in df.columns:
                return {
                    "success": False,
                    "error": f"Grouping column '{group_by}' not found."
                }

            if value_column not in numeric_columns:
                return {
                    "success": False,
                    "error": "Choose a valid numeric value_column."
                }

            grouped = df.groupby(group_by)[value_column].mean()
            result["grouped_average"] = {
                str(group): float(value)
                for group, value in grouped.items()
            }

        return result

    except pd.errors.EmptyDataError:
        return {"success": False, "error": "The CSV file is empty."}
    except pd.errors.ParserError as error:
        return {"success": False, "error": f"CSV parsing failed: {error}"}
    except (OSError, UnicodeError, ValueError) as error:
        return {"success": False, "error": str(error)}


def display_result(result):
    print("\n" + "=" * 60)
    print("                  CSV DATA ANALYZER")
    print("=" * 60)

    if not result["success"]:
        print(f"  Error: {result['error']}")
        print("=" * 60)
        return

    print(f"  File           : {result['file']}")
    print(f"  Total rows     : {result['rows']}")
    print(f"  Total columns  : {result['columns_count']}")
    print(f"  Column names   : {', '.join(result['column_names'])}")

    print("\n  DATA TYPES")
    print("  " + "-" * 56)
    for column, dtype in result["data_types"].items():
        print(f"  {column:<30} {dtype}")

    print("\n  MISSING VALUES")
    print("  " + "-" * 56)
    for column, count in result["missing_values"].items():
        print(f"  {column:<30} {count}")

    print("\n  NUMERIC SUMMARY")
    print("  " + "-" * 56)
    if not result["numeric_summary"]:
        print("  No numeric columns found.")
    else:
        print(f"  {'Column':<18} {'Count':>7} {'Mean':>10} "
              f"{'Median':>10} {'Min':>8} {'Max':>8}")
        for column, stats in result["numeric_summary"].items():
            mean = f"{stats['mean']:.2f}" if stats["mean"] is not None else "-"
            median = f"{stats['median']:.2f}" if stats["median"] is not None else "-"
            minimum = f"{stats['minimum']:.2f}" if stats["minimum"] is not None else "-"
            maximum = f"{stats['maximum']:.2f}" if stats["maximum"] is not None else "-"
            print(
                f"  {column[:18]:<18} {stats['count']:>7} "
                f"{mean:>10} {median:>10} {minimum:>8} {maximum:>8}"
            )

    if "grouped_average" in result:
        print("\n  GROUPED AVERAGES")
        print("  " + "-" * 56)
        for group, average in result["grouped_average"].items():
            print(f"  {group:<30} {average:.2f}")

    print("=" * 60)


if __name__ == "__main__":
    result = data_analyzer_tool("sample_data/students.csv")
    display_result(result)
