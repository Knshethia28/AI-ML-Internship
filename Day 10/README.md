# Day 10 – Machine Learning with Scikit-learn: Linear Regression

## Overview

Day 10 introduces the core Machine Learning workflow using **Scikit-learn**. A **Simple Linear Regression** model is built to predict an employee's salary based on their years of experience, evaluated using regression metrics, saved with `pickle`, and deployed via an interactive command-line prediction interface.

---

## Files

| File | Description |
|------|-------------|
| `Salary_dataset.csv` | Dataset containing `YearsExperience` and corresponding `Salary` |
| `linear_regression.py` | Standalone Python script for training, serializing with `pickle`, and interactive salary prediction |
| `linear_regression_model.pkl` | Saved (pickled) Scikit-learn Linear Regression model |
| `ml_practice.ipynb` | Comprehensive Jupyter notebook demonstrating EDA, train-test splitting, model training, evaluation metrics, and visualization |

---

## Machine Learning Workflow

1. **Data Loading & Preprocessing:** Load `Salary_dataset.csv` using Pandas, drop index columns, and separate the feature (`YearsExperience`) and target (`Salary`).
2. **Exploratory Data Analysis (EDA):** Check dataset summary, distribution, and visualize linear correlation via scatter plots.
3. **Train-Test Split:** Divide data into training and testing sets using `train_test_split`.
4. **Model Training:** Train a `LinearRegression()` model using `.fit()`.
5. **Model Evaluation:** Evaluate performance on test data using:
   - Mean Absolute Error (MAE)
   - Mean Squared Error (MSE) / Root Mean Squared Error (RMSE)
   - $R^2$ Score
6. **Model Persistence:** Save the trained model to disk as `linear_regression_model.pkl` using Python's `pickle` module for inference without retraining.

---

## How to Run

### Interactive Salary Predictor (CLI)
Run the script to train the model (if needed) and enter experience values interactively:

```bash
python linear_regression.py
```

**Example Interaction:**
```text
Model trained successfully!
Model saved successfully!

Enter years of experience (or q to quit): 1
Predicted Salary: 34,298.17

Enter years of experience (or q to quit): 5
Predicted Salary: 71,993.57

Enter years of experience (or q to quit): q
Program ended.
```

### Jupyter Notebook
To run the full end-to-end analysis and visualizations:

```bash
jupyter notebook ml_practice.ipynb
```
