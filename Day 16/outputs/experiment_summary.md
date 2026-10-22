# Chunk Size Experiment Summary

**Question:** How does Python organize its documentation to help developers move from learning basic syntax to exploring advanced language features and standard-library modules?

| Chunk size | Total chunks | Best distance | Average distance (top 3) | Top source |
| --- | --- | --- | --- | --- |
| 200 | 40 | 0.2445 | 0.2685 | python.txt |
| 400 | 17 | 0.2489 | 0.2674 | python.txt |
| 700 | 10 | 0.258 | 0.2883 | python.txt |

Lower distance means a closer match. Distances come from different chunk sets, so read the differences as a rough guide, not proof that one size is best.

Embedding model: nomic-embed-text. Answer model: qwen2.5:3b.