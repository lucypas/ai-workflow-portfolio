import json
from pathlib import Path


DOCUMENTS = [
    {
        "title": "Dataset Onboarding Standard",
        "content": "All datasets must include owner, source system, refresh frequency, required columns, and data quality rules."
    },
    {
        "title": "Data Quality Policy",
        "content": "Datasets should be checked for missing values, duplicate records, schema drift, and freshness before release."
    },
    {
        "title": "Executive Reporting Standard",
        "content": "Status reports should include project health, risks, blockers, milestones, dependencies, and recommended actions."
    }
]


def tokenize(text: str) -> set:
    """Simple tokenizer for portfolio-safe local retrieval."""
    normalized = (
        text.lower()
        .replace(",", "")
        .replace(".", "")
        .replace(":", "")
        .replace("?", "")
    )
    return set(normalized.split())


def simple_retrieve(query: str, documents: list, top_k: int = 2) -> list:
    """Retrieve and rank documents using simple term overlap."""
    query_terms = tokenize(query)
    scored_docs = []

    for doc in documents:
        content_terms = tokenize(doc["content"])
        title_terms = tokenize(doc["title"])

        content_score = len(query_terms.intersection(content_terms))
        title_score = len(query_terms.intersection(title_terms)) * 2
        score = content_score + title_score

        if score > 0:
            scored_docs.append({
                "title": doc["title"],
                "content": doc["content"],
                "score": score
            })

    ranked = sorted(scored_docs, key=lambda x: x["score"], reverse=True)
    total_score = sum(doc["score"] for doc in ranked) or 1

    for doc in ranked:
        doc["confidence"] = round(doc["score"] / total_score, 2)

    return ranked[:top_k]


def generate_answer(query: str, retrieved_docs: list, minimum_confidence: float = 0.20) -> str:
    if not retrieved_docs:
        return "I could not find relevant knowledge base content for this question."

    top_confidence = retrieved_docs[0].get("confidence", 0)

    if top_confidence < minimum_confidence:
        return (
            "I found weakly related content, but confidence is too low to provide a grounded answer. "
            "Please refine the question or add more knowledge base content."
        )

    sources = ", ".join([doc["title"] for doc in retrieved_docs])

    answer = f"""
Question:
{query}

Answer:
Based on the available knowledge base, the workflow should consider:
"""

    for doc in retrieved_docs:
        answer += f"- {doc['content']} (confidence: {doc['confidence']})\n"

    answer += f"\nSources used: {sources}"

    return answer.strip()


def load_knowledge_base(path: Path) -> list:
    with open(path, "r") as file:
        return json.load(file)


if __name__ == "__main__":
    base_path = Path(__file__).resolve().parents[1]
    knowledge_base_path = base_path / "input" / "knowledge_base.json"

    documents = load_knowledge_base(knowledge_base_path)
    user_query = "What should we check before onboarding a dataset?"

    retrieved = simple_retrieve(user_query, documents)
    answer = generate_answer(user_query, retrieved)

    print(answer)
