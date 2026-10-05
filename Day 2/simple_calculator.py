# ============================================================
# Simple Calculator
# Linkific AI/ML Internship - Day 2 Project
# Author: Kathan Shethia
# ============================================================

# Functions for basic arithmetic operations
def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        return "Error: Division by zero is not allowed."
    return num1 / num2


def get_number(prompt):
    """Takes input and ensures it is a valid numerical value."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def main():
    print("--- Simple Calculator ---")
    
    # 1. Take two numbers from the user
    num1 = get_number("Enter the first number: ")
    num2 = get_number("Enter the second number: ")

    # 2. Ask for operation
    print("\nSelect Operation:")
    print("  +  : Addition")
    print("  -  : Subtraction")
    print("  *  : Multiplication")
    print("  /  : Division")
    
    choice = input("Enter operator (+, -, *, /): ").strip()

    # 3. Perform calculation using if / elif / else
    if choice == "+":
        result = add(num1, num2)
        print(f"\nResult: {num1} + {num2} = {result}")
    elif choice == "-":
        result = subtract(num1, num2)
        print(f"\nResult: {num1} - {num2} = {result}")
    elif choice == "*":
        result = multiply(num1, num2)
        print(f"\nResult: {num1} * {num2} = {result}")
    elif choice == "/":
        result = divide(num1, num2)
        if isinstance(result, str):
            print(f"\n{result}")
        else:
            print(f"\nResult: {num1} / {num2} = {result}")
    else:
        print("\nInvalid choice! Please choose one of +, -, *, /.")


if __name__ == "__main__":
    main()
