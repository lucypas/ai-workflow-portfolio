def calculate_delivery_score(project: dict) -> int:
    """Calculate a 0-100 delivery score using delivery signals."""
    score = 100
    score -= project.get("blocked_items", 0) * 10
    score -= project.get("open_risks", 0) * 5
    score -= max(project.get("schedule_variance_days", 0), 0) * 2
    return max(score, 0)


def calculate_project_health(project: dict) -> str:
    """Classify program health using blockers, schedule variance, and risk volume."""
    score = calculate_delivery_score(project)

    if project.get("blocked_items", 0) > 3:
        return "Red"
    if project.get("schedule_variance_days", 0) > 10:
        return "Red"
    if score < 70:
        return "Red"
    if project.get("schedule_variance_days", 0) > 3 or project.get("open_risks", 0) > 5:
        return "Yellow"
    return "Green"


def classify_risk_level(project: dict) -> str:
    """Translate risk signals into a leadership-friendly risk level."""
    if project.get("blocked_items", 0) >= 4 or project.get("schedule_variance_days", 0) > 10:
        return "High"
    if project.get("open_risks", 0) > 5 or project.get("schedule_variance_days", 0) > 3:
        return "Medium"
    return "Low"


def recommend_action(health: str) -> str:
    if health == "Green":
        return "Continue standard delivery cadence and monitor dependencies."
    if health == "Yellow":
        return "Review risks in the next steering meeting and confirm mitigation owners."
    return "Escalate blockers, confirm executive decision points, and reset delivery timeline."


def generate_executive_summary(project: dict) -> str:
    health = calculate_project_health(project)
    delivery_score = calculate_delivery_score(project)
    risk_level = classify_risk_level(project)

    return f"""
Project: {project['project_name']}
Status: {health}
Delivery Score: {delivery_score}/100
Risk Level: {risk_level}

Executive Summary:
The {project['project_name']} initiative is currently rated {health}. 
The team has completed {project['completed_workstreams']} of {project['total_workstreams']} workstreams.

Key Delivery Signals:
- Open risks: {project['open_risks']}
- Blocked items: {project['blocked_items']}
- Schedule variance: {project['schedule_variance_days']} days

Recommended Action:
{recommend_action(health)}
""".strip()


if __name__ == "__main__":
    sample_project = {
        "project_name": "AI Dataset Onboarding Automation",
        "completed_workstreams": 3,
        "total_workstreams": 5,
        "open_risks": 4,
        "blocked_items": 1,
        "schedule_variance_days": 5
    }

    print(generate_executive_summary(sample_project))
