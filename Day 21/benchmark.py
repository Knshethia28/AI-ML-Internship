import asyncio
import statistics
import time
from pathlib import Path
import httpx

SERVERS = [("Synchronous original", "http://127.0.0.1:8000", "/upload", "/ask"),
           ("Asynchronous v1", "http://127.0.0.1:8001", "/api/v1/upload", "/api/v1/ask")]
REPEATS = 3

async def upload(client, base, endpoint, path):
    with open(path, "rb") as f:
        response = await client.post(base + endpoint, files={"file": (Path(path).name, f, "application/pdf")})
    response.raise_for_status()
    return response.json()["document_id"]

async def ask(client, base, endpoint, doc_id, question):
    start = time.perf_counter()
    try:
        r = await client.post(base + endpoint, json={"document_id": doc_id, "question": question})
        return {"seconds": time.perf_counter() - start, "status": r.status_code}
    except Exception as e:
        return {"seconds": time.perf_counter() - start, "status": type(e).__name__}

def show(label, results, batch=None):
    ok = [x["seconds"] for x in results if x["status"] == 200]
    print(f"\n{label}: {len(ok)}/{len(results)} successful")
    if ok:
        print(f"Average successful request: {statistics.mean(ok):.3f}s; min: {min(ok):.3f}s; max: {max(ok):.3f}s")
    if batch is not None:
        print(f"Concurrent batch wall time: {batch:.3f}s")
    print("Requests:", ", ".join(f"{x['seconds']:.3f}s / {x['status']}" for x in results))

async def main():
    path = input("Full path to a text-based PDF: ").strip().strip('"')
    question = input("Question answerable from that PDF: ").strip()
    if not Path(path).is_file() or not question:
        print("Check that the PDF path exists and the question is not empty.")
        return
    async with httpx.AsyncClient(timeout=120) as client:
        for label, base, upload_path, ask_path in SERVERS:
            (await client.get(base + "/health")).raise_for_status()
            doc_id = await upload(client, base, upload_path, path)
            sequential = [await ask(client, base, ask_path, doc_id, question) for _ in range(REPEATS)]
            show(f"{label} — sequential", sequential)
            start = time.perf_counter()
            concurrent = await asyncio.gather(*(ask(client, base, ask_path, doc_id, question) for _ in range(REPEATS)))
            show(f"{label} — concurrent", concurrent, time.perf_counter() - start)
    print("\nThis run makes 12 Gemini question-answer calls (6 per server). Results include model/network time; check statuses before comparing.")

if __name__ == "__main__":
    asyncio.run(main())
