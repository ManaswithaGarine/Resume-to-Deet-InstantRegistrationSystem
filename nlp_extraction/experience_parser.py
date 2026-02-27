"""
Parse education and experience sections from resume text.
"""
import re

EDU_KEYWORDS   = ["bachelor", "master", "phd", "b.tech", "m.tech", "bsc", "msc",
                   "b.e", "m.e", "diploma", "degree", "university", "college",
                   "institute", "school"]
EXP_KEYWORDS   = ["intern", "engineer", "developer", "analyst", "manager",
                   "consultant", "associate", "lead", "coordinator", "officer"]

def parse_experience(text: str) -> dict:
    """
    Returns:
        {
          "education":  list of str,
          "experience": list of str,
        }
    """
    lines      = [l.strip() for l in text.splitlines() if l.strip()]
    education  = []
    experience = []

    for line in lines:
        ll = line.lower()
        if any(kw in ll for kw in EDU_KEYWORDS) and len(line) < 200:
            education.append(line)
        elif any(kw in ll for kw in EXP_KEYWORDS) and len(line) < 200:
            experience.append(line)

    # Deduplicate while preserving order
    seen = set()
    education  = [x for x in education  if not (x in seen or seen.add(x))]
    seen = set()
    experience = [x for x in experience if not (x in seen or seen.add(x))]

    return {
        "education":  education[:6],
        "experience": experience[:6],
    }
