# ShopEase Knowledge Base – Day 28 Code Review Notes

## Scope
Reviewed and improved `knowledge_base.py` and `tests/test_knowledge_base.py`.
The existing JSON knowledge-base format and the public function names were retained.

## Issues identified
1. `load_articles()` checked only that the JSON root was a list. Individual entries could be malformed or missing required fields.
2. `search_articles()` used substring matching, which could count a query term as a match inside a different word (for example, `order` inside `preorder`).
3. Negative search limits were not handled explicitly.

## Improvements made
1. Added per-article validation. Every article must be a JSON object containing non-empty string values for `id`, `title`, `content`, and `keywords`.
2. Added case-insensitive whole-word tokenization using Python's standard `re` module. Punctuation is ignored, but partial-word matches are avoided.
3. Preserved the existing minimum of two matching query words, ranking order, default limit, and list-of-article return format.
4. Added explicit handling for negative limits (`ValueError`) while retaining the existing zero-limit behavior (empty list).
5. Expanded the knowledge-base test suite to cover malformed article entries, invalid required fields, substring false matches, and negative limits.

## Verification
- Focused command: `python -m pytest -q tests/test_knowledge_base.py`
- Result: **17 passed**.
- The actual project JSON file loaded successfully with 4 articles.
- Sample searches returned the expected late-delivery and refund articles.
- A check for `order` against an article containing only `preorder` returned no match.

## Verification limitation
The complete test suite could not be collected in this execution environment because the `langgraph` dependency is not installed. The API and graph tests therefore remain unverified here. Run `python -m pip install -r requirements.txt` in the project's virtual environment, then `python -m pytest -v` to run the complete suite.

## Files changed
- `knowledge_base.py`
- `tests/test_knowledge_base.py`
