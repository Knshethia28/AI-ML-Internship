# ============================================================
# Student Grade Calculator
# Linkific AI/ML Internship - Day 2 Project
# Author: Kathan Shethia
# ============================================================

def get_valid_marks(subject_name):
    """
    Takes and validates marks for a subject (must be a number between 0 and 100).
    """
    while True:
        try:
            marks = float(input(f"Enter marks for {subject_name} (0-100): "))
            if 0 <= marks <= 100:
                return marks
            else:
                print("Invalid input! Marks must be between 0 and 100.")
        except ValueError:
            print("Invalid input! Please enter a valid numerical value.")


def calculate_grade(percentage):
    """
    Determines the grade based on percentage using if/elif/else.
    """
    if percentage >= 90:
        return "A+", "Outstanding"
    elif percentage >= 80:
        return "A", "Excellent"
    elif percentage >= 70:
        return "B", "Very Good"
    elif percentage >= 60:
        return "C", "Good"
    elif percentage >= 50:
        return "D", "Pass"
    else:
        return "F", "Fail (Needs Improvement)"


def display_report_card(student_name, marks_list, total, percentage, grade, remarks):
    """
    Prints a clear and formatted summary of the student's performance.
    """
    print("\n" + "=" * 40)
    print("           STUDENT REPORT CARD")
    print("=" * 40)
    print(f"Student Name : {student_name}")
    print("-" * 40)
    
    for i, mark in enumerate(marks_list, start=1):
        print(f"Subject {i}: {mark:.2f} / 100")
        
    print("-" * 40)
    print(f"Total Marks  : {total:.2f} / {len(marks_list) * 100}")
    print(f"Percentage   : {percentage:.2f}%")
    print(f"Grade        : {grade}")
    print(f"Status       : {remarks}")
    print("=" * 40)


def main():
    print("--- Welcome to Student Grade Calculator ---")
    
    # 1. Ask for student name
    student_name = input("Enter student name: ").strip()
    while not student_name:
        print("Name cannot be empty.")
        student_name = input("Enter student name: ").strip()

    # 2. Ask for number of subjects with validation
    while True:
        try:
            num_subjects = int(input("Enter number of subjects: "))
            if num_subjects > 0:
                break
            else:
                print("Number of subjects must be at least 1.")
        except ValueError:
            print("Please enter a valid positive integer.")

    # 3. Take marks for each subject
    marks_list = []
    for i in range(1, num_subjects + 1):
        mark = get_valid_marks(f"Subject {i}")
        marks_list.append(mark)

    # 4. Calculate total and percentage
    total_marks = sum(marks_list)
    max_possible_marks = num_subjects * 100
    percentage = (total_marks / max_possible_marks) * 100

    # 5. Assign grade
    grade, remarks = calculate_grade(percentage)

    # 6. Display results
    display_report_card(student_name, marks_list, total_marks, percentage, grade, remarks)


if __name__ == "__main__":
    main()
