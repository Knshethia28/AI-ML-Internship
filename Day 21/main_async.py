import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import pymupdf
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from google import genai

load_dotenv()
app = FastAPI(title="PDF Question Answering RAG API", description="Versioned asynchronous PDF question-answering API.", version="1.1.0")
api_v1 = APIRouter(prefix="/api/v1", tags=["API v1"])
api_key = os.getenv("GEMINI_API_KEY")
genai_client = genai.Client(api_key=api_key) if api_key else None
documents = {}
LOG_PATH = Path(__file__).with_name("background_tasks.log")

@app.middleware("http")
async def measure_request_time(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response

def get_genai_client():
    """Dependency provider for the configured Gemini client."""
    if genai_client is None:
        raise HTTPException(status_code=503, detail="Gemini API key is not configured.")
    return genai_client

def write_background_event(event: str, details: str):
    """Write a small audit event after the HTTP response is sent."""
    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write(f"{datetime.now(timezone.utc).isoformat()}\t{event}\t{details}\n")

class QuestionRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1, max_length=2000)

@app.get("/")
def home():
    return {"message": "RAG API is running", "status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy"}

def extract_pdf_pages(content: bytes):
    try:
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            pages = [{"page": i + 1, "text": page.get_text().strip()} for i, page in enumerate(pdf)]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or unreadable PDF file.")
    if not any(page["text"] for page in pages):
        raise HTTPException(status_code=400, detail="No extractable text found in this PDF.")
    return pages

@api_v1.post("/upload")
async def upload_pdf(background_tasks: BackgroundTasks, file: Annotated[UploadFile, File(...)]):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    pages = extract_pdf_pages(content)
    document_id = str(len(documents) + 1)
    documents[document_id] = {"filename": file.filename, "pages": pages}
    background_tasks.add_task(write_background_event, "pdf_uploaded", f"document_id={document_id}; filename={file.filename}; pages={len(pages)}")
    return {"message": "PDF uploaded successfully.", "document_id": document_id, "filename": file.filename,
            "pages_processed": len(pages), "characters_extracted": sum(len(p["text"]) for p in pages)}

def select_relevant_chunks(question: str, pages: list[dict]):
    chunks = []
    for page in pages:
        for start in range(0, len(page["text"]), 1000):
            text = page["text"][start:start + 1000]
            if text.strip():
                chunks.append({"page": page["page"], "text": text})
    if not chunks:
        raise HTTPException(status_code=422, detail="No document text is available for answering.")
    stop_words = {"what", "is", "the", "a", "an", "of", "in", "on", "and", "to", "for", "this", "that", "with", "does", "do", "can", "you", "tell", "me", "about", "it", "are", "was", "were", "be", "explain", "please", "from", "which", "who", "how", "why"}
    terms = {w.lower().strip(".,?!:;()[]{}\"'") for w in question.split()}
    terms = {w for w in terms if len(w) > 2 and w not in stop_words}
    q = question.lower()
    summary = any(p in q for p in ("main topic", "summarize", "summary", "overview", "what is this document about", "what is the document about"))
    ranked = []
    for chunk in chunks:
        score = sum(term in chunk["text"].lower() for term in terms)
        if summary and chunk["page"] <= 3:
            score += 3
        ranked.append((score, chunk))
    ranked.sort(key=lambda item: item[0], reverse=True)
    selected = [chunk for _, chunk in ranked[:4] if chunk["text"].strip()]
    return selected or chunks[:4]

@api_v1.post("/ask")
async def ask_question(request: QuestionRequest, client: Annotated[genai.Client, Depends(get_genai_client)]):
    document = documents.get(request.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found. Upload the PDF first.")
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    selected = select_relevant_chunks(question, document["pages"])
    context = "\n\n".join(f"Page {c['page']}: {c['text']}" for c in selected)
    if not context.strip():
        raise HTTPException(status_code=422, detail="Could not build context from the document.")
    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.8-flash",
            contents=("You answer questions about uploaded PDF documents. Use only the supplied document context. "
                      "If the answer is unsupported, clearly state that. Give a complete, concise answer.\n\n"
                      f"Document filename: {document['filename']}\n\nDocument context:\n{context}\n\nQuestion: {question}"),
            config={"max_output_tokens": 400},
        )
        answer = response.text
        if not answer or not answer.strip():
            raise HTTPException(status_code=502, detail="The model returned an empty answer. Please retry later.")
        return {"document_id": request.document_id, "question": question, "answer": answer.strip(),
                "source_pages": sorted({c["page"] for c in selected})}
    except HTTPException:
        raise

    except Exception as error:
        print(
            f"Gemini API error: {type(error).__name__}: {error}",
            flush=True,
        )
        raise HTTPException(
            status_code=502,
            detail=(
                f"Answer generation failed: {type(error).__name__}. "
                "The model may be temporarily unavailable."
            ),
        )

app.include_router(api_v1)
