from flask import Flask, render_template, request, jsonify, session, redirect
import os

from resume_processing.pdf_extractor import extract_text_from_pdf
from resume_processing.ocr_handler import extract_text_with_ocr
from resume_processing.text_cleaner import clean_text

from nlp_extraction.entity_extractor import extract_entities
from nlp_extraction.skill_extractor import extract_skills
from nlp_extraction.experience_parser import parse_experience

from deet_profile.profile_builder import build_profile
from deet_profile.profile_schema import ProfileSchema

from analytics.role_matcher import match_roles, get_role_breakdown
from analytics.skill_gap import compute_skill_gap
from analytics.completeness_score import compute_completeness

from utils.validators import validate_pdf
from utils.helpers import format_file_size

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "deet-dev-secret")


# ── Page routes ──────────────────────────────────────────────────────────────

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/preview")
def preview():
    profile = session.get("profile")
    if not profile:
        return redirect("/upload")
    return render_template("preview.html", profile=profile)

@app.route("/dashboard")
def dashboard():
    profile = session.get("profile")
    if not profile:
        return redirect("/upload")
    analytics = session.get("analytics", {})
    return render_template("dashboard.html", profile=profile, analytics=analytics)


# ── API routes ────────────────────────────────────────────────────────────────

@app.route("/api/upload", methods=["POST"])
def api_upload():
    """Receive PDF, extract and return structured profile data."""
    if "resume" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["resume"]

    valid, err = validate_pdf(file)
    if not valid:
        return jsonify({"error": err}), 400

    # Try direct extraction, fall back to OCR
    raw_text = extract_text_from_pdf(file)
    if not raw_text or len(raw_text.strip()) < 50:
        file.seek(0)
        raw_text = extract_text_with_ocr(file)

    cleaned    = clean_text(raw_text)
    entities   = extract_entities(cleaned)
    skills     = extract_skills(cleaned)
    experience = parse_experience(cleaned)
    profile    = build_profile(entities, skills, experience)

    session["profile"]  = profile
    session["raw_text"] = cleaned

    return jsonify({"success": True, "profile": profile})


@app.route("/api/submit-profile", methods=["POST"])
def api_submit_profile():
    """Accept edited profile, compute analytics, store in session."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    schema = ProfileSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 422

    profile       = data
    role_matches  = match_roles(profile["skills"])
    best_role     = max(role_matches, key=lambda r: r["score"])
    completeness  = compute_completeness(profile)
    skill_gap     = compute_skill_gap(profile["skills"], best_role["role"])
    breakdown     = get_role_breakdown(best_role["role"], profile["skills"])

    analytics = {
        "completeness": completeness,
        "role_matches": role_matches,
        "best_role":    best_role,
        "skill_gap":    skill_gap,
        "breakdown":    breakdown,
    }

    session["profile"]   = profile
    session["analytics"] = analytics

    return jsonify({"success": True, "analytics": analytics})


@app.route("/api/role-analysis", methods=["POST"])
def api_role_analysis():
    """Return gap + breakdown for a chosen role (dropdown change)."""
    data   = request.get_json()
    role   = data.get("role", "")
    skills = data.get("skills", session.get("profile", {}).get("skills", []))

    gap       = compute_skill_gap(skills, role)
    breakdown = get_role_breakdown(role, skills)

    return jsonify({"gap": gap, "breakdown": breakdown})


if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
