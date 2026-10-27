
import sqlite3

DATABASE = "company_data.db"


def database_tool(action, student_id=None, name=None, marks=None):
    """Add, view, or search student records in SQLite."""

    try:
        with sqlite3.connect(DATABASE) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    marks REAL NOT NULL
                )
            """)

            cursor = connection.cursor()

            if action == "add":
                if student_id is None or not name or marks is None:
                    return {
                        "success": False,
                        "error": "Student ID, name and marks are required."
                    }

                cursor.execute(
                    "INSERT INTO students VALUES (?, ?, ?)",
                    (student_id, name.strip(), marks)
                )
                return {"success": True, "message": "Student added successfully."}

            elif action == "view":
                cursor.execute(
                    "SELECT student_id, name, marks FROM students ORDER BY student_id"
                )
                rows = cursor.fetchall()
                return {"success": True, "students": rows}

            elif action == "search":
                if student_id is None:
                    return {"success": False, "error": "Student ID is required."}

                cursor.execute(
                    "SELECT student_id, name, marks FROM students WHERE student_id = ?",
                    (student_id,)
                )
                row = cursor.fetchone()
                return {"success": True, "student": row}

            else:
                return {
                    "success": False,
                    "error": "Unsupported action. Use add, view or search."
                }

    except sqlite3.IntegrityError:
        return {"success": False, "error": "That student ID already exists."}
    except (sqlite3.Error, TypeError, ValueError) as error:
        return {"success": False, "error": str(error)}


def display_result(result):
    print("\n" + "=" * 55)
    print("                 STUDENT DATABASE")
    print("=" * 55)

    if not result["success"]:
        print(f"  Error: {result['error']}")

    elif "message" in result:
        print(f"  {result['message']}")

    elif "student" in result:
        row = result["student"]
        if row is None:
            print("  No matching student found.")
        else:
            print(f"  {'ID':<10} {'Name':<22} {'Marks':>8}")
            print("-" * 44)
            print(f"  {row[0]:<10} {row[1]:<22} {row[2]:>8.2f}")

    else:
        rows = result["students"]
        if not rows:
            print("  No student records found.")
        else:
            print(f"  {'ID':<10} {'Name':<22} {'Marks':>8}")
            print("-" * 44)
            for student_id, name, marks in rows:
                print(f"  {student_id:<10} {name:<22} {marks:>8.2f}")

    print("=" * 55)


if __name__ == "__main__":
    display_result(database_tool("add", 101, "Aarav", 85.5))
    display_result(database_tool("view"))
    display_result(database_tool("search", student_id=101))
