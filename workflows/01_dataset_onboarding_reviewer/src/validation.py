"""Dataset onboarding validation logic."""


def validate_dataset(dataset_profile: dict, expected_output: dict) -> dict:
    """Validate dataset readiness against expected onboarding rules."""
    issues = []

    columns = set(dataset_profile.get("columns", []))
    required_columns = set(expected_output.get("required_columns", []))

    missing_columns = required_columns - columns
    if missing_columns:
        issues.append({
            "type": "missing_columns",
            "severity": "high",
            "details": sorted(list(missing_columns))
        })

    max_null_rate = expected_output.get("max_null_rate", 0.05)
    for column, null_rate in dataset_profile.get("null_rates", {}).items():
        if column in required_columns and null_rate > max_null_rate:
            issues.append({
                "type": "high_null_rate",
                "severity": "medium",
                "column": column,
                "null_rate": null_rate,
                "threshold": max_null_rate
            })

    freshness_hours = dataset_profile.get("freshness_hours")
    max_freshness_hours = expected_output.get("max_freshness_hours", 24)

    if freshness_hours is not None and freshness_hours > max_freshness_hours:
        issues.append({
            "type": "stale_dataset",
            "severity": "medium",
            "freshness_hours": freshness_hours,
            "threshold": max_freshness_hours
        })

    status = "approved" if not issues else "needs_review"

    return {
        "dataset_name": dataset_profile.get("dataset_name"),
        "status": status,
        "issues": issues,
        "issue_count": len(issues)
    }
