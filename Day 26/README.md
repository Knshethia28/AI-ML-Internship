# Day 26 – Responsible AI & Prompt Engineering Workbench

## Overview

Day 26 focuses on two key aspects of applied Artificial Intelligence:
1. **Responsible AI Framework:** Principles, governance, and operational guardrails for safe, ethical, and transparent AI deployment (covering fairness, privacy, accuracy, human oversight, and liability case studies).
2. **Prompt Engineering Workbench (POC):** An interactive Streamlit application demonstrating core prompt-engineering patterns (zero-shot, few-shot, role-based prompting, structured outputs, and step-by-step task breakdown) with optional Google Gemini integration.

---

## Directory Structure

```text
Day 26/
├── README.md                          # Top-level directory overview
├── Responsible_AI.md                  # Comprehensive policy & guidelines for Responsible AI
├── Sources_and_Attribution.md         # Reference citations & case study attribution
└── Prompt_Engineering_POC/            # Streamlit-based Prompt Engineering Workbench
    ├── app.py                         # Streamlit application entry point
    ├── requirements.txt               # Dependencies (streamlit, google-genai, etc.)
    ├── .env.example                   # Environment variable template for Gemini API key
    ├── README.md                      # POC setup, usage guide, and testing instructions
    └── sample_test_cases.md           # Sample test scenarios across prompt techniques
```

---

## Files & Components

| Component | Description |
|---|---|
| [`Responsible_AI.md`](Responsible_AI.md) | Policy document detailing fairness, transparency, data privacy, hallucination prevention, risk assessment, and incident response |
| [`Sources_and_Attribution.md`](Sources_and_Attribution.md) | Source links and citations for case studies (including the Air Canada chatbot liability tribunal decision) |
| [`Prompt_Engineering_POC/app.py`](Prompt_Engineering_POC/app.py) | Interactive Streamlit workbench to build, inspect, download, and optionally evaluate structured prompts with Gemini |
| [`Prompt_Engineering_POC/sample_test_cases.md`](Prompt_Engineering_POC/sample_test_cases.md) | Structured test cases covering zero-shot, few-shot, and role-based prompt formats |
| [`Prompt_Engineering_POC/README.md`](Prompt_Engineering_POC/README.md) | Quickstart and local execution instructions for the Streamlit POC |

---

## Key Highlights

- **Responsible AI Principles:** Emphasizes fairness, explainability, security, human-in-the-loop validation, and legal accountability for automated customer-facing systems.
- **Prompt Engineering Techniques:** Hands-on workbench illustrating parameter control (temperature, max tokens), format constraints (JSON, Markdown), and few-shot exemplar injection.
- **Offline / Live Dual Mode:** The workbench operates fully offline for prompt construction and template generation, with optional live LLM inference when configured with a Gemini API key.

