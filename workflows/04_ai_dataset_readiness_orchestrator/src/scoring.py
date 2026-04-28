def calculate_readiness_score(validation_results: dict) -> int:
    """Calculate a 0-100 readiness score based on validation issues."""
    score = 100

    severity_penalties = {
        "critical": 30,
        "high": 20,
        "medium": 10,
        "low": 5
    }

    for issue in validation_results.get("issues", []):
        score -= severity_penalties.get(issue.get("severity", "low"), 5)

    return max(score, 0)


def assign_readiness_status(score: int) -> str:
    """Map readiness score to delivery status."""
    if score >= 90:
        return "approved"
    if score >= 75:
        return "approved_with_monitoring"
    if score >= 50:
        return "needs_remediation"
    return "blocked"
