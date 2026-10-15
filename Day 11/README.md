# Day 11 – Classification Using Scikit-learn: Logistic Regression & Decision Tree

## Overview

Day 11 focuses on **Supervised Machine Learning: Classification**. Using the classic **Iris flower dataset**, two popular classification algorithms—**Logistic Regression** and **Decision Tree Classifier**—are built, evaluated, visualized, and compared to predict flower species based on morphological measurements.

---

## Files

| File | Description |
|------|-------------|
| `Iris.csv` | Dataset containing 150 records of Iris flowers across 3 species with 4 feature measurements |
| `classification.ipynb` | Complete Jupyter notebook with data cleaning, train-test splitting, model training, evaluation, tree visualization, and inference |

---

## Dataset Details

The dataset contains measurements for 3 Iris species: *Iris-setosa*, *Iris-versicolor*, and *Iris-virginica*.

| Column | Type | Description |
|--------|------|-------------|
| `Id` | Identifier | Unique record ID (dropped during preprocessing) |
| `SepalLengthCm` | Feature | Length of sepal in centimeters |
| `SepalWidthCm` | Feature | Width of sepal in centimeters |
| `PetalLengthCm` | Feature | Length of petal in centimeters |
| `PetalWidthCm` | Feature | Width of petal in centimeters |
| `Species` | Target | Class label (*Iris-setosa*, *Iris-versicolor*, *Iris-virginica*) |

---

## Workflow & Implementation

### 1. Data Loading & Preprocessing
- Loaded `Iris.csv` using Pandas.
- Dropped the non-informative `Id` column.
- Verified missing values: **0 null entries**.
- Identified and removed **3 duplicate rows** (150 → 147 unique observations).
- Separated features ($X$) and target ($y$).

### 2. Train-Test Split
- Split ratio: **80% training (117 samples)** and **20% testing (30 samples)**.
- Set `random_state=2` for reproducible results.

### 3. Model Training & Evaluation

#### Model 1: Logistic Regression
- Estimator: `LogisticRegression()`
- **Test Accuracy:** **100.0%**
- **Performance:** Perfect Precision, Recall, and F1-score (1.00) across all three classes on the test split.

#### Model 2: Decision Tree Classifier
- Estimator: `DecisionTreeClassifier(criterion="entropy")`
- **Test Accuracy:** **96.67%**
- **Performance:** Misclassified only 1 sample between *Iris-versicolor* and *Iris-virginica* due to overlapping boundary measurements.

### 4. Decision Tree Visualization
- Visualized the decision structure using Scikit-learn's `plot_tree()`.
- Highlights how threshold rules (e.g., `PetalLengthCm <= 2.45` perfectly isolating *Iris-setosa*) drive classification.

### 5. Model Comparison Summary

| Model | Criterion / Solver | Test Accuracy (%) | Key Characteristics |
|-------|-------------------|:----------------:|---------------------|
| **Logistic Regression** | L-BFGS (Default) | **100.00%** | Linear decision boundaries, probabilistic outputs |
| **Decision Tree** | Entropy (Information Gain) | **96.67%** | Non-linear, interpretable decision flowchart rules |

### 6. Inference on Unseen Sample
Tested a new sample `[5.1, 3.5, 1.4, 0.2]`:
- **Logistic Regression Prediction:** `Iris-setosa`
- **Decision Tree Prediction:** `Iris-setosa`

---

## Libraries Used

- `pandas` – data loading, cleaning, and manipulation
- `matplotlib` – plotting and tree visualization
- `scikit-learn`:
  - `model_selection.train_test_split`
  - `linear_model.LogisticRegression`
  - `tree.DecisionTreeClassifier`, `tree.plot_tree`
  - `metrics.accuracy_score`, `metrics.classification_report`

---

## How to Run

1. Install prerequisites:
   ```bash
   pip install pandas matplotlib scikit-learn notebook
   ```
2. Launch Jupyter Notebook:
   ```bash
   jupyter notebook classification.ipynb
   ```
3. Run all cells sequentially (`Kernel > Restart & Run All`).
