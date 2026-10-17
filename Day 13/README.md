# Day 13 – Natural Language Processing (NLP): Text Preprocessing & TF-IDF Vectorization

## Overview

Day 13 introduces fundamental **Natural Language Processing (NLP)** concepts. The session covers end-to-end text preprocessing on movie reviews—including lowercasing, tokenization, stopword removal with negation preservation, and non-alphabetic filtering—followed by feature extraction using **Term Frequency–Inverse Document Frequency (TF-IDF)** to convert text into numerical representations for machine learning.

---

## Files

| File | Description |
|------|-------------|
| `nlp.csv` | Dataset containing 20 movie reviews labeled with sentiment (`p` = positive, `n` = negative) |
| `NLP_Text_Preprocessing.ipynb` | Jupyter notebook implementing text cleaning, tokenization, custom stopword filtering, and TF-IDF matrix generation |

---

## Dataset

The dataset consists of **20 rows × 3 columns**:

| Column | Description |
|--------|-------------|
| `id` | Unique identifier for each review (1 to 20) |
| `review` | Raw movie review text (with mixed cases, punctuation, emojis, and stopwords) |
| `result` | Target sentiment label (`p` for positive, `n` for negative) |

---

## NLP Preprocessing Pipeline

### 1. Lowercasing
Converts all review strings to lowercase to ensure consistency (e.g., `"Good"`, `"ITS"`, and `"goOD"` map to identical root tokens).

### 2. Tokenization
Splits sentences into words and punctuation marks using NLTK's `wordpunct_tokenize`.

### 3. Stopword Removal with Negation Preservation
- Uses NLTK's standard English stopwords list.
- **Negation Handling:** Explicitly preserves crucial negation words (`"not"`, `"no"`, `"nor"`) by removing them from the stopword set, preventing loss of sentiment nuance.

### 4. Punctuation & Non-Alphabetic Filtering
Filters out symbols, punctuation (such as `!`, `:`, `)`), and keeps only alphabetic tokens using `word.isalpha()`.

### 5. Sentence Reconstruction
Joins the filtered tokens back into clean, processed text strings ready for vectorization.

---

## Feature Extraction: TF-IDF Vectorization

- Implemented using Scikit-learn's `TfidfVectorizer`.
- **Vocabulary Size:** Identifies **53 unique terms** across the 20 reviews.
- **Output Matrix:** Creates a **(20, 53)** document-term numerical matrix where values represent relative term importance based on frequency in a review balanced against corpus-wide rarity.

---

## Libraries Used

- `pandas` – data loading and matrix representation
- `nltk` – text preprocessing tools:
  - `nltk.tokenize.wordpunct_tokenize`
  - `nltk.corpus.stopwords`
- `scikit-learn` – `TfidfVectorizer` for numerical feature extraction

---

## How to Run

1. Install required packages:
   ```bash
   pip install pandas nltk scikit-learn notebook
   ```
2. Open the notebook:
   ```bash
   jupyter notebook NLP_Text_Preprocessing.ipynb
   ```
3. Run all cells sequentially (`Kernel > Restart & Run All`). The NLTK `stopwords` corpus will download automatically on first execution.
