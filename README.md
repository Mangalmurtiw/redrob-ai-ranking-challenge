# Redrob AI Ranking Challenge

## Overview

This project solves the Intelligent Candidate Discovery & Ranking Challenge by ranking candidates for the role of Senior AI Engineer at Redrob.

The solution focuses on understanding recruiter intent rather than simple keyword matching.

---

## Ranking Strategy

The final score is computed using a hybrid scoring framework:

### 1. Experience Fit
- Preferred range: 5–9 years
- Senior-level candidates receive higher weight

### 2. Retrieval & Ranking Experience
Strong signals for:
- Search systems
- Recommendation systems
- Retrieval pipelines
- Embeddings
- Vector databases
- Ranking infrastructure

### 3. AI / ML Relevance
Signals include:
- NLP
- LLMs
- RAG
- LoRA
- Machine Learning
- Deep Learning

### 4. Career History Analysis
Uses:
- Job titles
- Work descriptions
- Domain relevance
- Product-oriented experience

### 5. Behavioral Signals
Uses Redrob platform signals:
- Recruiter response rate
- Interview completion rate
- Open-to-work status
- Recruiter saves
- GitHub activity
- Relocation willingness

### 6. Deterministic Tie Breaking
Candidate IDs are used as a stable tie-breaker to ensure validator compliance.

---

## Files

- `rank_candidates_v4.py` – Final ranking pipeline
- `submission.csv` – Final generated submission
- `validate_submission.py` – Official validator
- `candidate_schema.json` – Dataset schema

---

## Run

Place `candidates.jsonl` in the project root and execute:

```bash
python rank_candidates_v4.py
```

---

## Output

Generates:

```text
submission.csv
```

which passes the official validation script.

---

## Note

Dataset files are intentionally excluded from this repository.
