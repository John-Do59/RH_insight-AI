"""
Scoring Service — Phase 3
Responsable du calcul du score global, des sous-scores pondérés,
de l'explicabilité et de l'historisation.
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScoreBreakdown:
    """Structured, explainable score result."""
    vector_score: float = 0.0
    skill_score: float = 0.0
    experience_score: float = 0.0
    education_score: float = 0.0
    certification_score: float = 0.0
    github_score: float = 0.0
    llm_score: float = 0.0
    final_score: float = 0.0

    # Weights used
    weights_used: dict = field(default_factory=dict)

    # Sub-score explanations
    skills_label: str = ""
    experience_label: str = ""
    education_label: str = ""

    def to_dict(self) -> dict:
        return {
            "final_score": self.final_score,
            "sub_scores": {
                "semantic_similarity": round(self.vector_score, 1),
                "skills_match": round(self.skill_score, 1),
                "experience_match": round(self.experience_score, 1),
                "education_match": round(self.education_score, 1),
                "certification_match": round(self.certification_score, 1),
                "github_activity": round(self.github_score, 1),
                "llm_reasoning": round(self.llm_score, 1),
            },
            "weights": self.weights_used,
            "labels": {
                "skills": self.skills_label,
                "experience": self.experience_label,
                "education": self.education_label,
            }
        }


def compute_score(
    vector_score: float,
    skill_score: float,
    experience_score: float,
    education_score: float = 100.0,
    certification_score: float = 100.0,
    github_score: float = 0.0,
    llm_score: float = 50.0,
    experience_gap: int = 0,
    matched_skills: list = None,
    missing_skills: list = None,
    candidate_years: int = None,
    job_required_years: int = None,
) -> ScoreBreakdown:
    """
    Computes a weighted final score with explainable sub-scores.
    Weights are dynamic: GitHub weight is redistributed if no score available.

    Default weight distribution (sums to 1.0):
      - 30% semantic vector similarity
      - 25% skills match (required skills only)
      - 15% experience
      - 10% education
      - 10% LLM reasoning
      -  5% certifications
      -  5% GitHub (optional, redistributed if absent)
    """
    matched_skills = matched_skills or []
    missing_skills = missing_skills or []

    base_weights = {
        "vector": 0.30,
        "skills": 0.25,
        "experience": 0.15,
        "education": 0.10,
        "llm": 0.10,
        "certifications": 0.05,
        "github": 0.05,
    }

    # If no GitHub score, redistribute weight to skills + vector
    if github_score == 0.0:
        base_weights["vector"] += 0.03
        base_weights["skills"] += 0.02
        del base_weights["github"]
        github_contribution = 0.0
    else:
        github_contribution = github_score * base_weights["github"]

    weighted = (
        vector_score * base_weights["vector"] +
        skill_score * base_weights["skills"] +
        experience_score * base_weights["experience"] +
        education_score * base_weights["education"] +
        llm_score * base_weights["llm"] +
        certification_score * base_weights["certifications"] +
        github_contribution
    )

    final = round(min(100.0, max(0.0, weighted)), 2)

    # Build human-readable labels
    n_matched = len(matched_skills)
    n_missing = len(missing_skills)
    skills_label = f"{n_matched} compétences requises couvertes, {n_missing} manquantes"

    if candidate_years is not None and job_required_years is not None:
        if experience_gap > 0:
            experience_label = f"Il manque {experience_gap} an(s) d'expérience ({candidate_years}/{job_required_years} requis)"
        else:
            experience_label = f"Expérience suffisante ({candidate_years} ans, {job_required_years} requis)"
    else:
        experience_label = "Expérience non renseignée"

    edu_pct = int(education_score)
    education_label = f"Niveau d'études compatible à {edu_pct}%"

    return ScoreBreakdown(
        vector_score=vector_score,
        skill_score=skill_score,
        experience_score=experience_score,
        education_score=education_score,
        certification_score=certification_score,
        github_score=github_score,
        llm_score=llm_score,
        final_score=final,
        weights_used={k: round(v, 3) for k, v in base_weights.items()},
        skills_label=skills_label,
        experience_label=experience_label,
        education_label=education_label,
    )


def score_label(score: float) -> str:
    """Returns a human-readable rating label for a score."""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Très bon"
    elif score >= 55:
        return "Bon"
    elif score >= 40:
        return "Moyen"
    else:
        return "Faible"
