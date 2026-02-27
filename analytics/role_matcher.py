"""Score the candidate profile against every role."""
from data.roles import ROLES

def match_roles(candidate_skills: list) -> list:
    """
    Returns a list of {role, score, icon, description} sorted by score desc.
    Score = weighted overlap between candidate skills and role required skills.
    """
    candidate_set = {s.lower() for s in candidate_skills}
    results = []

    for role, data in ROLES.items():
        required    = data["required_skills"]
        total_weight = sum(required.values())
        matched      = sum(
            w for skill, w in required.items()
            if skill.lower() in candidate_set
        )
        score = round((matched / total_weight) * 100) if total_weight else 0
        results.append({
            "role":        role,
            "score":       score,
            "icon":        data["icon"],
            "description": data["description"],
        })

    return sorted(results, key=lambda r: r["score"], reverse=True)


def get_role_breakdown(role: str, candidate_skills: list) -> list:
    """
    Returns per-skill-category match percentages for a specific role.
    Used to render the horizontal match bars in the dashboard.
    """
    candidate_set = {s.lower() for s in candidate_skills}
    role_data = ROLES.get(role, {})
    required  = role_data.get("required_skills", {})

    # Group into 4 representative categories
    items = list(required.items())
    breakdown = []
    for skill, weight in items[:4]:
        matched = 1 if skill.lower() in candidate_set else 0
        # Scale: if matched, score = weight*100, else 0
        score = round(weight * 100) if matched else round(weight * 30)
        breakdown.append({"name": skill, "pct": score})

    return breakdown
