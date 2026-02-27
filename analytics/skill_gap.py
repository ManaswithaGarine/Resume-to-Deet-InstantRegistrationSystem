"""Compute the skill gap between candidate and a target role."""
from data.roles import ROLES
from data.skills_courses import SKILL_COURSES

def compute_skill_gap(candidate_skills: list, role: str) -> dict:
    """
    Returns:
        {
          "missing":   list of str,
          "severity":  "low" | "moderate" | "high",
          "courses":   list of course dicts for missing skills,
        }
    """
    candidate_set = {s.lower() for s in candidate_skills}
    role_data     = ROLES.get(role, {})
    required      = role_data.get("required_skills", {})

    missing = [
        skill for skill in required
        if skill.lower() not in candidate_set
    ]

    # Weight-based severity
    missing_weight = sum(required[s] for s in missing)
    total_weight   = sum(required.values()) or 1
    ratio          = missing_weight / total_weight

    if ratio < 0.25:
        severity = "low"
    elif ratio < 0.55:
        severity = "moderate"
    else:
        severity = "high"

    courses = [
        SKILL_COURSES[s] for s in missing if s in SKILL_COURSES
    ][:4]

    return {
        "missing":  missing,
        "severity": severity,
        "courses":  courses,
    }
