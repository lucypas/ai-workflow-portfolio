import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from validators import validate_schema, validate_null_rates, validate_business_rules


def test_schema_validation_flags_missing_columns():
    dataset_profile = {"columns": ["customer_id"]}
    expected_contract = {
        "required_columns": ["customer_id", "event_timestamp"],
        "required_schema_version": "1.0.0"
    }

    issues = validate_schema(dataset_profile, expected_contract)
    assert len(issues) == 2


def test_null_rate_validation_flags_high_null_rate():
    dataset_profile = {
        "null_rates": {"customer_id": 0.10}
    }
    expected_contract = {
        "critical_columns": ["customer_id"],
        "max_null_rate_critical": 0.05
    }

    issues = validate_null_rates(dataset_profile, expected_contract)
    assert len(issues) == 1
    assert issues[0]["severity"] == "high"


def test_business_rule_validation_passes():
    dataset_profile = {"row_count": 200000}
    business_rules = {
        "rules": [
            {
                "name": "Minimum row count",
                "field": "row_count",
                "operator": ">=",
                "value": 100000,
                "severity": "high"
            }
        ]
    }

    issues = validate_business_rules(dataset_profile, business_rules)
    assert issues == []
