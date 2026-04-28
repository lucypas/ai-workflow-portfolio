import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from scoring import calculate_readiness_score, assign_readiness_status


def test_score_with_no_issues_is_100():
    result = calculate_readiness_score({"issues": []})
    assert result == 100


def test_score_deducts_for_high_issue():
    result = calculate_readiness_score({
        "issues": [{"severity": "high"}]
    })
    assert result == 80


def test_status_approved():
    assert assign_readiness_status(95) == "approved"


def test_status_blocked():
    assert assign_readiness_status(40) == "blocked"
