# Resume to DEET — Instant Registration

Upload a PDF resume and instantly get an auto-filled DEET jobseeker profile,
career analytics, skill gap analysis, and course recommendations.

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm   # optional, for NER
python app.py
```

Then open http://localhost:5000

## Flow

1. **Landing** `/` — hero + feature overview
2. **Upload** `/upload` — drag-and-drop PDF; auto-extracts profile via NLP
3. **Preview** `/preview` — review and edit the auto-filled profile
4. **Dashboard** `/dashboard` — career analytics, role match, skill gap, courses

## Project Structure

```
resume-to-deet/
├── app.py                     # Flask entry point + all routes
├── requirements.txt
├── data/
│   ├── roles.py               # Role definitions + required skills
│   └── skills_courses.py      # Skill → course recommendations
├── resume_processing/
│   ├── pdf_extractor.py       # pdfplumber text extraction
│   ├── ocr_handler.py         # Tesseract OCR fallback
│   └── text_cleaner.py        # Normalise raw text
├── nlp_extraction/
│   ├── entity_extractor.py    # Name / email / phone via regex
│   ├── skill_extractor.py     # Skill vocab matching
│   └── experience_parser.py   # Education & experience sections
├── deet_profile/
│   ├── profile_schema.py      # Marshmallow validation schema
│   └── profile_builder.py     # Assemble profile dict
├── analytics/
│   ├── role_matcher.py        # Score candidate vs all roles
│   ├── skill_gap.py           # Missing skills + severity
│   └── completeness_score.py  # Profile completeness %
├── utils/
│   ├── validators.py          # PDF size/type validation
│   └── helpers.py             # format_file_size etc.
├── static/
│   ├── css/style.css          # All styles
│   └── js/app.js              # All client-side logic
└── templates/
    ├── base.html              # Shared layout (nav, stepper)
    ├── landing.html
    ├── upload.html
    ├── preview.html
    └── dashboard.html
```
