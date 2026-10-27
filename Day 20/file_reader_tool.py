
from pathlib import Path


def file_reader(file_path):
    """Read a UTF-8 text or CSV file."""

    path = Path(file_path)

    if not path.exists():
        return {"success": False, "error": f"File not found: {file_path}"}

    if not path.is_file():
        return {"success": False, "error": "The path is not a file."}

    try:
        content = path.read_text(encoding="utf-8")
        return {
            "success": True,
            "file": path.name,
            "content": content
        }
    except (OSError, UnicodeError) as error:
        return {"success": False, "error": str(error)}


def display_result(result):
    print("\n" + "=" * 55)
    print("                  FILE READER")
    print("=" * 55)

    if not result["success"]:
        print(f"  Error: {result['error']}")
    else:
        print(f"  File: {result['file']}")
        print("-" * 55)
        print(result["content"].rstrip() or "(File is empty)")
        print("-" * 55)

    print("=" * 55)


if __name__ == "__main__":
    display_result(file_reader("sample_data/students.csv"))
