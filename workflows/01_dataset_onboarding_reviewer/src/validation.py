def validate_dataset(dataset_profile: dict, expected_output: dict) -> dict:
    """Validate a dataset profile against an expected contract."""
    issues = []

    columns = set(dataset_profile.get("columns", []))
    required_columns = set(expected_output.get("required_columns", []))

    missing_columns = sorted(required_columns - columns)
    if missing_columns:
        issues.append({
            "type": "missing_columns",
            "severity": "high",
            "message": "Dataset is missing required columns.",
            "details": missing_columns
        })

    max_null_rate = expected_output.get("max_null_rate", 0.05)
    null_rates = dataset_profile.get("null_rates", {})

    for column in required_columns:
        null_rate = null_rates.get(column)

        if null_rate is None:
            issues.append({
                "type": "missing_null_rate_metadata",
                "severity": "medium",
                "message": f"Null-rate metadata is missing for required column: {column}",
                "column": column
            })
        elif null_rate > max_null_rate:
            issues.append({
                "type": "high_null_rate",
                "severity": "medium",
                "message": f"Required column exceeds maximum null-rate threshold: {column}",
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
            "message": "Dataset freshness exceeds SLA.",
            "freshness_hours": freshness_hours,
            "threshold": max_freshness_hours
        })

    readiness_score = calculate_readiness_score(issues)
    decision = assign_onboarding_decision(readiness_score, len(issues))

    return {
        "dataset_name": dataset_profile.get("dataset_name"),
        "readiness_score": readiness_score,
        "decision": decision,
        "status": "approved" if decision == "GO" else "needs_review",
        "issues": issues,
        "issue_count": len(issues)
    }


def calculate_readiness_score(issues: list) -> int:
    """Calculate a simple readiness score from validation issues."""
    score = 100

    penalties = {
        "critical": 30,
        "high": 20,
        "medium": 10,
        "low": 5
    }

    for issue in issues:
        score -= penalties.get(issue.get("severity", "low"), 5)

    return max(score, 0)


def assign_onboarding_decision(readiness_score: int, issue_count: int) -> str:
    """Assign a data onboarding decision based on readiness and issue volume."""
    if readiness_score >= 90 and issue_count == 0:
        return "GO"
    if readiness_score >= 75:
        return "GO_WITH_WARNINGS"
    return "NO_GO"
