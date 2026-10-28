# Day 21 API Documentation — Async Version

Base URL: `http://127.0.0.1:8001` · Swagger UI: `/docs` · Version: `1.1.0`

## Existing utility routes
- `GET /` — API status.
- `GET /health` — health check.

## Version 1 routes
### `POST /api/v1/upload`
Send `multipart/form-data` with a `file` field containing a readable, non-empty PDF. Returns a `document_id`, filename, pages processed and extracted character count. Errors: `400` for invalid/empty PDFs or PDFs without extractable text. A background task records the upload in `background_tasks.log` after the response.

### `POST /api/v1/ask`
Send JSON:
```json
{"document_id":"1","question":"What is the main topic of this document?"}
```
Returns the answer and `source_pages`. Errors: `400` blank question; `404` unknown document; `422` no usable context; `502` model failure/empty answer; `503` missing Gemini API key.

## Day 21 concepts implemented
- Async/await: `/api/v1/ask` awaits `client.aio.models.generate_content(...)`.
- Middleware: adds `X-Process-Time` response header with server-side duration.
- Background task: logs successful PDF uploads to a local text file.
- Dependency injection: `Depends(get_genai_client)` provides the Gemini client.
- Validation: Pydantic field limits plus PDF validation.
- API versioning: new endpoints are under `/api/v1/`.

Timing in `X-Process-Time` is server-side processing time. `benchmark.py` measures client-observed duration, which also includes network and Gemini response time. Example responses in this document are illustrative, not benchmark evidence.
