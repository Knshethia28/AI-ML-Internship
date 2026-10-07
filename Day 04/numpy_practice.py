import numpy as np

print("NumPy version:", np.__version__)

# 1D Array
marks = np.array([78, 85, 92, 67, 88])

print("\n1D Array:")
print(marks)

# 2D Array
student_marks = np.array([
    [78, 85, 92],
    [67, 88, 75],
    [90, 95, 89]
])

print("\n2D Array:")
print(student_marks)

# Indexing
print("\nIndexing:")
print("First mark:", marks[0])
print("Third mark:", marks[2])
print("First student's Chemistry mark:", student_marks[0, 1])

# Slicing
print("\nSlicing:")
print("First three marks:", marks[:3])
print("First two students:")
print(student_marks[:2])

# Mathematical Operations
print("\nMathematical Operations:")
print("Sum:", np.sum(marks))
print("Mean:", np.mean(marks))
print("Maximum:", np.max(marks))
print("Minimum:", np.min(marks))