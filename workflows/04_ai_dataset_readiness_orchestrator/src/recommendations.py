def generate_recommendations(validation_results: dict, readiness_score: int, status: str) -> list:
    """Generate AI-style recommendations from validation results.

    This intentionally avoids calling a real LLM so the repo can run locally.
    In a production version, this layer could call an approved LLM endpoint.
    """
    recommendations = []

    issue_types = {issue["type"] for issue in validation_results.get("issues", [])}

    if "schema_validation" in issue_types:
        recommendations.append(
            "Resolve missing required columns before downstream AI or analytics use."
        )

    if "null_rate_validation" in issue_types:
        recommendations.append(
            "Review upstream data capture for critical fields with high or missing null-rate metadata."
        )

    if "business_rule_validation" in issue_types:
        recommendations.append(
            "Assign remediation owners for failed business rules and re-run validation after fixes."
        )

    if readiness_score >= 90:
        recommendations.append(
            "Dataset is ready for onboarding. Continue standard monitoring after release."
        )
    elif status == "approved_with_monitoring":
        recommendations.append(
            "Dataset can proceed with monitoring. Track quality metrics during initial production use."
        )
    elif status == "needs_remediation":
        recommendations.append(
            "Dataset should not be promoted until remediation actions are completed and revalidated."
        )
    else:
        recommendations.append(
            "Dataset should be blocked from production use until critical issues are resolved."
        )

    return recommendations
