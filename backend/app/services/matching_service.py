"""
Matching Service — Phase 3
Responsable de la comparaison fine entre un candidat et une offre.
LangGraph l'appelle via matching_nodes.py — ce service ne connaît pas LangGraph.
"""
from typing import Any


def compare_skills(candidate_skills: list[str], job_skills: list[str], required_skills: list[str]) -> dict:
    """
    Compares candidate skills against job requirements.
    Supports semantic matching by lowercasing and normalizing skill names.
    Returns matched/missing/bonus skills and a score.
    """
    def normalize(s: str) -> str:
        return s.lower().strip().replace("-", " ").replace("_", " ").replace(".", "")

    c_normalized = {normalize(s): s for s in candidate_skills}
    j_required_normalized = {normalize(s): s for s in required_skills}
    j_all_normalized = {normalize(s): s for s in job_skills}

    matched = [orig for norm, orig in j_required_normalized.items() if norm in c_normalized]
    missing = [orig for norm, orig in j_required_normalized.items() if norm not in c_normalized]
    bonus = [orig for norm, orig in c_normalized.items() if norm not in j_all_normalized]

    skill_score = (len(matched) / len(j_required_normalized) * 100) if j_required_normalized else 100.0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "bonus_skills": bonus[:5],   # top 5 bonus skills
        "skill_score": round(skill_score, 2),
    }


def compare_experience(candidate_years: int | None, job_required_years: int | None) -> dict:
    """
    Compares years of experience, returns a score and a gap.
    """
    c_years = candidate_years or 0
    j_years = job_required_years or 0

    if j_years == 0:
        return {"experience_score": 100.0, "experience_gap": 0}

    score = min(100.0, (c_years / j_years) * 100)
    gap = max(0, j_years - c_years)
    return {"experience_score": round(score, 2), "experience_gap": gap}


def compare_education(candidate_education: list | None, job_education_level: str | None) -> dict:
    """
    Simple heuristic match on education level.
    """
    LEVELS = {
        "bac": 1, "bac+2": 2, "bts": 2, "dut": 2, "deust": 2,
        "bac+3": 3, "bachelor": 3, "licence": 3,
        "bac+4": 4, "master 1": 4,
        "bac+5": 5, "master": 5, "master 2": 5, "ingénieur": 5, "mba": 5,
        "doctorat": 6, "phd": 6,
    }

    def extract_level(text: str) -> int:
        t = text.lower()
        for key, val in sorted(LEVELS.items(), key=lambda x: -x[1]):
            if key in t:
                return val
        return 0

    if not job_education_level:
        return {"education_score": 100.0}

    job_level_value = extract_level(job_education_level)
    if job_level_value == 0:
        return {"education_score": 100.0}

    candidate_max_level = 0
    for edu in (candidate_education or []):
        lvl = extract_level(str(edu))
        candidate_max_level = max(candidate_max_level, lvl)

    score = min(100.0, (candidate_max_level / job_level_value) * 100)
    return {"education_score": round(score, 2)}


def compare_certifications(candidate_certs: list | None, job_certs: list | None) -> dict:
    """
    Checks if candidate holds required certifications.
    """
    if not job_certs:
        return {"certification_score": 100.0, "matched_certifications": [], "missing_certifications": []}

    def normalize(s: str) -> str:
        return s.lower().strip()

    c_set = {normalize(c) for c in (candidate_certs or [])}
    matched = [c for c in job_certs if normalize(c) in c_set]
    missing = [c for c in job_certs if normalize(c) not in c_set]
    score = (len(matched) / len(job_certs) * 100) if job_certs else 100.0

    return {
        "certification_score": round(score, 2),
        "matched_certifications": matched,
        "missing_certifications": missing,
    }


def run_full_comparison(
    candidate_data: dict[str, Any],
    job_data: dict[str, Any],
    candidate_skills: list[str],
    job_skills: list[str],
    job_required_skills: list[str],
) -> dict[str, Any]:
    """
    Master comparison function. Calls all comparison sub-functions and returns a unified gaps dict.
    This is the single entry point called by matching_nodes.py.
    """
    skills_result = compare_skills(candidate_skills, job_skills, job_required_skills)
    exp_result = compare_experience(
        candidate_data.get("experience_years"),
        job_data.get("experience_years")
    )
    edu_result = compare_education(
        candidate_data.get("education"),
        job_data.get("education_level")
    )
    cert_result = compare_certifications(
        candidate_data.get("certifications"),
        job_data.get("certifications")
    )

    return {**skills_result, **exp_result, **edu_result, **cert_result}
