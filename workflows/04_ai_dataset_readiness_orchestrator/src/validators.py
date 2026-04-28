def validate_schema(dataset_profile: dict, expected_contract: dict) -> list:
    issues = []

    actual_columns = set(dataset_profile.get("columns", []))
    required_columns = set(expected_contract.get("required_columns", []))

    missing_columns = sorted(required_columns - actual_columns)

    if missing_columns:
        issues.append({
            "type": "schema_validation",
            "severity": "critical",
            "message": "Dataset is missing required columns.",
            "details": missing_columns
        })

    if dataset_profile.get("schema_version") != expected_contract.get("required_schema_version"):
        issues.append({
            "type": "schema_version",
            "severity": "medium",
            "message": "Dataset schema version does not match expected contract.",
            "expected": expected_contract.get("required_schema_version"),
            "actual": dataset_profile.get("schema_version")
        })

    return issues


def validate_null_rates(dataset_profile: dict, expected_contract: dict) -> list:
    issues = []

    critical_columns = expected_contract.get("critical_columns", [])
    max_null_rate = expected_contract.get("max_null_rate_critical", 0.05)
    null_rates = dataset_profile.get("null_rates", {})

    for column in critical_columns:
        null_rate = null_rates.get(column)

        if null_rate is None:
            issues.append({
                "type": "null_rate_validation",
                "severity": "high",
                "message": f"No null-rate metadata was provided for critical column: {column}",
                "column": column
            })
        elif null_rate > max_null_rate:
            issues.append({
                "type": "null_rate_validation",
                "severity": "high",
                "message": f"Critical column exceeds allowed null-rate threshold: {column}",
                "column": column,
                "null_rate": null_rate,
                "threshold": max_null_rate
            })

    return issues


def validate_business_rules(dataset_profile: dict, business_rules: dict) -> list:
    issues = []

    for rule in business_rules.get("rules", []):
        field = rule["field"]
        operator = rule["operator"]
        expected_value = rule["value"]
        actual_value = dataset_profile.get(field)

        passed = False

        if operator == ">=":
            passed = actual_value >= expected_value
        elif operator == "<=":
            passed = actual_value <= expected_value
        elif operator == "==":
            passed = actual_value == expected_value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

        if not passed:
            issues.append({
                "type": "business_rule_validation",
                "severity": rule.get("severity", "medium"),
                "message": f"Business rule failed: {rule['name']}",
                "field": field,
                "expected": f"{operator} {expected_value}",
                "actual": actual_value
            })

    return issues


def run_all_validations(dataset_profile: dict, expected_contract: dict, business_rules: dict) -> dict:
    issues = []
    issues.extend(validate_schema(dataset_profile, expected_contract))
    issues.extend(validate_null_rates(dataset_profile, expected_contract))
    issues.extend(validate_business_rules(dataset_profile, business_rules))

    return {
        "dataset_name": dataset_profile.get("dataset_name"),
        "owner": dataset_profile.get("owner"),
        "source_system": dataset_profile.get("source_system"),
        "issues": issues,
        "issue_count": len(issues)
    }
