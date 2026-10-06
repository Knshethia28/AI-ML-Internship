import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_valid_id(prompt="Enter student ID: "):
    while True:
        try:
            val = int(input(prompt))
            if val <= 0:
                print("ID must be a positive integer. Please try again.")
                continue
            return val
        except ValueError:
            print("Invalid input! Please enter a valid numeric ID.")

def get_valid_string(prompt, field_name="Input"):
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"{field_name} cannot be empty. Please try again.")
            continue
        if "," in value:
            print(f"{field_name} cannot contain commas. Please try again.")
            continue
        if value.isdigit() or not any(c.isalpha() for c in value):
            print(f"Invalid {field_name.lower()}! It must contain letters and cannot be purely numeric.")
            continue
        if not all(c.isalnum() or c in " .'-" for c in value):
            print(f"Invalid characters in {field_name.lower()}! Only letters, spaces, hyphens, and dots are allowed.")
            continue
        return value

def add_student():
    id = get_valid_id("Enter student ID: ")

    # Check for duplicate ID
    try:
        with open("students.txt", "r") as file:
            for line in file:
                line_str = line.strip()
                if not line_str:
                    continue
                parts = line_str.split(", ")
                if len(parts) >= 1 and int(parts[0]) == id:
                    print(f"Error: Student with ID {id} already exists!")
                    return
    except FileNotFoundError:
        pass  # File doesn't exist yet, no duplicates possible

    name = get_valid_string("Enter student name: ", "Student name")
    course = get_valid_string("Enter student course: ", "Student course")
    with open("students.txt", "a") as file:
        file.write(f"{id}, {name}, {course}\n")
    print(f"Student {name} added successfully!")

def view_students():
    try:
        with open("students.txt", "r") as file:
            data = file.read().strip()
            if data:
                print("Student List:\n" + data)
            else:
                print("No students found.")
    except FileNotFoundError:
        print("No student file found. Please add a student first.")

def search_student(search_id):
    try:
        with open("students.txt", "r") as file:
            data = file.readlines()
            if not data:
                print("No students found.")
                return False
            for line in data:
                line_str = line.strip()
                if not line_str:
                    continue
                parts = line_str.split(", ")
                if len(parts) >= 3 and int(parts[0]) == search_id:
                    print(f"Student Found:\nID: {parts[0]}, Name: {parts[1]}, Course: {parts[2]}")
                    return True
            print("Student not found.")
            return False
    except FileNotFoundError:
        print("No student file found. Please add a student first.")
        return False

def update_student(update_id):
    if not search_student(update_id):
        return
    new_id = get_valid_id("Enter new ID: ")
    new_name = get_valid_string("Enter new name: ", "Student name")
    new_course = get_valid_string("Enter new course: ", "Student course")

    # Check if new_id is already taken by a different student
    if new_id != update_id:
        try:
            with open("students.txt", "r") as file:
                for line in file:
                    line_str = line.strip()
                    if not line_str:
                        continue
                    parts = line_str.split(", ")
                    if len(parts) >= 1 and int(parts[0]) == new_id:
                        print(f"Error: Student with ID {new_id} already exists!")
                        return
        except FileNotFoundError:
            pass

    with open("students.txt", "r") as file:
        data = file.readlines()
    with open("students.txt", "w") as file:
        for line in data:
            line_str = line.strip()
            if not line_str:
                continue
            parts = line_str.split(", ")
            if len(parts) >= 3 and int(parts[0]) == update_id:
                file.write(f"{new_id}, {new_name}, {new_course}\n")
            else:
                file.write(line)
    print("Student updated successfully!")

def delete_student(delete_id):
    if not search_student(delete_id):
        return
    with open("students.txt", "r") as file:
        data = file.readlines()
    with open("students.txt", "w") as file:
        for line in data:
            line_str = line.strip()
            if not line_str:
                continue
            parts = line_str.split(", ")
            if len(parts) >= 1 and int(parts[0]) == delete_id:
                pass
            else:
                file.write(line)
    print(f"Student ID {delete_id} deleted successfully!")

def has_students():
    try:
        with open("students.txt", "r") as file:
            if file.read().strip():
                return "yes"
            return "empty"
    except FileNotFoundError:
        return "no_file"

def main():
    print("----- Student Management System -----")

    while True:
        print("\n1. Add Student\n2. View Students\n3. Search Student\n4. Update Student\n5. Delete Student\n6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            status = has_students()
            if status == "no_file":
                print("No student file found. Please add a student first.")
            elif status == "empty":
                print("No students found.")
            else:
                search_student(get_valid_id("Enter student ID to search: "))
        elif choice == '4':
            status = has_students()
            if status == "no_file":
                print("No student file found. Please add a student first.")
            elif status == "empty":
                print("No students found.")
            else:
                update_student(get_valid_id("Enter student ID to update: "))
        elif choice == '5':
            status = has_students()
            if status == "no_file":
                print("No student file found. Please add a student first.")
            elif status == "empty":
                print("No students found.")
            else:
                delete_student(get_valid_id("Enter student ID to delete: "))
        elif choice == '6':
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
