"""Executive status summary workflow."""

import json
from pathlib import Path


def calculate_project_health(project: dict) -> str:
    """Calculate project health from delivery metrics."""
    if project["blocked_items"] > 3:
        return "Red"
    if project["schedule_variance_days"] > 10:
        return "Red"
    if project["schedule_variance_days"] > 3 or project["open_risks"] > 5:
        return "Yellow"
    return "Green"


def recommend_action(health: str) -> str:
    """Recommend action based on project health."""
    if health == "Green":
        return "Continue standard delivery cadence and monitor dependencies."
    if health == "Yellow":
        return "Review risks in the next steering meeting and confirm mitigation owners."
    return "Escalate blockers, confirm executive decision points, and reset delivery timeline."


def generate_executive_summary(project: dict) -> str:
    """Generate an executive-ready status summary."""
    health = calculate_project_health(project)

    return f"""
Project: {project['project_name']}
Status: {health}

Executive Summary:
The {project['project_name']} initiative is currently rated {health}.
The team has completed {project['completed_workstreams']} of {project['total_workstreams']} workstreams.

Key Risks:
- Open risks: {project['open_risks']}
- Blocked items: {project['blocked_items']}
- Schedule variance: {project['schedule_variance_days']} days

Recommended Action:
{recommend_action(health)}
""".strip()


def main() -> None:
    base_path = Path(__file__).resolve().parents[1]

    with open(base_path / "input" / "project_status.json", encoding="utf-8") as f:
        project = json.load(f)

    print(generate_executive_summary(project))


if __name__ == "__main__":
    main()
