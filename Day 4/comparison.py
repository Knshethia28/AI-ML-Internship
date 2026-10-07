import numpy as np

python_list = [10, 20, 30]
numpy_array = np.array([10, 20, 30])

print("Python List:", python_list)
print("NumPy Array:", numpy_array)

print("\nList * 2:", python_list * 2)
print("NumPy Array * 2:", numpy_array * 2)

print("\nList + List:", python_list + [40, 50, 60])
print("NumPy Array + Array:", numpy_array + np.array([40, 50, 60]))