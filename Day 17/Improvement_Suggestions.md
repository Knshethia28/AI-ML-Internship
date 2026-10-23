# RAG API Improvement Suggestions

## 1. Improve document retrieval

**Current limitation:** The API ranks fixed-size text chunks using keyword overlap. A question phrased differently from the source text may retrieve less relevant chunks.

**Suggestion:** Improve keyword scoring and heading awareness first. As a later enhancement, use semantic embeddings and vector similarity to retrieve passages based on meaning.

**Priority:** High, because retrieval quality directly affects answers.

## 2. Improve chunking and source attribution

**Current limitation:** Text is split into chunks of up to 1,000 characters without paragraph-aware boundaries or overlap. The returned page numbers identify selected chunks, but do not guarantee every listed page directly supports the answer.

**Suggestion:** Split text at paragraph or sentence boundaries, add modest chunk overlap, and return source excerpts or more precise references. Test source relevance using several questions before claiming reliable citations.

**Priority:** High.

## 3. Add upload and resource limits

**Current limitation:** The upload endpoint reads the entire file into memory and has no explicit upload-size or page-count limit. The tested 155-page PDF succeeded, but one successful test does not establish behavior for arbitrarily large files.

**Suggestion:** Set a maximum upload size and consider page-count, processing-time, and concurrency limits. Return a clear error when a limit is exceeded.

**Priority:** High.

## 4. Support scanned PDFs with OCR

**Current limitation:** PDFs with no extractable text are rejected with `No extractable text found in this PDF.` Scanned pages may contain text only as images.

**Suggestion:** Either document that the current version supports text-based PDFs only or add an optional OCR stage for image-based pages. Test OCR separately because it adds processing time and complexity.

**Priority:** Medium.

## 5. Persist uploaded documents

**Current limitation:** Documents are stored in an in-memory Python dictionary. They disappear when the server restarts, and IDs based on dictionary length can be reused.

**Suggestion:** Generate unique document IDs and store extracted text and metadata in persistent local storage. If vector retrieval is added later, persist its index or embeddings as well.

**Priority:** High if the API will be used beyond a short local session.

## 6. Strengthen model error handling

**Current limitation:** Gemini availability, quota limits, network errors, or empty responses can interrupt answer generation. The current code returns a `502` for caught generation errors but does not explicitly implement retries or request timeouts.

**Suggestion:** Add bounded retries for transient errors, suitable timeouts, clearer error messages, and structured logging. Never expose API keys in responses. Keep the key in `.env` and do not commit that file.

**Priority:** High.

## 7. Expand robustness tests

Consider adding these follow-up tests:

- A zero-byte file, separately from a PDF with no extractable text.
- A corrupted or malformed PDF.
- A password-protected PDF.
- A file that exceeds a configured upload limit.
- A question whose answer is absent from the document.
- A server restart followed by a question about a previously uploaded document, to demonstrate the current in-memory storage limitation.
- Repeated questions to observe answer consistency and model availability.

Record actual responses and status codes before marking these tests as passed.

## 8. Improve API documentation and setup

**Suggestion:** Keep `requirements.txt` accurate, document supported files and limitations, and add clear endpoint descriptions and response schemas. Document that uploaded documents currently remain available only while the server process retains its in-memory state.

## Recommended implementation order

1. Add upload-size limits and validate empty or malformed inputs.
2. Improve chunking, retrieval ranking, and source-page relevance.
3. Add timeouts and clearer handling of model-service failures.
4. Introduce persistent storage and unique document IDs.
5. Consider semantic retrieval and OCR as later enhancements.

These are proposed improvements, not features claimed to be implemented.
