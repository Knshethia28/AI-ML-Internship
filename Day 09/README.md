# Day 9 – Exploratory Data Analysis (EDA) on Student Performance

## Overview

This session performs a full **Exploratory Data Analysis (EDA)** on the cleaned student performance dataset prepared on Day 8. The goal is to uncover meaningful patterns, visualise distributions, and derive evidence-based insights before building any machine learning models.

---

## Files

| File | Description |
|------|-------------|
| `eda.ipynb` | Main Jupyter notebook containing the complete EDA workflow |
| `cleaned_student_performance.csv` | Input dataset: 30 students, 10 columns (carried over from Day 8) |

---

## Dataset

The dataset contains **30 rows × 10 columns**, with no missing values or duplicates (verified in the notebook).

| Column | Description |
|--------|-------------|
| `student_id` | Unique student identifier (e.g., S001) |
| `name` | Student name |
| `department` | Department (AIML, CSE, ECE, IT, MECH) |
| `study_year` | Year of study |
| `age` | Student age |
| `attendance` | Attendance percentage |
| `python_marks` | Python exam marks |
| `machine_learning_marks` | Machine Learning exam marks |
| `projects_completed` | Number of projects completed |
| `join_date` | Date of joining |

---

## Notebook Workflow

### 1. Data Loading & Validation
- Loads `cleaned_student_performance.csv` using Pandas
- Confirms shape (30, 10), zero missing values, zero duplicate rows

### 2. Descriptive Statistics
- Uses `df.describe()` to generate count, mean, std, min, quartiles, and max for all numerical columns:
  - `attendance`: mean ≈ 77.97, range 57–98
  - `python_marks`: mean ≈ 70.63, range 41–95
  - `machine_learning_marks`: mean ≈ 70.77, range 35–100
  - `projects_completed`: mean ≈ 3.63, range 0–7
- Computes **department-wise averages** for Python marks, ML marks, and projects completed

### 3. Trend & Pattern Analysis
- Groups data by `department` and calculates mean for all numerical columns
- Identifies top/bottom departments for each metric:
  - Highest Python marks avg → **ECE (75.00)**
  - Highest ML marks avg → **AIML (82.30)**
  - Highest attendance avg → **MECH (86.20)**
  - Highest projects avg → **MECH (5.20)**

### 4. Data Visualisations (5 Charts)
Five charts are generated using Matplotlib and Seaborn:

| # | Chart Type | Description |
|---|-----------|-------------|
| 1 | Histogram | Distribution of student attendance percentages |
| 2 | Grouped Bar Chart | Average Python vs ML marks compared by department |
| 3 | Scatter Plot | Attendance vs ML marks relationship |
| 4 | Box Plot | Python marks distribution across departments |
| 5 | Count Plot | Frequency of different project completion counts |

### 5. Correlation Analysis
- Computes Pearson correlation between 6 selected variable pairs:
  - `attendance` ↔ `machine_learning_marks`: **0.257** (weak positive)
  - `attendance` ↔ `python_marks`: **0.156** (very weak positive)
  - `python_marks` ↔ `machine_learning_marks`: **0.041** (negligible)
  - `projects_completed` ↔ `machine_learning_marks`: **-0.090**
  - `projects_completed` ↔ `python_marks`: **-0.137**
  - `age` ↔ `machine_learning_marks`: **-0.146**

### 6. Business Insights (5 Evidence-Based Findings)

| # | Insight | Key Evidence |
|---|---------|-------------|
| 1 | ML performance varies across departments | AIML avg: **82.30**, ECE avg: **60.25** |
| 2 | Python and ML marks are nearly uncorrelated | Pearson r ≈ **0.041** |
| 3 | Attendance has only a weak positive link to ML marks | Pearson r ≈ **0.257** |
| 4 | Project completion differs between departments | MECH avg: **5.20**, IT avg: **1.00** |
| 5 | Attendance levels also differ by department | MECH: **86.20%**, ECE: **67.50%** |

> **Note:** Findings are exploratory, not causal. The dataset contains only 30 students, so generalisation requires caution.

### 7. Conclusion
- EDA transforms raw data into interpretable information
- Visualisations communicate patterns more clearly than tables alone
- Correlation does not imply causation
- Findings provide a foundation for asking better questions before model building

---

## Libraries Used

- `pandas` – data loading, grouping, statistics, correlation
- `matplotlib` – base plotting
- `seaborn` – styled visualisations (theme: `whitegrid`)

---

## How to Run

1. Ensure the required libraries are installed:
   ```bash
   pip install pandas matplotlib seaborn notebook
   ```
2. Open the notebook:
   ```bash
   jupyter notebook eda.ipynb
   ```
3. Run all cells from top to bottom (`Kernel > Restart & Run All`)
