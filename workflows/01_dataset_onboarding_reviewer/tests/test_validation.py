import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CURRENT_DIR / "src"))

from validation import validate_dataset  # noqa: E402


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
    assert result["issue_count"] == 1
    assert result["issues"][0]["type"] == "missing_columns"
