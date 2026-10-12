# Day 8 - Data Preprocessing and Cleaning

This folder contains the data preprocessing and data-cleaning exercises completed as part of **Day 8** of the **Linkific AI/ML Internship**, focusing on preparing raw data for reliable exploratory analysis and machine learning workflows using **Pandas**.

---

## 📂 Files Included

### 1. `student-data-v2.csv`
The raw, uncleaned student dataset (33 rows, 10 columns):
- Contains data-quality issues including 3 duplicate records, missing values in numerical columns (`age`, `attendance`, `python_marks`, `ml_marks`), inconsistent casing/whitespace in categorical fields (e.g., ` aiml `, `Cse`), and dates stored as raw strings (`DD-MM-YYYY`).

### 2. `student_data_deduplicated.csv`
An intermediate dataset saved after detecting and removing duplicate entries (30 rows, 10 columns).

### 3. `cleaned_student_performance.csv`
The final sanitized dataset exported after completing all data cleaning, imputation, standardization, and type casting steps (30 rows, 10 columns, 0 missing values).

### 4. `data_preprocessing.ipynb`
An interactive Jupyter Notebook detailing the end-to-end data preprocessing pipeline.

---

## 📊 Notebook Workflow & Sections (`data_preprocessing.ipynb`)

The notebook follows a systematic data cleaning pipeline structured into 5 core sections:

### 1. Removing Duplicate Records
- Identified duplicate entries using `df.duplicated()` (detected **3 duplicate rows**).
- Dropped duplicates using `df.drop_duplicates()`, reducing the dataset from **33 to 30 unique records**.
- Exported the intermediate deduplicated dataset to `student_data_deduplicated.csv`.

### 2. Handling Missing Values
- Checked missing value counts across all columns: `age` (2), `attendance` (2), `python_marks` (2), `ml_marks` (2).
- Applied **median imputation** on numerical features to avoid sensitivity to outliers:
  - `age`: imputed with median **21.0**
  - `attendance`: imputed with median **76.8**
  - `python_marks`: imputed with median **72.0**
  - `ml_marks`: imputed with median **73.5**
- Confirmed that all missing numerical values were resolved with zero remaining nulls.

### 3. Standardizing Column Names and Values
- **Renamed columns** for clarity and consistency:
  - `year` $\rightarrow$ `study_year`
  - `ml_marks` $\rightarrow$ `machine_learning_marks`
- **Standardized text and categorical values**: Stripped leading/trailing whitespace from student names (e.g., `ISHAAN`) and normalized department names to uppercase (`.str.strip().str.upper()`), unifying categories into: `AIML` (10), `CSE` (8), `MECH` (5), `ECE` (4), and `IT` (3).

### 4. Correcting Data Types
- Converted `join_date` from string (`object`) to `datetime64` using `pd.to_datetime()` with format `"%d-%m-%Y"` and `errors="coerce"`.
- Verified that all dates were successfully parsed without missing dates (`NaT`).

### 5. Saving and Verifying the Cleaned Dataset
- Exported the final processed DataFrame to `cleaned_student_performance.csv` (with `index=False`).
- Conducted final verification checks:
  - **Final Shape**: 30 rows $\times$ 10 columns
  - **Duplicates Remaining**: 0
  - **Missing Values**: 0 across all columns
  - **Data Types**: Appropriate numeric, string, and datetime formats

---

## 🚀 How to Run

Ensure `pandas` and Jupyter support are installed:

```bash
pip install pandas jupyter
```

Launch the notebook:

```bash
jupyter notebook data_preprocessing.ipynb
```
*(Or open directly in VS Code using the Jupyter extension)*
