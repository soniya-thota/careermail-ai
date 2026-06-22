import re
from collections import Counter

ROLE_SKILLS = {
    "ai_ml": ["python", "pytorch", "tensorflow", "scikit-learn", "machine learning", "deep learning", "llm", "rag", "vector database", "nlp", "computer vision", "model evaluation", "mlops"],
    "software": ["python", "java", "javascript", "react", "fastapi", "api", "backend", "postgresql", "system design", "docker", "git", "testing"],
    "data": ["sql", "python", "spark", "kafka", "airflow", "aws", "etl", "elt", "data modeling", "data pipeline", "postgresql", "delta lake"],
}

STOPWORDS = set("the and for with from this that your you are have has will can our we they role using into across data software engineer engineering experience work team build building".split())


def normalize(text: str) -> str:
    return (text or "").lower()


def extract_keywords(text: str, limit: int = 12):
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+.#-]{2,}", normalize(text))
    words = [w for w in words if w not in STOPWORDS]
    counts = Counter(words)
    return [word for word, _ in counts.most_common(limit)]


def analyze_resume_match(resume: str, job_description: str):
    resume_text = normalize(resume)
    jd_text = normalize(job_description)
    all_skills = sorted(set(sum(ROLE_SKILLS.values(), [])))

    matched = [skill for skill in all_skills if skill in resume_text and skill in jd_text]
    missing = [skill for skill in all_skills if skill in jd_text and skill not in resume_text]
    jd_keywords = extract_keywords(job_description, limit=15)

    score = min(95, 45 + len(matched) * 6 - len(missing) * 3)
    score = max(20, score)

    role_focus = "AI/ML Engineer"
    if any(skill in jd_text for skill in ["spark", "kafka", "airflow", "etl", "data pipeline"]):
        role_focus = "AI/Data Engineer"
    if any(skill in jd_text for skill in ["react", "backend", "api", "java", "system design"]):
        role_focus = "Software Engineer / AI Product Engineer"

    bullets = [
        "Built AI-powered and data-driven applications using Python, FastAPI, React, and PostgreSQL to transform unstructured data into actionable insights.",
        "Developed machine learning workflows with Python, PyTorch, Scikit-learn, Pandas, and NumPy for preprocessing, training, evaluation, and analysis.",
        "Implemented scalable data engineering pipelines using Spark, Kafka, Airflow, AWS, and SQL to support batch and streaming analytics use cases.",
    ]

    outreach = (
        "Hi [Name], I came across the role and found it closely aligned with my background in "
        "AI/ML, software engineering, and data-driven applications. I recently completed my MS in "
        "Computer Science & Engineering (AI/ML Track) from the University at Buffalo and have hands-on "
        "experience with Python, FastAPI, React, PyTorch, SQL, AWS, and data pipelines. I’d appreciate "
        "the opportunity to connect and learn more."
    )

    return {
        "match_score": score,
        "role_focus": role_focus,
        "matched_skills": matched[:12],
        "missing_skills": missing[:10],
        "job_keywords": jd_keywords,
        "recommended_resume_bullets": bullets,
        "recruiter_outreach": outreach,
        "next_actions": [
            "Add 2-3 keywords from the job description into project bullets where truthful.",
            "Prepare one story each for AI/ML, software engineering, and data pipeline experience.",
            "If the role mentions LLM/RAG, highlight your RAG Job Assistant and CareerMail AI projects.",
        ],
    }
