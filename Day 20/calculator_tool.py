
def calculator(a, b, operation):
    """Perform a mathematical operation and return structured results."""

    operations = {
        "add": ("Addition", lambda: a + b, "+"),
        "subtract": ("Subtraction", lambda: a - b, "-"),
        "multiply": ("Multiplication", lambda: a * b, "×"),
        "divide": ("Division", lambda: a / b, "÷"),
        "modulo": ("Modulo", lambda: a % b, "%"),
    }

    operation = operation.lower().strip()

    if operation not in operations:
        return {"success": False, "error": "Unsupported operation."}

    if operation in ("divide", "modulo") and b == 0:
        return {"success": False, "error": "Cannot divide by zero."}

    try:
        label, calculate, symbol = operations[operation]
        return {
            "success": True,
            "operation": operation,
            "label": label,
            "expression": f"{a:g} {symbol} {b:g}",
            "result": calculate()
        }
    except (TypeError, ValueError, OverflowError) as error:
        return {"success": False, "error": str(error)}


def display_result(result):
    print("\n" + "=" * 36)
    print("          CALCULATOR")
    print("=" * 36)

    if not result["success"]:
        print(f"  Error: {result['error']}")
    else:
        print(f"  Operation : {result['label']}")
        print(f"  Calculation: {result['expression']}")
        print(f"  Result    : {result['result']:g}")

    print("=" * 36)


if __name__ == "__main__":
    display_result(calculator(25, 5, "multiply"))
    display_result(calculator(10, 0, "divide"))
