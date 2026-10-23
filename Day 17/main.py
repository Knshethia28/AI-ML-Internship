
import os
import pymupdf  # fitz

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from google import genai

load_dotenv()

app = FastAPI(
    title="PDF Question Answering RAG API",
    description="Upload a PDF and ask questions about its content.",
    version="1.0.0",
)

# Configure Gemini using the API key stored in .env
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# Temporary in-memory storage for uploaded documents
documents = {}


class QuestionRequest(BaseModel):
    document_id: str
    question: str


@app.get("/")
def home():
    return {
        "message": "RAG API is running",
        "status": "success",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate the file name and extension
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # Extract text from every PDF page
    try:
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            pages = [
                {
                    "page": page_number + 1,
                    "text": page.get_text().strip(),
                }
                for page_number, page in enumerate(pdf)
            ]
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or unreadable PDF file.",
        )

    # Reject scanned PDFs or files without extractable text
    if not any(page["text"] for page in pages):
        raise HTTPException(
            status_code=400,
            detail="No extractable text found in this PDF.",
        )

    # Generate a unique document ID
    document_id = str(len(documents) + 1)

    documents[document_id] = {
        "filename": file.filename,
        "pages": pages,
    }

    return {
        "message": "PDF uploaded successfully.",
        "document_id": document_id,
        "filename": file.filename,
        "pages_processed": len(pages),
        "characters_extracted": sum(
            len(page["text"]) for page in pages
        ),
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    # Check API configuration
    if not client:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured.",
        )

    # Check whether the requested document exists
    document = documents.get(request.document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found. Upload the PDF first.",
        )

    # Validate the question
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    # Split extracted text into chunks of up to 1000 characters
    chunks = []

    for page in document["pages"]:
        text = page["text"]

        for start in range(0, len(text), 1000):
            chunk_text = text[start:start + 1000]

            if chunk_text.strip():
                chunks.append({
                    "page": page["page"],
                    "text": chunk_text,
                })

    if not chunks:
        raise HTTPException(
            status_code=422,
            detail="No document text is available for answering.",
        )

    # Remove common words that provide little retrieval value
    stop_words = {
        "what", "is", "the", "a", "an", "of", "in", "on",
        "and", "to", "for", "this", "that", "with", "does",
        "do", "can", "you", "tell", "me", "about", "it",
        "are", "was", "were", "be", "explain", "please",
        "from", "which", "who", "how", "why"
    }

    terms = {
        word.lower().strip(".,?!:;()[]{}\"'")
        for word in request.question.split()
    }

    terms = {
        word for word in terms
        if len(word) > 2 and word not in stop_words
    }

    # Detect questions asking for a general overview
    question_lower = request.question.lower()

    summary_question = any(
        phrase in question_lower
        for phrase in [
            "main topic",
            "summarize",
            "summary",
            "overview",
            "what is this document about",
            "what is the document about",
        ]
    )

    # Score chunks according to keyword overlap
    ranked = []

    for chunk in chunks:
        text_lower = chunk["text"].lower()

        score = sum(
            term in text_lower
            for term in terms
        )

        # Favor introductory pages for overview questions
        if summary_question and chunk["page"] <= 3:
            score += 3

        ranked.append((score, chunk))

    # Sort the highest-scoring chunks first
    ranked.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    # Select up to four relevant chunks
    selected = [
        chunk
        for score, chunk in ranked[:4]
        if chunk["text"].strip()
    ]

    # If no keywords matched, use the first available chunks
    if not selected:
        selected = chunks[:4]

    # Build context and retain page numbers
    context = "\n\n".join(
        f"Page {chunk['page']}: {chunk['text']}"
        for chunk in selected
    )

    if not context.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not build context from the document.",
        )

    # Generate an answer using Gemini
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "You answer questions about uploaded PDF documents. "
                "Use the filename and supplied context to understand "
                "the document's topic. Answer using only the supplied "
                "document information. If the answer is not supported "
                "by the context, clearly state that. Give a complete, "
                "concise answer.\n\n"
                f"Document filename: {document['filename']}\n\n"
                f"Document context:\n{context}\n\n"
                f"Question: {request.question}"
            ),
            config={"max_output_tokens": 400},
        )

        answer = response.text

        if not answer or not answer.strip():
            raise HTTPException(
                status_code=502,
                detail=(
                    "The model returned an empty answer. "
                    "Please retry later."
                ),
            )

        return {
            "document_id": request.document_id,
            "question": request.question,
            "answer": answer.strip(),
            "source_pages": sorted({
                chunk["page"] for chunk in selected
            }),
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=(
                f"Answer generation failed: {type(error).__name__}. "
                "The model may be temporarily unavailable."
            ),
        )
