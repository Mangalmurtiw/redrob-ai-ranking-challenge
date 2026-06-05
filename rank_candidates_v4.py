import json
import pandas as pd

TOP_K = 100

GOOD_TITLES = {
    "ml engineer",
    "machine learning engineer",
    "ai engineer",
    "search engineer",
    "recommendation systems engineer",
    "recommendation engineer",
    "applied ml engineer",
    "nlp engineer",
    "senior nlp engineer",
    "data scientist",
    "senior data scientist"
}

BAD_TITLES = {
    "marketing manager",
    "hr manager",
    "accountant",
    "customer support",
    "content writer",
    "sales executive"
}

RETRIEVAL_TERMS = [
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "matching",
    "relevance",
    "embedding",
    "embeddings",
    "vector",
    "semantic search",
    "rerank",
    "reranking",
    "bm25",
    "ndcg",
    "mrr",
    "map",
    "a/b testing",
    "ab testing"
]

VECTOR_SKILLS = {
    "milvus",
    "pinecone",
    "faiss",
    "qdrant",
    "weaviate",
    "elasticsearch",
    "opensearch"
}

AI_SKILLS = {
    "nlp",
    "llm",
    "lora",
    "qlora",
    "bert",
    "rag",
    "fine-tuning llms",
    "transformers"
}


def score_candidate(candidate):
    score = 0

    profile = candidate.get("profile", {})

    # Experience
    exp = profile.get("years_of_experience", 0)

    if 5 <= exp <= 9:
        score += 25
    elif 4 <= exp <= 11:
        score += 15

    # Title weight reduced (V4)
    title = profile.get("current_title", "").lower()

    if title in GOOD_TITLES:
        score += 10

    if title in BAD_TITLES:
        score -= 20

    # Retrieval / ranking evidence
    retrieval_score = 0

    for job in candidate.get("career_history", []):
        text = (
            job.get("title", "") + " " +
            job.get("description", "")
        ).lower()

        for term in RETRIEVAL_TERMS:
            if term in text:
                retrieval_score += 4

    score += min(retrieval_score, 50)

    # Skills
    for skill in candidate.get("skills", []):
        name = skill.get("name", "").lower()

        if name in VECTOR_SKILLS:
            score += 3

        if name in AI_SKILLS:
            score += 2

    # Redrob signals
    rr = candidate.get("redrob_signals", {})

    if rr.get("open_to_work_flag", False):
        score += 10

    score += rr.get("recruiter_response_rate", 0) * 15
    score += rr.get("interview_completion_rate", 0) * 10

    score += min(
        rr.get("saved_by_recruiters_30d", 0) * 2,
        20
    )

    score += min(
        rr.get("search_appearance_30d", 0) / 50,
        10
    )

    github = rr.get("github_activity_score", -1)

    if github > 0:
        score += github / 10

    # Notice period bonus
    notice = rr.get("notice_period_days", 180)

    if notice <= 30:
        score += 10
    elif notice <= 60:
        score += 5

    # Relocation bonus
    if rr.get("willing_to_relocate", False):
        score += 5

    return round(score, 4)


rows = []

with open("candidates.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)

        score = score_candidate(candidate)

        rows.append({
            "candidate_id": candidate["candidate_id"],
            "raw_score": score,
            "title": candidate["profile"]["current_title"]
        })

# Sort with validator-compatible tie breaking
rows = sorted(
    rows,
    key=lambda x: (-x["raw_score"], x["candidate_id"])
)

rows = rows[:TOP_K]

max_score = rows[0]["raw_score"]

output = []

for rank, row in enumerate(rows, start=1):
    output.append({
        "candidate_id": row["candidate_id"],
        "rank": rank,
        "score": round(row["raw_score"] / max_score, 6),
        "reasoning": (
            f"{row['title']}; "
            f"retrieval/ranking experience; "
            f"strong behavioral signals"
        )
    })

submission = pd.DataFrame(output)

submission.to_csv(
    "submission.csv",
    index=False
)

print("submission.csv generated")
print(submission.head(10))
