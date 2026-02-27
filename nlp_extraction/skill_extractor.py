"""
Match resume text against a known skills vocabulary.
"""
import re
from data.roles import ROLES

# Build master skill vocabulary from all roles
SKILL_VOCAB = set()
for role_data in ROLES.values():
    SKILL_VOCAB.update(role_data["required_skills"].keys())

# Additional common skills not tied to a specific role
EXTRA_SKILLS = {
    "Python","Java","JavaScript","TypeScript","C++","C#","Go","Rust","Kotlin",
    "HTML","CSS","SQL","NoSQL","Git","Linux","AWS","Azure","GCP",
    "Machine Learning","Deep Learning","NLP","Computer Vision","OpenCV",
    "Pandas","NumPy","Matplotlib","Seaborn","Scikit-learn",
    "Teamwork","Leadership","Communication","Problem Solving","Presentation",
    "Agile","Scrum","Project Management",
}
SKILL_VOCAB.update(EXTRA_SKILLS)

def extract_skills(text: str) -> list[str]:
    """
    Case-insensitive substring search for each skill in the vocabulary.
    Returns a deduplicated list of found skills.
    """
    found = []
    text_lower = text.lower()
    for skill in sorted(SKILL_VOCAB):
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found
