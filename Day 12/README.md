# Day 12 – Model Evaluation and Performance Analysis

## Overview

Day 12 focuses on **Model Evaluation and Performance Metrics** for supervised classification. Rather than retraining models, the previously trained **Logistic Regression** and **Decision Tree** classifiers from Day 11 are loaded from serialized pickle files and evaluated on unseen test data using comprehensive classification metrics and confusion matrices.

---

## Files

| File | Description |
|------|-------------|
| `classification_evaluation.ipynb` | Jupyter notebook for loading saved models, evaluating metrics, plotting confusion matrices, and comparing models |
| `performance_report.txt` | Automatically generated text file containing classification reports and model comparison summary |

---

## Workflow & Implementation

1. **Model & Data Loading:**
   - Deserialized `logistic_regression.pkl` and `decision_tree.pkl` from Day 11's `saved_models/` folder using Python's `pickle` module.
   - Loaded and preprocessed the Iris dataset (`147` cleaned records after dropping `Id` and duplicate rows).
   - Recreated the exact Day 11 test split (80% train / 20% test, `random_state=2`).

2. **Performance Metrics Computed:**
   - **Accuracy & Balanced Accuracy**
   - **Precision (Macro)**
   - **Recall (Macro)**
   - **F1-Score (Macro & Weighted)**
   - **Confusion Matrix** visualization using `ConfusionMatrixDisplay`

3. **Evaluation Summary:**

| Model | Accuracy (%) | Precision (Macro %) | Recall (Macro %) | F1-Score (Macro %) |
|-------|:------------:|:-------------------:|:----------------:|:------------------:|
| **Logistic Regression** | **100.00%** | **100.00%** | **100.00%** | **100.00%** |
| **Decision Tree** | **96.67%** | **96.88%** | **96.21%** | **96.33%** |

4. **Report Generation:**
   - Exported complete classification reports and the comparison table to `performance_report.txt`.

---

## How to Run

1. Ensure the Day 11 models exist in `Day 11/saved_models/`.
2. Launch the Jupyter notebook:
   ```bash
   jupyter notebook classification_evaluation.ipynb
   ```
3. Run all cells (`Kernel > Restart & Run All`) to regenerate the outputs and `performance_report.txt`.
