# Sample Prompt Tests

| Test | Technique | Input | Expected check |
|---|---|---|---|
| 1 | Zero-shot | Explain supervised learning to a beginner | Clear definition and relevant example |
| 2 | Few-shot | Classify short feedback as Positive, Neutral or Negative using supplied examples | Follows labels and examples; does not invent labels |
| 3 | Role + Context | Explain a database index to a first-year student | Appropriate depth and vocabulary |
| 4 | Structured Output | Extract name, date and status from a supplied paragraph as JSON | Valid structure; missing fields handled explicitly |
| 5 | Stepwise Task Breakdown | Create a study plan from supplied subjects and available hours | Practical sequence; no invented availability |

## Evaluation dimensions
Score each response from 1 (poor) to 5 (strong) for relevance, factual accuracy, completeness, format compliance and uncertainty handling. Verify facts separately; a high prompt-quality score is not proof that an answer is true.
