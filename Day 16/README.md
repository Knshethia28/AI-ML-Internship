# Day 16 – Retrieval-Augmented Generation (RAG) with Local Documentation

## Overview

Day 16 focuses on building an end-to-end, fully local **Retrieval-Augmented Generation (RAG)** system. RAG augments a Large Language Model (LLM) with external, domain-specific knowledge by retrieving relevant passages from a curated document store before generating an answer.

This implementation runs **100% locally** using **Ollama** and **ChromaDB**—eliminating the need for third-party cloud services or paid API keys.

---

## Architecture & Workflow

```
[ Web Docs / Text ] 
        │
        ▼ (HTML cleaning & sanitization)
  [ Clean Text ]
        │
        ▼ (Sliding-window chunking)
  [ Text Chunks ] ──► [ nomic-embed-text ] ──► [ ChromaDB Vector Store ]
                                                         │
[ User Query ] ──► [ nomic-embed-text ] ──► (Cosine Similarity Search)
                                                         │
                                                         ▼ (Top-K Chunks)
                                                [ Context + Prompt ]
                                                         │
                                                         ▼
                                                  [ qwen2.5:3b ]
                                                         │
                                                         ▼
                                                [ Grounded Answer ]
```

### Pipeline Steps:
1. **Document Ingestion & Cleaning:** Web documentation pages (e.g., Python standard docs, Hugging Face documentation) are fetched via `requests`, parsed and stripped of HTML/nav/script boilerplate using `BeautifulSoup4`, and saved under `documents/`.
2. **Text Chunking:** Clean text is segmented into fixed-size character windows with overlapping margins (e.g., 400 characters with 50-character overlap) to preserve semantic coherence across chunk boundaries.
3. **Vector Embedding:** Chunks are vectorized using the local `nomic-embed-text` embedding model through Ollama's `/api/embed` endpoint.
4. **Vector Storage & Indexing:** Chunks, embeddings, and source metadata are stored in a persistent **ChromaDB** collection using cosine distance (`hnsw:space: cosine`).
5. **Contextual Retrieval:** User questions are converted to embeddings and queried against the collection to extract the top $K$ most semantically similar chunks.
6. **Grounded Answer Generation:** The retrieved passages are formatted into a constrained system prompt, instructing the local `qwen2.5:3b` model to answer strictly using the provided context and avoid hallucination.
7. **Chunk Size Experimentation:** Comparison of retrieval distance and answer quality across different chunking sizes (200, 400, and 700 characters).

---

## Directory Structure

```text
Day 16/
├── Day_16_Basic_RAG.ipynb     # Main Jupyter notebook executing the RAG pipeline
├── README.md                  # Documentation and execution guide
├── documents/                 # Preprocessed documentation files (.txt)
│   ├── huggingface.txt
│   └── python.txt
├── chroma_db/                 # Persistent ChromaDB vector index and metadata
└── outputs/                   # Experiment evaluation outputs and comparison CSVs
```

---

## Models & Tools

| Component | Model / Library | Role |
|-----------|-----------------|------|
| **Embedding Model** | `nomic-embed-text` (via Ollama) | High-performance text embeddings for semantic similarity |
| **Generation Model** | `qwen2.5:3b` (via Ollama) | 3B instruction-tuned local LLM for context-grounded response generation |
| **Vector Database** | `chromadb` | Persistent local vector store with HNSW indexing |
| **Web Scraping** | `requests` & `beautifulsoup4` | Document acquisition and DOM tag cleaning |
| **Data Analysis** | `pandas` | Benchmarking and chunk size comparison tables |

---

## Setup & Prerequisites

### 1. Install and Start Ollama
Ensure [Ollama](https://ollama.com/) is installed and running on your system:
```bash
ollama serve
```

Pull the required embedding and generation models:
```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:3b
```

### 2. Environment & Dependencies
Activate your virtual environment and install the required packages:
```bash
pip install requests beautifulsoup4 chromadb pandas
```

---

## How to Run

1. Open `Day_16_Basic_RAG.ipynb` in VS Code or JupyterLab.
2. Select your Python virtual environment kernel (`.venv`).
3. Ensure Ollama is active on `http://localhost:11434`.
4. Execute the notebook cells sequentially:
   - **Step 1:** Verifies Ollama connectivity and installed model tags.
   - **Step 2:** Scrapes and saves reference documentation into the `documents/` folder.
   - **Step 3:** Chunks documents, computes embeddings, and indexes them in ChromaDB.
   - **Step 4:** Prompts for a question, retrieves the top 3 chunks, and generates a grounded response with source citations.
   - **Step 5 & 6:** Runs comparative evaluations across chunk sizes (200, 400, 700 characters) and exports analysis results.

---

## Key Takeaways

1. **Hallucination Mitigation:** Grounding generation strictly within retrieved context ensures answers remain factual and verifiable with source citations.
2. **Chunking Granularity Trade-offs:**
   - **Smaller chunks (e.g., 200 chars):** Precise semantic matching but risks splitting sentences and losing surrounding context.
   - **Larger chunks (e.g., 700 chars):** Richer context per chunk but risks introducing irrelevant noise into the retrieval ranking.
   - **Moderate chunks (e.g., 400 chars with 50-char overlap):** Provides a robust balance of specificity and context for technical documentation.
3. **Data Privacy & Cost:** Running embeddings and inference via Ollama enables air-gapped, zero-cost information retrieval without sending private data to external APIs.
