import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from status_summary import calculate_project_health, calculate_delivery_score, classify_risk_level


def test_green_project_health():
    project = {
        "blocked_items": 0,
        "schedule_variance_days": 1,
        "open_risks": 2
    }

    assert calculate_project_health(project) == "Green"


def test_red_project_health_for_blockers():
    project = {
        "blocked_items": 5,
        "schedule_variance_days": 1,
        "open_risks": 2
    }

    assert calculate_project_health(project) == "Red"


def test_delivery_score_deducts_for_signals():
    project = {
        "blocked_items": 1,
        "schedule_variance_days": 5,
        "open_risks": 4
    }

    assert calculate_delivery_score(project) == 60


def test_medium_risk_level():
    project = {
        "blocked_items": 1,
        "schedule_variance_days": 5,
        "open_risks": 4
    }

    assert classify_risk_level(project) == "Medium"
