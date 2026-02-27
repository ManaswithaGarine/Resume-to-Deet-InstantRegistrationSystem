"""Assemble a structured DEET profile dict from extracted components."""

def build_profile(entities: dict, skills: list, experience: dict) -> dict:
    """
    Combine outputs from entity_extractor, skill_extractor, and
    experience_parser into a single normalised profile dict.
    """
    education_entries = [
        {"title": line, "institution": ""}
        for line in experience.get("education", [])
    ]
    experience_entries = [
        {"role": line, "company": "", "year": ""}
        for line in experience.get("experience", [])
    ]

    return {
        "name":       entities.get("name", ""),
        "email":      entities.get("email", ""),
        "phone":      entities.get("phone", ""),
        "skills":     skills,
        "education":  education_entries,
        "experience": experience_entries,
    }
