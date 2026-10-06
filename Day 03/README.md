# Day 3 - Student Management System

This folder contains the project completed for **Day 3** of the **Linkific AI/ML Internship**, focusing on Python **File I/O**, **Data Persistence**, and full **CRUD** (Create, Read, Update, Delete) operations.

---

## 📂 Files Included

### 1. `student_management.py`
A command-line interface (CLI) application for managing student records.
- **Add Student**: Adds a new student record (`ID`, `Name`, `Course`) and ensures no duplicate IDs are created.
- **View Students**: Displays all stored student records from `students.txt`.
- **Search Student**: Searches for a student by ID and prints their details.
- **Update Student**: Edits existing student details (`ID`, `Name`, `Course`) with duplicate ID safeguards.
- **Delete Student**: Removes a student record by ID and updates the text file.

### 2. `students.txt`
The data storage file storing student records in comma-separated format:
```text
ID, Name, Course
```

---

## 🛡️ Key Features & Validations

- **Robust Input Handling**:
  - Validates numeric IDs and prevents runtime crashes from invalid characters.
  - Rejects empty strings and purely numeric entries for student names and courses.
  - Allows valid punctuation (e.g., `"Alice Jr."`, `"CS-101"`).
  - Blocks commas in names/courses to avoid corrupting CSV formatting.
- **File & Empty State Guards**:
  - Gracefully checks if the file exists or is empty before prompting for an ID during Search, Update, or Delete.
- **Duplicate Prevention**:
  - Blocks duplicate IDs during creation as well as updating.

---

## 🚀 How to Run

```bash
# Run the Student Management System
python student_management.py
```
