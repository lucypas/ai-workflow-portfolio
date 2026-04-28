from datetime import datetime, timezone
import json
from pathlib import Path


def build_audit_record(dataset_profile: dict, validation_results: dict, readiness_score: int, status: str, recommendations: list) -> dict:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "workflow": "ai_dataset_readiness_orchestrator",
        "dataset_name": dataset_profile.get("dataset_name"),
        "owner": dataset_profile.get("owner"),
        "source_system": dataset_profile.get("source_system"),
        "readiness_score": readiness_score,
        "status": status,
        "issue_count": validation_results.get("issue_count"),
        "issues": validation_results.get("issues", []),
        "recommendations": recommendations
    }


def write_audit_record(audit_record: dict, output_path: Path) -> Path:
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / "dataset_readiness_audit.json"
    file_path.write_text(json.dumps(audit_record, indent=2))
    return file_path
