"""Score how complete the DEET profile is (0-100)."""

WEIGHTS = {
    "name":       22,
    "email":      20,
    "phone":      15,
    "education":  20,
    "experience": 10,
    "skills":     13,
}

def compute_completeness(profile: dict) -> int:
    score = 0
    if profile.get("name"):       score += WEIGHTS["name"]
    if profile.get("email"):      score += WEIGHTS["email"]
    if profile.get("phone"):      score += WEIGHTS["phone"]
    if profile.get("education"):  score += WEIGHTS["education"]
    if profile.get("experience"): score += WEIGHTS["experience"]
    if profile.get("skills"):     score += WEIGHTS["skills"]
    return min(score, 100)
