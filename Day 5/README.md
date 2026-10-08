# Day 5 - Pandas: Basic Dataset Analysis

This folder contains the exploratory data analysis (EDA) practice completed as part of **Day 5** of the **Linkific AI/ML Internship**, focusing on **Pandas DataFrame operations**, **data inspection**, **handling missing values**, and **filtering datasets**.

---

## 📂 Files Included

### 1. `student_data.csv`
A dataset containing academic and performance details of 20 students across `CSE` and `AIML` departments:
- **Columns**: `Student_ID`, `Name`, `Department`, `Age`, `Attendance`, `Python_Marks`, `ML_Marks`, `Projects`.
- **Characteristics**: Includes real-world scenarios such as missing values (`NaN`) to practice data quality checks.

### 2. `pandas_analysis.ipynb`
An interactive Jupyter Notebook demonstrating core Pandas functionalities:
1. **Loading Data**: Reading CSV files using `pd.read_csv()`.
2. **Previewing Data**: Viewing initial and ending records using `.head()` and `.tail()`.
3. **Dataset Dimensions**: Checking row and column counts using `.shape`.
4. **Data Information & Types**: Inspecting data types and non-null counts with `.info()`.
5. **Missing Value Analysis**: Detecting missing values across columns using `.isnull().sum()`.
6. **Conditional Filtering**: Querying subsets of data based on department, attendance, marks thresholds, and project counts.
7. **Summary Statistics**: Generating descriptive statistics (`mean`, `std`, `min`, `max`, percentiles) with `.describe()`.

---

## 🚀 How to Run

Ensure `pandas` and Jupyter support are installed:

```bash
pip install pandas jupyter
```

Launch the notebook:

```bash
jupyter notebook pandas_analysis.ipynb
```
*(Or open directly in VS Code with the Jupyter extension)*
