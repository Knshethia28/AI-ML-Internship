import pandas as pd
import numpy as np
from pathlib import Path

FILE_PATH = Path(__file__).parent / "marks.csv"
COLUMNS = ["ID", "Name", "Physics", "Chemistry", "Maths"]

def load_data():
    """Loads student marks data from marks.csv or initializes an empty DataFrame."""
    if not FILE_PATH.exists():
        return pd.DataFrame(columns=COLUMNS)
    try:
        df = pd.read_csv(FILE_PATH)
        if df.empty:
            return pd.DataFrame(columns=COLUMNS)
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    """Saves DataFrame back to marks.csv."""
    df.to_csv(FILE_PATH, index=False)

def get_valid_id(prompt="Enter student ID: "):
    """Validates that input is a positive integer ID."""
    while True:
        try:
            val = int(input(prompt))
            if val <= 0:
                print("ID must be a positive integer. Please try again.")
                continue
            return val
        except ValueError:
            print("Invalid input! Please enter a valid numeric ID.")

def get_valid_name(prompt="Enter student name: "):
    """Validates student name string."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Student name cannot be empty. Please try again.")
            continue
        if "," in value:
            print("Student name cannot contain commas. Please try again.")
            continue
        if value.isdigit() or not any(c.isalpha() for c in value):
            print("Invalid student name! It must contain letters and cannot be purely numeric.")
            continue
        if not all(c.isalnum() or c in " .'-" for c in value):
            print("Invalid characters in student name! Only letters, spaces, hyphens, and dots are allowed.")
            continue
        return value

def get_valid_mark(subject_name):
    """Validates subject mark between 0 and 100."""
    while True:
        try:
            val = float(input(f"Enter marks for {subject_name} (0-100): "))
            if 0 <= val <= 100:
                # Store as int if whole number, else float
                return int(val) if val.is_integer() else val
            print("Marks must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input! Please enter a numeric mark value.")

def view_and_analyze():
    """Displays student performance metrics and subject analysis using NumPy and Pandas."""
    df = load_data()
    if df.empty:
        print("\nNo student records found. Please insert students first.")
        return

    names = df["Name"].values
    marks = df[["Physics", "Chemistry", "Maths"]].values

    total_marks = np.sum(marks, axis=1)
    percentage = (total_marks / 300) * 100

    subject_averages = np.mean(marks, axis=0)
    subject_highest = np.max(marks, axis=0)

    highest_mark = np.max(marks)
    lowest_mark = np.min(marks)

    print("\n--- Student Marks Analysis ---")
    for i in range(len(names)):
        if percentage[i] >= 90:
            grade = "A+"
        elif percentage[i] >= 80:
            grade = "A"
        elif percentage[i] >= 70:
            grade = "B"
        elif percentage[i] >= 60:
            grade = "C"
        elif percentage[i] >= 50:
            grade = "D"
        elif percentage[i] >= 40:
            grade = "E"
        else:
            grade = "F"

        result = "Pass" if percentage[i] >= 40 else "Fail"

        print(
            f"ID: {df['ID'][i]} | Name: {names[i]} | "
            f"Total: {total_marks[i]} / 300 | "
            f"Percentage: {round(percentage[i], 2)} % | "
            f"Grade: {grade} | {result}"
        )

    print("\n--- Subject Analysis ---")
    subjects = ["Physics", "Chemistry", "Maths"]
    for i in range(len(subjects)):
        print(
            f"{subjects[i]} | "
            f"Average: {round(subject_averages[i], 2)} | "
            f"Highest: {subject_highest[i]}"
        )

    print(f"\nHighest Overall Mark: {highest_mark}")
    print(f"Lowest Overall Mark: {lowest_mark}")

def insert_student():
    """Inserts a new student record into marks.csv."""
    df = load_data()
    student_id = get_valid_id("Enter student ID: ")

    if not df.empty and student_id in df["ID"].values:
        print(f"Error: Student with ID {student_id} already exists!")
        return

    name = get_valid_name("Enter student name: ")
    physics = get_valid_mark("Physics")
    chemistry = get_valid_mark("Chemistry")
    maths = get_valid_mark("Maths")

    new_row = pd.DataFrame([{
        "ID": student_id,
        "Name": name,
        "Physics": physics,
        "Chemistry": chemistry,
        "Maths": maths
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    print(f"Student {name} (ID: {student_id}) added successfully!")

def update_student():
    """Updates an existing student's details and marks in marks.csv."""
    df = load_data()
    if df.empty:
        print("\nNo student records found to update.")
        return

    update_id = get_valid_id("Enter student ID to update: ")
    if update_id not in df["ID"].values:
        print(f"Student with ID {update_id} not found.")
        return

    idx = df.index[df["ID"] == update_id][0]
    print(f"Current details -> ID: {df.at[idx, 'ID']}, Name: {df.at[idx, 'Name']}, Physics: {df.at[idx, 'Physics']}, Chemistry: {df.at[idx, 'Chemistry']}, Maths: {df.at[idx, 'Maths']}")

    new_id = get_valid_id("Enter new ID: ")
    if new_id != update_id and new_id in df["ID"].values:
        print(f"Error: Student with ID {new_id} already exists!")
        return

    new_name = get_valid_name("Enter new name: ")
    new_physics = get_valid_mark("Physics")
    new_chemistry = get_valid_mark("Chemistry")
    new_maths = get_valid_mark("Maths")

    df.at[idx, "ID"] = new_id
    df.at[idx, "Name"] = new_name
    df.at[idx, "Physics"] = new_physics
    df.at[idx, "Chemistry"] = new_chemistry
    df.at[idx, "Maths"] = new_maths

    save_data(df)
    print("Student record updated successfully!")

def delete_student():
    """Deletes a student record from marks.csv."""
    df = load_data()
    if df.empty:
        print("\nNo student records found to delete.")
        return

    delete_id = get_valid_id("Enter student ID to delete: ")
    if delete_id not in df["ID"].values:
        print(f"Student with ID {delete_id} not found.")
        return

    deleted_name = df.loc[df["ID"] == delete_id, "Name"].values[0]
    df = df[df["ID"] != delete_id]
    save_data(df)
    print(f"Student {deleted_name} (ID: {delete_id}) deleted successfully!")

def main():
    print("===== Student Marks Analysis & Management System =====")

    while True:
        print("\n1. View & Analyze Marks")
        print("2. Insert Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            view_and_analyze()
        elif choice == '2':
            insert_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose an option between 1 and 5.")

if __name__ == "__main__":
    main()