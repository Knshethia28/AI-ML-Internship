# Prompt Engineering Workbench — Day 26 POC

A small Streamlit proof of concept for constructing structured prompts using common prompt-engineering techniques. It supports zero-shot, few-shot, role/context, structured-output and stepwise task-breakdown approaches.

## What works without an API key
- Enter a task, audience, context, output format and constraints.
- Build a reusable prompt.
- Inspect and download the generated prompt.
- Review a prompt-testing checklist.

## Optional live LLM response
The app can send the generated prompt to Google's Gemini API when a valid API key is supplied. The API call is optional; the prompt builder itself does not require a key.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   `pip install -r requirements.txt`

5. Start the app:

   `streamlit run app.py`

6. To enable live responses, enter a Gemini API key in the sidebar. Alternatively, set `GEMINI_API_KEY` as an environment variable before starting the app.

## Example test
- Task: Explain photosynthesis.
- Audience: A class 8 student.
- Context: No additional context.
- Technique: Zero-shot.
- Output: One paragraph and three bullet points.
- Constraints: Use simple language; do not exceed 120 words.

Then change the technique to Structured Output and ask for JSON with `definition`, `inputs` and `outputs` fields.

## Scope and limitations
This POC demonstrates prompt construction and optional API-based generation. It does not independently verify generated facts, guarantee model accuracy, or provide production-grade authentication, logging, privacy controls or safety monitoring. Do not submit confidential or personal information to an external model without approval.

## Files
- `app.py` — Streamlit application
- `requirements.txt` — dependencies
- `.env.example` — environment-variable example
