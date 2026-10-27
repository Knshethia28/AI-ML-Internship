
from datetime import datetime, date


def date_tool(action, date1=None, date2=None):
    """Return current date/time or calculate the difference between dates."""

    if action == "now":
        current = datetime.now()
        return {
            "success": True,
            "date": current.strftime("%d %B %Y"),
            "time": current.strftime("%I:%M:%S %p")
        }

    if action == "difference":
        if not date1 or not date2:
            return {
                "success": False,
                "error": "Both dates are required in YYYY-MM-DD format."
            }

        try:
            first = date.fromisoformat(date1)
            second = date.fromisoformat(date2)
            return {
                "success": True,
                "date1": first.isoformat(),
                "date2": second.isoformat(),
                "days_between": abs((second - first).days)
            }
        except ValueError:
            return {
                "success": False,
                "error": "Invalid date. Use YYYY-MM-DD."
            }

    return {
        "success": False,
        "error": "Unsupported action. Use 'now' or 'difference'."
    }


def display_result(result):
    print("\n" + "=" * 42)
    print("                 DATE TOOL")
    print("=" * 42)

    if not result["success"]:
        print(f"  Error: {result['error']}")
    elif "date" in result and "time" in result:
        print(f"  Current date: {result['date']}")
        print(f"  Current time: {result['time']}")
    else:
        print(f"  First date : {result['date1']}")
        print(f"  Second date: {result['date2']}")
        print(f"  Difference : {result['days_between']} days")

    print("=" * 42)


if __name__ == "__main__":
    display_result(date_tool("now"))
    display_result(
        date_tool("difference", "2026-10-01", "2026-10-27")
    )
