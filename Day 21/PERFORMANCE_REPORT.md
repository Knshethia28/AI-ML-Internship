# Day 21 — Performance Benchmark Report

## Objective
Compare the original synchronous PDF Q&A API with the Day 21 asynchronous, versioned API for sequential and concurrent requests, and document the outcome.

## Environment and test inputs
- Operating system: Windows (PowerShell)
- Original API: `http://127.0.0.1:8000` — Day 17 synchronous implementation
- Async API: `http://127.0.0.1:8001` — Day 21 implementation, API version `1.1.0`
- PDF used: `Module 4-Fundamentals of Neural Network.pdf`
- Question used: `What is an Activation Function?`
- Requests per test: 3
- Gemini model configured: `gemini-3.8-flash`
- Test date: 28 October 2026

## Performance comparison — latest comparable run

| API version | Test mode | Attempted | Successful | Successful-request average | Concurrent batch wall time |
|---|---|---:|---:|---:|---:|
| Day 17 synchronous | Sequential | 3 | 0 | N/A | N/A |
| Day 21 asynchronous v1 | Sequential | 3 | 0 | N/A | N/A |
| Day 17 synchronous | Concurrent | 3 | 0 | N/A | 0.404 s |
| Day 21 asynchronous v1 | Concurrent | 3 | 0 | N/A | 0.394 s |

**Important:** The timings above are client-observed timings for failed requests, not successful answer-generation latency. They must not be interpreted as proof of a performance improvement. A percentage improvement is therefore **not reported**.

### Request-level output recorded

| API | Test mode | Request durations / outcomes |
|---|---|---|
| Day 17 synchronous | Sequential | 0.483 s / 502; 0.355 s / 502; 0.413 s / 502 |
| Day 17 synchronous | Concurrent | 0.402 s / 502; 0.386 s / 502; 0.403 s / 502 |
| Day 21 asynchronous v1 | Sequential | 0.414 s / 502; 0.391 s / 502; 0.307 s / 502 |
| Day 21 asynchronous v1 | Concurrent | 0.391 s / 502; 0.394 s / 502; 0.389 s / 502 |

## Findings
- The PDF upload endpoint returned `200 OK`, confirming that the upload succeeded.
- The question-answering requests failed for both APIs, returning `502 Bad Gateway`.
- Diagnostic logging exposed the underlying Gemini error: `429 RESOURCE_EXHAUSTED`. Google's response stated that the free-tier daily generation-request quota for `gemini-3.8-flash` had been exceeded, with a quota value of 20 requests per day for the reported metric.
- The Day 21 API's `502` response is the application's wrapper around the upstream Gemini quota error; it is not evidence by itself that the async implementation is defective.
- Since neither API returned successful answers in the latest comparable run, successful-request averages cannot be calculated and the benchmark does not establish whether the async version improves performance under successful load.

## Conclusion
The Day 21 implementation and benchmark script were prepared, and both APIs were exercised. However, a valid performance comparison remains **inconclusive** because Gemini generation requests were blocked by the daily free-tier quota. A conclusive benchmark requires rerunning the same tests after quota availability returns (or with an authorized model/project with available quota), then comparing successful sequential and concurrent results. No performance improvement is claimed from the failed-request timings.
