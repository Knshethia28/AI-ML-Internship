# Day 7 - Netflix Movies and TV Shows: End-to-End EDA

This folder contains an end-to-end **Exploratory Data Analysis (EDA)** project on the **Netflix Movies and TV Shows dataset** completed as part of **Day 7** of the **Linkific AI/ML Internship**.

---

## 📂 Project Structure

```text
Day 7/
├── data/
│   ├── netflix_titles.csv    # Original raw dataset
│   ├── netflix_sample.csv    # Sampled dataset for initial exploration
│   └── netflix_cleaned.csv   # Cleaned and processed dataset
├── notebooks/
│   └── netflix_analysis.ipynb # Complete EDA, cleaning, and visualization notebook
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## 📊 Notebook Workflow & Analysis (`netflix_analysis.ipynb`)

The analysis is structured into 7 core sections matching [`netflix_analysis.ipynb`](notebooks/netflix_analysis.ipynb):

### 1. Loading and Sampling the Dataset
- Loaded the full Netflix catalog of 8,807 titles (`netflix_titles.csv`).
- Extracted a stratified, reproducible sample of **2,000 records** (`netflix_sample.csv`) for consistent exploration and visualization.

### 2. Initial Dataset Inspection
- Inspected dataset shape, structure, column data types, and summary statistics.
- Checked for missing values across all columns (`director`, `cast`, `country`, `date_added`, `rating`).

### 3. Data Cleaning
- **3.1 Handling Missing Values**: Imputed missing categorical entries in `director`, `cast`, and `country` with `"Unknown"`.
- **Date Transformation**: Converted `date_added` strings to datetime (`date_added_parsed`) and extracted `year_added`.
- **Duration Parsing**: Extracted integer runtimes (`duration_minutes`) for movies to enable quantitative analysis.
- **Export**: Saved the cleaned sample to `data/netflix_cleaned.csv`.

### 4. Exploratory Data Analysis (EDA)
- Analyzed content distributions, release timelines, rating categories, and country contributions.

### 5. Data Visualization
- **5.1 Movies vs. TV Shows**: Bar chart comparing the count of Movies vs. TV Shows.
- **5.2 Netflix Titles Added by Year**: Line chart tracking the volume of content added over time (`date_added_parsed`).
- **5.3 Distribution of Movie Durations**: Histogram visualizing the spread and frequency of movie runtimes in minutes.
- **5.4 Distribution of Titles by Release Year**: Histogram showing content distribution across original release years.
- **5.5 Relationship Between Movie Release Year and Duration**: Scatter plot examining movie lengths across release eras.

### 6. Key Insights from the Data
- **6.1 Movies Are More Common Than TV Shows**: Movies account for **68.2%** (1,364 titles) while TV Shows account for **31.8%** (636 titles).
- **6.2 Recent Release Years Have High Representation**: Top release years in the sample are **2018** (262), **2019** (255), **2020** (231), **2017** (231), and **2016** (198).
- **6.3 TV-MA Is the Most Common Content Rating**: **TV-MA** leads with 692 titles, followed by **TV-14** (532), **TV-PG** (216), **R** (180), and **PG-13** (91).
- **6.4 The United States Has the Highest Country Count**: After splitting multi-country entries, the **United States** leads with 828 mentions, followed by **India** (247), **United Kingdom** (205), **Canada** (104), and **France** (87).
- **6.5 Movie Durations Cluster Around Feature-Length Running Times**: Average runtime is **100.33 minutes** (Median: 98 mins), with the middle 50% falling between **87 and 115 minutes**.
- **6.6 Some Movies Have Much Longer or Shorter Durations**: Runtimes range from 9 to 253 minutes with a standard deviation of **28.08 minutes**.
- **6.7 The Year 2019 Has the Highest Count of Titles Added**: Titles added peaked in **2019** (456), followed by **2020** (437), **2018** (371), **2021** (340), and **2017** (262).
- **6.8 Release Year and Addition Year Describe Different Events**: Distinguishes between original production year (`release_year`, peaked in 2018) and the year the title was cataloged on Netflix (`date_added`, peaked in 2019).

### 7. Conclusion
- Summarizes the complete data pipeline from raw ingestion to exploratory visualization, noting the importance of distinguishing missing information and interpreting sample distributions accurately.



---

## 🛠️ Requirements & Setup

Install the required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

Launch Jupyter and open the analysis notebook:

```bash
jupyter notebook notebooks/netflix_analysis.ipynb
```
*(Or open the notebook directly in VS Code)*
