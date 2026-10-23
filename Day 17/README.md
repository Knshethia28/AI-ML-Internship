# Day 17 – PDF Question-Answering RAG API with FastAPI & Google Gemini

## Overview

Day 17 focuses on building and validating a RESTful **Retrieval-Augmented Generation (RAG)** backend service using **FastAPI**, **PyMuPDF**, and the **Google GenAI SDK (Gemini)**.

The API enables users to upload PDF documents, automatically extracts and indexes text page-by-page, performs keyword-based contextual chunk retrieval, and generates factual, context-grounded answers citing the specific source pages.

---

## Architecture & Workflow

```text
                                  ┌────────────────────────┐
                                  │      Client / UI       │
                                  │   (FastAPI Swagger)    │
                                  └───────────┬────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      │ POST /upload (PDF file)                       │ POST /ask (JSON body)
                      ▼                                               ▼
         ┌─────────────────────────┐                     ┌─────────────────────────┐
         │     File Validation     │                     │     Document Lookup     │
         │ (.pdf check & non-empty)│                     │  (in-memory documents)  │
         └────────────┬────────────┘                     └────────────┬────────────┘
                      ▼                                               ▼
         ┌─────────────────────────┐                     ┌─────────────────────────┐
         │   PyMuPDF (fitz) Text   │                     │  Text Chunking & Preproc│
         │   Extraction per Page   │                     │  (1000-char intervals)  │
         └────────────┬────────────┘                     └────────────┬────────────┘
                      ▼                                               ▼
         ┌─────────────────────────┐                     ┌─────────────────────────┐
         │ Scanned PDF Rejection   │                     │ Keyword-Overlap Ranking │
         │ (rejects non-text PDFs) │                     │ (stopwords + overview)  │
         └────────────┬────────────┘                     └────────────┬────────────┘
                      ▼                                               ▼
         ┌─────────────────────────┐                     ┌─────────────────────────┐
         │ Store in Document Cache │                     │ Select Top-4 Chunks     │
         │ Returns: "document_id"  │                     │ & Build Prompt Context  │
         └─────────────────────────┘                     └────────────┬────────────┘
                                                                      ▼
                                                         ┌─────────────────────────┐
                                                         │   Google Gemini API     │
                                                         │  (Grounded Generation)  │
                                                         └────────────┬────────────┘
                                                                      ▼
                                                         ┌─────────────────────────┐
                                                         │ Response: answer +      │
                                                         │ "source_pages" [1, 3..] │
                                                         └─────────────────────────┘
```

---

## Directory Structure

```text
Day 17/
├── main.py                      # FastAPI application with PDF extraction & Gemini integration
├── README.md                    # Project documentation and execution guide
├── RAG_API_Testing_Report.md    # Comprehensive test report for valid and edge-case inputs
├── Improvement_Suggestions.md   # Architectural roadmap and production enhancement recommendations
└── RAG_API_Testing_Assets/      # Test verification screenshots from Swagger UI
    ├── 01_successful_pdf_upload.png
    ├── 02_empty_question_400.png
    ├── 03_unsupported_file_400.png
    ├── 04_pdf_without_extractable_text_400.png
    ├── 05_covariance_question_200.png
    ├── 06_unknown_document_404.png
    ├── 07_large_pdf_upload_200.png
    └── 08_server_test_logs.png
```

---

## API Endpoints Reference

| Method | Endpoint | Description | Request | Status Codes |
|---|---|---|---|---|
| `GET` | `/` | API status check | None | `200 OK` |
| `GET` | `/health` | Service health status | None | `200 OK` |
| `POST` | `/upload` | Upload and process a PDF document | `multipart/form-data` (`file`) | `200 OK`, `400 Bad Request` |
| `POST` | `/ask` | Ask a question about an uploaded PDF | JSON: `{"document_id": "...", "question": "..."}` | `200 OK`, `400 Bad Request`, `404 Not Found`, `422 Unprocessable`, `502 Bad Gateway`, `503 Unavailable` |

---

## Implementation Details

### 1. Robust Input Validation
- **File Format Verification:** Restricts uploads strictly to `.pdf` extensions (`400 Bad Request`).
- **Empty File Protection:** Rejects empty files or zero-byte uploads.
- **Scanned / Image-only PDF Handling:** Detects PDFs with no extractable text layer and rejects them early with an informative error message.

### 2. Chunking & Heuristic Retrieval
- Splits extracted document text into manageable 1,000-character chunks while tracking original page numbers.
- Filters out non-informative English stop words (`what`, `is`, `the`, `explain`, etc.) to isolate high-value search terms.
- Implements **overview-intent boosting**: Automatically awards relevance bonuses to introductory pages (pages $\le 3$) when queries ask for summaries or general document overviews.
- Dynamically selects up to 4 top-ranking chunks to assemble concise prompt context.

### 3. Context Grounding & Citation
- Enforces strict system instructions instructing Gemini to answer **only** using the supplied PDF excerpts.
- Returns a structured payload including the generated `answer` and a sorted list of `source_pages` enabling verifiable citation.

---

## Setup & Running

### 1. Environment Configuration
Create a `.env` file inside the `Day 17` directory with your Gemini API key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn pymupdf python-dotenv google-genai pydantic
```

### 3. Run the Development Server
Launch the server with live reload:
```bash
uvicorn main:app --reload
```

The service will start at `http://127.0.0.1:8000`.

### 4. Interactive Documentation
Explore and test the API directly using the interactive Swagger UI:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Testing & Validation Summary

The API underwent testing across valid workflows and edge-case error scenarios:

| Test ID | Scenario | Expected / Observed Status | Result |
|:---:|---|:---:|:---:|
| **T01** | Valid PDF upload (`Covariance and Correlation.pdf`) | `200 OK` | **Passed** (16 pages, 2,478 chars indexed) |
| **T02** | Empty or whitespace-only question | `400 Bad Request` | **Passed** (Rejected with clear message) |
| **T03** | Unsupported file format upload | `400 Bad Request` | **Passed** (`Only PDF files are supported`) |
| **T04** | PDF with no extractable text | `400 Bad Request` | **Passed** (`No extractable text found`) |
| **T05** | Question answering with citation | `200 OK` | **Passed** (Answer returned with pages 1, 3, 4, 8) |
| **T06** | Querying a non-existent document ID | `404 Not Found` | **Passed** (`Document not found`) |
| **T07** | Large multi-page PDF (`155 pages`) | `200 OK` | **Passed** (36,903 chars processed) |

*Full test breakdown, logs, and screenshot evidence are documented in [RAG_API_Testing_Report.md](RAG_API_Testing_Report.md).*

---

## Future Enhancements

Key architectural improvements planned for production readiness:
1. **Semantic Vector Search:** Transition from keyword-overlap ranking to semantic embeddings using ChromaDB or FAISS.
2. **Persistent Document Storage:** Move beyond in-memory caching to persistent disk/database storage with UUIDs.
3. **OCR Integration:** Add Tesseract / PyMuPDF OCR fallbacks to support scanned documents.
4. **Resilience & Rate Limiting:** Implement client request timeouts, retry backoffs, and upload payload size guards.

*Detailed improvement proposals are outlined in [Improvement_Suggestions.md](Improvement_Suggestions.md).*
