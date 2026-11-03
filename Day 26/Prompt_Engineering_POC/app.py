import os
import json
import requests
import streamlit as st

st.set_page_config(page_title="Prompt Engineering Workbench", page_icon="🧩", layout="wide")
st.title("Prompt Engineering Workbench")
st.caption("Day 26 Proof of Concept • Build, compare and test structured prompts")

TECHNIQUES = {
    "Zero-shot": "Complete the task directly. Do not assume examples that were not provided.",
    "Few-shot": "Study the examples and follow their pattern consistently. If the examples conflict, explain the conflict.",
    "Role + Context": "Adopt the specified role and use the supplied context to tailor the response.",
    "Structured Output": "Return the answer using exactly the requested structure. Do not add text outside that structure.",
    "Stepwise Task Breakdown": "Solve the task in clear stages. Show only a concise explanation of the approach and the final result; do not reveal private chain-of-thought."
}

def build_prompt(task, context, audience, technique, output_format, constraints, examples):
    parts = [
        "ROLE\nYou are a careful, helpful AI assistant. Be accurate, clear and appropriately cautious.",
        f"TASK\n{task.strip()}",
        f"AUDIENCE\n{audience.strip() or 'General audience'}",
        f"CONTEXT\n{context.strip() or 'No additional context provided.'}",
        f"PROMPTING APPROACH\n{technique}: {TECHNIQUES[technique]}",
    ]
    if examples.strip() and technique == "Few-shot":
        parts.append("EXAMPLES\n" + examples.strip())
    parts.extend([
        f"OUTPUT FORMAT\n{output_format.strip() or 'Use clear headings and concise paragraphs.'}",
        f"CONSTRAINTS\n{constraints.strip() or 'Do not invent facts. State uncertainty when information is missing.'}",
        "RELIABILITY RULE\nSeparate facts from assumptions. If the provided information is insufficient, say what is missing rather than guessing."
    ])
    return "\n\n".join(parts)

def call_gemini(api_key, model, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        json={
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        },
        timeout=(10, 120)
    )

    response.raise_for_status()

    data = response.json()

    candidates = data.get("candidates", [])

    if not candidates:
        raise ValueError(
            f"Gemini returned no generated response. Details: {data}"
        )

    return candidates[0]["content"]["parts"][0]["text"]

with st.sidebar:
    st.header("LLM connection (optional)")
    api_key = st.text_input("Google Gemini API key", type="password",
                            value=os.getenv("GEMINI_API_KEY", ""))
    model = st.text_input("Gemini model", value="gemini-3.5-flash-lite")
    st.caption("Without an API key, the workbench still builds and lets you inspect/copy prompts. The live response feature requires internet access and a valid API key.")

left, right = st.columns([1, 1])
with left:
    task = st.text_area("Task / instruction", placeholder="e.g. Explain supervised learning to a first-year student.", height=110)
    audience = st.text_input("Target audience", value="Beginner student")
    context = st.text_area("Context / source material", placeholder="Paste relevant background, notes or approved source text here.", height=130)
    technique = st.selectbox("Prompting technique", list(TECHNIQUES.keys()))
    examples = st.text_area("Examples (used for Few-shot)", placeholder="Input: ...\nOutput: ...", height=100)
    output_format = st.text_input("Expected output format", value="Use a short introduction followed by 4 bullet points.")
    constraints = st.text_area("Constraints", value="Use simple language. Do not invent facts. If information is missing, state that clearly.", height=90)
    generate = st.button("Build prompt", type="primary", use_container_width=True)

with right:
    st.subheader("Generated prompt")
    if generate:
        if not task.strip():
            st.warning("Enter a task before building the prompt.")
            prompt = ""
        else:
            prompt = build_prompt(task, context, audience, technique, output_format, constraints, examples)
            st.session_state["prompt"] = prompt
    else:
        prompt = st.session_state.get("prompt", "")
    if prompt:
        st.code(prompt, language="text")
        st.download_button("Download prompt (.txt)", prompt, file_name="generated_prompt.txt")
        if st.button("Send prompt to Gemini"):
            if not api_key:
                st.error("Add a Gemini API key in the sidebar to use live generation.")
            else:
                try:
                    with st.spinner("Generating response..."):
                        answer = call_gemini(api_key, model, prompt)
                    st.session_state["answer"] = answer
                except requests.HTTPError as exc:
                    st.error(f"Gemini API request failed: {exc.response.status_code} — {exc.response.text[:500]}")
                except Exception as exc:
                    st.error(f"Could not generate a response: {exc}")
    if st.session_state.get("answer"):
        st.subheader("Model response")
        st.write(st.session_state["answer"])

st.divider()
st.subheader("Prompt testing checklist")
st.markdown("""
- **Relevance:** Does the response answer the actual task?
- **Accuracy:** Can important factual claims be verified?
- **Completeness:** Are all requested parts present?
- **Format:** Does the output follow the requested structure?
- **Uncertainty:** Does the model admit when the supplied context is insufficient?
- **Consistency:** Does the prompt behave acceptably on more than one test input?
""")
st.info("Responsible-use note: Do not paste confidential, personal or sensitive company data into an external model unless the service and data use have been approved.")
