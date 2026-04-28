import json
from pathlib import Path

from validation import validate_dataset


def generate_review_summary(validation_result: dict) -> str:
    dataset = validation_result["dataset_name"]
    decision = validation_result["decision"]
    score = validation_result["readiness_score"]
    issues = validation_result["issues"]

    if decision == "GO":
        return (
            f"{dataset} passed intake checks with a readiness score of {score}/100. "
            "The dataset is ready for downstream workflow use."
        )

    summary = (
        f"{dataset} requires review before onboarding.\n"
        f"Decision: {decision}\n"
        f"Readiness Score: {score}/100\n\n"
        "Issues found:\n"
    )

    for issue in issues:
        summary += f"- {issue['severity'].upper()}: {issue['type']}"

        if "column" in issue:
            summary += f" on column {issue['column']}"

        if "details" in issue:
            summary += f": {issue['details']}"

        summary += "\n"

    if decision == "GO_WITH_WARNINGS":
        summary += "\nRecommended Action: Proceed with monitoring and assign owners for warnings."
    else:
        summary += "\nRecommended Action: Block onboarding until remediation is complete."

    return summary


def main():
    base_path = Path(__file__).resolve().parents[1]

    with open(base_path / "input" / "dataset_profile.json") as f:
        dataset_profile = json.load(f)

    with open(base_path / "input" / "expected_output.json") as f:
        expected_output = json.load(f)

    validation_result = validate_dataset(dataset_profile, expected_output)
    summary = generate_review_summary(validation_result)

    print(json.dumps(validation_result, indent=2))
    print("\nAI-style review summary:")
    print(summary)


if __name__ == "__main__":
    main()
