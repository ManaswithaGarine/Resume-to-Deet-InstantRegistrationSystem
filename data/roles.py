"""Role definitions with required skills and weights."""

ROLES = {
    "ML Engineer": {
        "required_skills": {
            "Python":1.0,"Machine Learning":1.0,"TensorFlow":0.9,
            "PyTorch":0.9,"MLOps":0.8,"Docker":0.7,
            "SQL":0.6,"Statistics":0.8,"Deep Learning":0.9,
        },
        "description": "Build and deploy ML models at scale.",
        "icon": "🤖",
    },
    "Data Analyst": {
        "required_skills": {
            "SQL":1.0,"Excel":0.9,"Python":0.8,"Power BI":0.8,
            "Tableau":0.7,"Statistics":0.9,"R":0.6,"Data Visualization":0.8,
        },
        "description": "Transform raw data into business insights.",
        "icon": "📊",
    },
    "Data Scientist": {
        "required_skills": {
            "Python":1.0,"Statistics":1.0,"Machine Learning":0.9,
            "SQL":0.8,"R":0.7,"Spark":0.7,"Deep Learning":0.8,
        },
        "description": "Discover patterns and build predictive models.",
        "icon": "🔬",
    },
    "Backend Developer": {
        "required_skills": {
            "Python":0.8,"Java":0.8,"Node.js":0.9,"REST APIs":0.9,
            "PostgreSQL":0.8,"Docker":0.8,"SQL":0.7,
        },
        "description": "Design and maintain server-side systems.",
        "icon": "⚙️",
    },
    "Frontend Developer": {
        "required_skills": {
            "HTML":1.0,"CSS":1.0,"JavaScript":1.0,"React":0.9,"TypeScript":0.8,
        },
        "description": "Build beautiful, performant user interfaces.",
        "icon": "🎨",
    },
    "Full Stack Developer": {
        "required_skills": {
            "HTML":0.8,"CSS":0.8,"JavaScript":0.9,"React":0.8,
            "Node.js":0.8,"Python":0.7,"PostgreSQL":0.7,"Docker":0.7,
        },
        "description": "Own the entire web stack from UI to database.",
        "icon": "🌐",
    },
}
