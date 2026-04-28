import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from rag_assistant import simple_retrieve, generate_answer, DOCUMENTS


def test_retrieve_dataset_onboarding_content():
    results = simple_retrieve("dataset onboarding required columns", DOCUMENTS)

    assert len(results) > 0
    assert results[0]["score"] > 0
    assert "confidence" in results[0]


def test_generate_answer_includes_sources():
    results = simple_retrieve("executive reporting risks blockers", DOCUMENTS)
    answer = generate_answer("What should an executive report include?", results)

    assert "Sources used" in answer


def test_generate_answer_fallback_when_no_results():
    answer = generate_answer("How do I repair a car engine?", [])

    assert "could not find relevant" in answer
