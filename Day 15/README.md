# Day 15 – Exploring Pretrained AI Models with Hugging Face Transformers

## Overview

Day 15 explores the **Hugging Face Model Hub** and demonstrates how to leverage state-of-the-art pretrained transformer models for three distinct Natural Language Processing (NLP) tasks:
1. **Text Generation** (Instruction-tuned Large Language Model)
2. **Sentiment Analysis** (Transformer-based text classification)
3. **Text Summarization** (Sequence-to-sequence encoder-decoder model)

Each model was loaded, tested with custom inputs, evaluated on task-specific criteria, and benchmarked for inference latency.

---

## Files

| File | Description |
|------|-------------|
| `LLM_Comparison.ipynb` | Jupyter notebook documenting the Model Hub exploration, pipeline setup, inference execution, output evaluation, and comparative performance analysis |

---

## Models Explored

| Task | Model | Hugging Face Repository | Architecture Type |
|------|-------|-------------------------|-------------------|
| **Text Generation** | Qwen2.5-0.5B-Instruct | `Qwen/Qwen2.5-0.5B-Instruct` | Autoregressive Decoder LLM |
| **Sentiment Analysis** | Twitter-RoBERTa-Sentiment-Latest | `cardiffnlp/twitter-roberta-base-sentiment-latest` | RoBERTa Encoder Classifier |
| **Summarization** | FLAN-T5-Base | `google/flan-t5-base` | Sequence-to-Sequence (Seq2Seq) |

---

## Experiments & Observations

### Experiment 1: Text Generation
- **Model:** `Qwen2.5-0.5B-Instruct`
- **Input Prompt:** 
  > *"Explain three practical ways artificial intelligence can improve education. Use simple language and give one example for each."*
- **Generated Output:**
  > Produced a structured, well-articulated response breaking down practical applications:
  > 1. **Personalized Learning Paths:** Adapting learning pace and suggesting tailored resources (e.g., interactive exercises for struggling math students).
  > 2. **Adaptive Assessment Tools:** Dynamically adjusting test difficulty based on ongoing student performance.
- **Inference Time:** **54.54 seconds** (CPU runtime)
- **Evaluation:** High relevance and strong instruction-following, balanced against higher computational demands and generation latency.

---

### Experiment 2: Sentiment Analysis
- **Model:** `Twitter-RoBERTa-Sentiment-Latest`
- **Input Review:** 
  > *"The product quality is excellent, and the delivery was faster than expected."*
- **Predicted Class:** **`positive`**
- **Confidence Score:** **0.9846 (98.46%)**
- **Inference Time:** **0.16 seconds**
- **Evaluation:** Extremely fast and decisive classification; highly optimized for sentiment extraction with negligible latency.

---

### Experiment 3: Text Summarization
- **Model:** `FLAN-T5-Base`
- **Input Passage:** A 100-word paragraph detailing the benefits of AI in education (teacher support, personalized practice, feedback) alongside necessary precautions (privacy, accuracy, human guidance).
- **Generated Summary:**
  > *"Use human guidance to help students learn."*
- **Inference Time:** **1.53 seconds**
- **Evaluation:** Successfully identified a central theme with fast response time, though aggressive compression omitted secondary nuances (e.g., privacy and accuracy considerations).

---

## Comparative Analysis

| Task | Model | Output Summary | Inference Latency | Primary Strength |
|------|-------|----------------|:-----------------:|------------------|
| **Text Generation** | `Qwen2.5-0.5B-Instruct` | Multi-point explanatory response | ~54.5 s | Coherence & instruction following |
| **Sentiment Analysis** | `Twitter-RoBERTa-Sentiment-Latest` | `positive` (98.46% confidence) | ~0.16 s | High confidence & near-instant latency |
| **Summarization** | `FLAN-T5-Base` | Single-sentence abstractive summary | ~1.5 s | Rapid content synthesis |

---

## Key Takeaways

1. **Pretrained Efficiency:** Pretrained transformer pipelines enable zero-shot and few-shot capabilities across complex language tasks without training from scratch.
2. **Task-Specific Specialization:** Specialized encoder models (such as RoBERTa for classification) deliver orders-of-magnitude faster inference (~0.16s) compared to general-purpose generative LLMs (~54.5s on CPU).
3. **Critical Evaluation:** Generated outputs must be critically validated—concise summaries may miss context, and high confidence in classification does not eliminate edge-case errors.
4. **Resource Allocation:** Model selection requires balancing output depth against latency and memory footprint depending on deployment constraints.

---

## Tools & Libraries

- **Hugging Face Transformers** (`pipeline`, `AutoTokenizer`, `AutoModelForSeq2SeqLM`)
- **PyTorch** (`torch`)
- **SentencePiece** (Tokenizer backend)
- **Pandas** (Comparison metrics reporting)
- **Google Colab** (Cloud compute execution)

---

## Execution Note

This notebook was executed in **Google Colab** using cloud resources to download model weights and run inference efficiently without consuming local storage. All outputs, tokenizers, and benchmark metrics are preserved directly within the notebook file.
