import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CURRENT_DIR / "src"))

from rag_assistant import generate_answer, simple_retrieve  # noqa: E402


DOCUMENTS = [
    {
        "title": "Dataset Onboarding Standard",
        "content": "All datasets must include owner, source system, refresh frequency, required columns, and data quality rules."
    },
    {
        "title": "Executive Reporting Standard",
        "content": "Status reports should include project health, risks, blockers, milestones, dependencies, and recommended actions."
    }
]


def test_retrieve_dataset_onboarding_content():
    results = simple_retrieve("dataset onboarding required columns", DOCUMENTS)

    assert len(results) > 0
    assert results[0]["score"] > 0
    assert "Dataset" in results[0]["title"]


def test_generate_answer_no_results():
    answer = generate_answer("unknown topic", [])

    assert "could not find" in answer
