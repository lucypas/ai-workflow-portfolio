import json
from pathlib import Path

from validators import run_all_validations
from scoring import calculate_readiness_score, assign_readiness_status
from recommendations import generate_recommendations
from audit import build_audit_record, write_audit_record


def load_json(path: Path) -> dict:
    with open(path, "r") as file:
        return json.load(file)


def run_workflow() -> dict:
    base_path = Path(__file__).resolve().parents[1]

    dataset_profile = load_json(base_path / "input" / "dataset_profile.json")
    expected_contract = load_json(base_path / "input" / "expected_contract.json")
    business_rules = load_json(base_path / "input" / "business_rules.json")

    validation_results = run_all_validations(
        dataset_profile=dataset_profile,
        expected_contract=expected_contract,
        business_rules=business_rules
    )

    readiness_score = calculate_readiness_score(validation_results)
    status = assign_readiness_status(readiness_score)
    recommendations = generate_recommendations(validation_results, readiness_score, status)

    audit_record = build_audit_record(
        dataset_profile=dataset_profile,
        validation_results=validation_results,
        readiness_score=readiness_score,
        status=status,
        recommendations=recommendations
    )

    audit_path = write_audit_record(audit_record, base_path / "output")

    print("AI Dataset Readiness Orchestrator")
    print("=" * 40)
    print(f"Dataset: {audit_record['dataset_name']}")
    print(f"Owner: {audit_record['owner']}")
    print(f"Readiness Score: {readiness_score}")
    print(f"Status: {status}")
    print(f"Issue Count: {audit_record['issue_count']}")
    print("\nRecommendations:")
    for recommendation in recommendations:
        print(f"- {recommendation}")

    print(f"\nAudit log written to: {audit_path}")

    return audit_record


if __name__ == "__main__":
    run_workflow()
