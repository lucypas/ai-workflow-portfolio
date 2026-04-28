"""Simple portfolio-safe RAG-style knowledge assistant."""

import json
import re
from pathlib import Path


def tokenize(text: str) -> set[str]:
    """Convert text into lowercase word tokens."""
    return set(re.findall(r"\b\w+\b", text.lower()))


def simple_retrieve(query: str, documents: list[dict], top_k: int = 2) -> list[dict]:
    """Retrieve the most relevant documents using simple token overlap."""
    query_terms = tokenize(query)
    scored_docs = []

    for doc in documents:
        content_terms = tokenize(doc["content"] + " " + doc["title"])
        score = len(query_terms.intersection(content_terms))

        scored_docs.append({
            "title": doc["title"],
            "content": doc["content"],
            "score": score
        })

    ranked = sorted(scored_docs, key=lambda x: x["score"], reverse=True)
    return [doc for doc in ranked if doc["score"] > 0][:top_k]


def generate_answer(query: str, retrieved_docs: list[dict]) -> str:
    """Generate an answer from retrieved knowledge base content."""
    if not retrieved_docs:
        return "I could not find relevant knowledge base content for this question."

    sources = ", ".join([doc["title"] for doc in retrieved_docs])

    answer = f"""
Question:
{query}

Answer:
Based on the available knowledge base, the workflow should consider:
"""

    for doc in retrieved_docs:
        answer += f"- {doc['content']}\n"

    answer += f"\nSources used: {sources}"
    return answer.strip()


def load_documents() -> list[dict]:
    """Load mock knowledge base documents."""
    base_path = Path(__file__).resolve().parents[1]
    with open(base_path / "input" / "knowledge_base.json", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    documents = load_documents()
    user_query = "What should we check before onboarding a dataset?"

    retrieved = simple_retrieve(user_query, documents)
    answer = generate_answer(user_query, retrieved)

    print(answer)


if __name__ == "__main__":
    main()
