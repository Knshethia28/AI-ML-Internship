
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv("Salary_dataset.csv")

# Remove unnecessary column
df.drop(columns=["Unnamed: 0"], errors="ignore", inplace=True)

# Select feature and target
features = df[["YearsExperience"]]
target = df["Salary"]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.25, random_state=42
)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

print("Model trained successfully!")

# Save the trained model
with open("linear_regression_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")

# Load the saved model
with open("linear_regression_model.pkl", "rb") as file:
    model = pickle.load(file)

# Predict salary using user input
while True:
    experience = input(
        "\nEnter years of experience (or q to quit): "
    )

    if experience.lower() == "q":
        print("Program ended.")
        break

    try:
        experience = float(experience)

        if experience < 0:
            print("Experience cannot be negative.")
            continue

        user_input = pd.DataFrame({
            "YearsExperience": [experience]
        })

        salary = model.predict(user_input)

        print(f"Predicted Salary: {salary[0]:,.2f}")

    except ValueError:
        print("Please enter a valid number.")
