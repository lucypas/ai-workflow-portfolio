import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CURRENT_DIR / "src"))

from status_summary import calculate_project_health, recommend_action  # noqa: E402


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


def test_yellow_recommendation():
    assert "steering meeting" in recommend_action("Yellow")
