# Day 4 - NumPy Basics & Student Marks Analysis

This folder contains the practice exercises and data analysis projects completed as part of **Day 4** of the **Linkific AI/ML Internship**, focusing on **NumPy arrays**, **vectorized computations**, and **dataset analysis**.

---

## 📂 Files Included

### 1. `numpy_practice.py`
Introduction to essential NumPy concepts:
- **1D & 2D Arrays**: Array creation and multidimensional structure.
- **Indexing & Slicing**: Accessing individual elements and sub-arrays.
- **Statistical Operations**: Calculating `sum()`, `mean()`, `max()`, and `min()`.

### 2. `comparison.py`
A practical comparison between Python standard lists and NumPy arrays:
- **Scalar Multiplication**: Demonstrates list repetition (`[10, 20] * 2`) vs. vectorized element-wise multiplication (`np.array([10, 20]) * 2`).
- **Addition**: Demonstrates list concatenation vs. element-wise vector addition.

### 3. `marks.csv`
Sample dataset containing student performance records:
```csv
ID,Name,Physics,Chemistry,Maths
1,Rahul,78,85,92
...
```

### 4. `students_marks_analysis.py`
A menu-driven CLI application using **Pandas** and **NumPy** for CRUD operations and student performance analysis:
- **View & Analyze Marks**:
  - **Student Metrics (`axis=1`)**: Total marks, percentages, grades (`A+` to `F`), and Pass/Fail status.
  - **Subject Metrics (`axis=0`)**: Class average and highest score for Physics, Chemistry, and Maths.
  - **Overall Extremes**: Highest and lowest marks scored across all subjects.
- **Insert Student**: Adds a new student record to `marks.csv` with unique ID validation, name validation, and `0 - 100` marks constraints.
- **Update Student**: Modifies student name or marks for any subject in `marks.csv`.
- **Delete Student**: Removes a student record by ID and updates `marks.csv`.

---

## 🚀 How to Run

Make sure you have `numpy` and `pandas` installed:

```bash
pip install numpy pandas
```

Run any script using Python:

```bash
# Run NumPy practice
python numpy_practice.py

# Run list vs array comparison
python comparison.py

# Run student marks analysis
python students_marks_analysis.py
```
