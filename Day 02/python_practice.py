# Day 2 Python Practice - Linkific AI/ML Internship

# 1. Variables and Data Types
name = "Kathan"
day = 2
score = 85.5
is_active = True

# 2. if / elif / else
marks = 75
if marks >= 90:
    print("Grade: A")
elif marks >= 60:
    print("Grade: B")
else:
    print("Grade: C")

# 3. for loop and range()
print("For loop with range:")
for i in range(1, 6):
    print(i, end=" ")
print()

# Iterating through a list
skills = ["Python", "Machine Learning", "Data Science"]
for skill in skills:
    print("Skill:", skill)

# 4. while loop
count = 3
print("While loop countdown:")
while count > 0:
    print(count)
    count -= 1

# 5. break and continue
print("Break example (stop at 3):")
for num in range(1, 6):
    if num == 3:
        break
    print(num)

print("Continue example (skip 3):")
for num in range(1, 6):
    if num == 3:
        continue
    print(num)

# 6. Functions (Parameters and Return values)
def greet(person):
    return f"Hello, {person}! Welcome to Day 2."

def add_numbers(a, b):
    return a + b

# Calling functions
message = greet(name)
total = add_numbers(15, 25)

print(message)
print("Sum of 15 and 25:", total)
