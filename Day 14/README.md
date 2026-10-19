# Hotel Review Sentiment Analysis

## Project Overview

This project uses supervised Machine Learning to classify hotel reviews as **positive**, **negative**, or **neutral**. It uses TF-IDF text features and a Logistic Regression classifier.

## Dataset

- File: `Book1.csv`
- Review text column: `Review`
- Sentiment label column: `result`
- Rows available after cleaning: 20,491
- Label distribution: 18,831 positive, 1,569 negative, and 91 neutral reviews

## Workflow

1. Load and inspect the labeled dataset.
2. Clean review text and labels.
3. Prepare TF-IDF text features.
4. Split the data into training (80%) and testing (20%) sets, preserving class proportions.
5. Train a Logistic Regression classifier.
6. Save the trained classifier and fitted TF-IDF vectorizer with Joblib.
7. Enter a new review in the notebook to predict its sentiment.
8. Evaluate using accuracy, precision, recall, F1-score, and a confusion matrix.

## Results

The held-out test set contains 4,099 reviews. The model achieved **92.83% accuracy** on this split.

The classes are imbalanced, and the evaluation shows that the model did not correctly identify any neutral reviews in the test set. Therefore, accuracy alone does not describe performance across all classes; refer to the classification report and confusion matrix in the notebook.

## Files

- `Sentiment_Analysis.ipynb` — executable project notebook
- `Book1.csv` — labeled review dataset
- `sentiment_model.joblib` — saved classifier
- `tfidf_vectorizer.joblib` — saved TF-IDF vectorizer

## Requirements

Python 3, Pandas, scikit-learn, Joblib, and Jupyter Notebook/JupyterLab.

Install the Python packages with:

```bash
pip install pandas scikit-learn joblib jupyter
```

## Run the Project

1. Keep `Book1.csv` in the same directory as the notebook.
2. Open `Sentiment_Analysis.ipynb` in Jupyter.
3. Run the notebook cells in order. The training cells regenerate and save the model files.
4. In **Section 8**, run the user-input cell and enter a hotel review to see its predicted sentiment.
5. Review the evaluation results in **Section 9**.

The saved `.joblib` files should be loaded only from a trusted source.
