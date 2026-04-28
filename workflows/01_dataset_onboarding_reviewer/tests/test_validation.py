import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from validation import validate_dataset, calculate_readiness_score, assign_onboarding_decision


def test_dataset_passes_validation():
    dataset_profile = {
        "dataset_name": "test_dataset",
        "columns": ["customer_id", "event_timestamp", "channel", "event_type"],
        "null_rates": {
            "customer_id": 0.0,
            "event_timestamp": 0.01,
            "channel": 0.02,
            "event_type": 0.01
        },
        "freshness_hours": 3
    }

    expected_output = {
        "required_columns": ["customer_id", "event_timestamp", "channel", "event_type"],
        "max_null_rate": 0.05,
        "max_freshness_hours": 24
    }

    result = validate_dataset(dataset_profile, expected_output)

    assert result["status"] == "approved"
    assert result["decision"] == "GO"
    assert result["readiness_score"] == 100
    assert result["issue_count"] == 0


def test_dataset_flags_missing_column():
    dataset_profile = {
        "dataset_name": "test_dataset",
        "columns": ["customer_id", "channel"],
        "null_rates": {
            "customer_id": 0.0,
            "channel": 0.01
        },
        "freshness_hours": 3
    }

    expected_output = {
        "required_columns": ["customer_id", "event_timestamp", "channel"],
        "max_null_rate": 0.05,
        "max_freshness_hours": 24
    }

    result = validate_dataset(dataset_profile, expected_output)

    assert result["status"] == "needs_review"
    assert result["decision"] == "NO_GO"
    assert result["issue_count"] >= 1


def test_readiness_score_deducts_by_severity():
    issues = [
        {"severity": "high"},
        {"severity": "medium"}
    ]

    assert calculate_readiness_score(issues) == 70


def test_assign_onboarding_decision_no_go():
    assert assign_onboarding_decision(60, 3) == "NO_GO"
