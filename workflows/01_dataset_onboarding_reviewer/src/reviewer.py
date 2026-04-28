"""Runnable dataset onboarding reviewer."""

import json
from pathlib import Path

from validation import validate_dataset


def generate_review_summary(validation_result: dict) -> str:
    """Generate an executive-readable dataset onboarding summary."""
    dataset = validation_result["dataset_name"]
    status = validation_result["status"]
    issues = validation_result["issues"]

    if status == "approved":
        return f"{dataset} passed onboarding checks and is ready for downstream workflow use."

    summary = f"{dataset} requires review before onboarding.\n\nIssues found:\n"
    for issue in issues:
        summary += f"- {issue['severity'].upper()}: {issue['type']}"

        if "column" in issue:
            summary += f" on column {issue['column']}"

        if "details" in issue:
            summary += f": {issue['details']}"

        summary += "\n"

    return summary


def main() -> None:
    base_path = Path(__file__).resolve().parents[1]

    with open(base_path / "input" / "dataset_profile.json", encoding="utf-8") as f:
        dataset_profile = json.load(f)

    with open(base_path / "input" / "expected_output.json", encoding="utf-8") as f:
        expected_output = json.load(f)

    validation_result = validate_dataset(dataset_profile, expected_output)
    summary = generate_review_summary(validation_result)

    print(json.dumps(validation_result, indent=2))
    print("\nAI-style review summary:")
    print(summary)


if __name__ == "__main__":
    main()
