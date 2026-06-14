"""
Matching Nodes — Phase 3 (Orchestrator-only)
LangGraph nodes that orchestrate calls to matching_service and scoring_service.
No business logic here — pure orchestration.
"""
import numpy as np
from typing import Any

from backend.app.graph.matching_state import MatchingState
from backend.app.database.session import get_db
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.skill import CandidateSkill, JobSkill, Skill
from backend.app.models.github import GithubProfile
from backend.app.llm.ollama_client import get_fast_llm
from backend.app.services.matching_service import run_full_comparison
from backend.app.services.scoring_service import compute_score, score_label
import json


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    if not vec1 or not vec2:
        return 0.0
    v1, v2 = np.array(vec1), np.array(vec2)
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (n1 * n2))


def load_data_node(state: MatchingState) -> MatchingState:
    """Loads candidate, job and their associated data from the database."""
    db = next(get_db())
    candidate = db.query(Candidate).filter(Candidate.id == state["candidate_id"]).first()
    job = db.query(Job).filter(Job.id == state["job_id"]).first()

    if not candidate or not job:
        raise ValueError("Candidat ou offre introuvable")

    # Candidate skills
    c_skills = db.query(Skill.name).join(CandidateSkill).filter(
        CandidateSkill.candidate_id == candidate.id
    ).all()

    # Job skills — distinguish required vs preferred
    j_all = db.query(Skill.name, JobSkill.is_required).join(JobSkill).filter(
        JobSkill.job_id == job.id
    ).all()
    job_all_skills = [row[0] for row in j_all]
    job_required_skills = [row[0] for row in j_all if row[1] is True]

    state["candidate_data"] = {
        "id": str(candidate.id),
        "title": candidate.title,
        "experience_years": candidate.experience_years,
        "education": candidate.education or [],
        "certifications": candidate.certifications or [],
        "languages": candidate.languages or [],
        "embedding": candidate.embedding,
        "summary": candidate.summary,
    }

    state["job_data"] = {
        "id": str(job.id),
        "title": job.title,
        "description": job.description,
        "experience_years": job.experience_years,
        "education_level": job.education_level,
        "certifications": job.certifications or [],
        "embedding": job.embedding,
    }

    state["candidate_skills"] = [s[0] for s in c_skills]
    state["job_skills"] = job_all_skills
    state["job_required_skills"] = job_required_skills

    # GitHub profile
    github = db.query(GithubProfile).filter(
        GithubProfile.candidate_id == candidate.id
    ).first()
    if github:
        state["candidate_data"]["github"] = {
            "contribution_score": github.contribution_score,
            "repositories_count": github.repositories_count,
        }

    return state


def vector_retrieval_node(state: MatchingState) -> MatchingState:
    """Computes cosine similarity between candidate and job embeddings."""
    c_emb = state["candidate_data"].get("embedding")
    j_emb = state["job_data"].get("embedding")

    if c_emb and j_emb:
        sim = cosine_similarity(c_emb, j_emb)
        state["vector_score"] = round(max(0.0, sim) * 100, 2)
    else:
        state["vector_score"] = 0.0

    return state


def skill_comparison_node(state: MatchingState) -> MatchingState:
    """
    Delegates all comparison logic to matching_service.
    Populates scores and gap analysis into state.
    """
    comparison = run_full_comparison(
        candidate_data=state["candidate_data"],
        job_data=state["job_data"],
        candidate_skills=state["candidate_skills"],
        job_skills=state["job_skills"],
        job_required_skills=state.get("job_required_skills", state["job_skills"]),
    )

    state["matched_skills"] = comparison["matched_skills"]
    state["missing_skills"] = comparison["missing_skills"]
    state["bonus_skills"] = comparison.get("bonus_skills", [])
    state["skill_score"] = comparison["skill_score"]
    state["experience_score"] = comparison["experience_score"]
    state["experience_gap"] = comparison.get("experience_gap", 0)
    state["education_score"] = comparison.get("education_score", 100.0)
    state["certification_score"] = comparison.get("certification_score", 100.0)

    # GitHub score
    github_data = state["candidate_data"].get("github")
    state["github_score"] = min(100.0, (github_data.get("contribution_score") or 0) * 10) if github_data else 0.0

    return state


def reasoning_node(state: MatchingState) -> MatchingState:
    """Uses LLM to generate human-readable strengths, gaps and an explanation."""
    llm = get_fast_llm()

    prompt = f"""En tant qu'expert RH senior, évaluez la compatibilité entre ce candidat et cette offre.

Candidat:
- Titre: {state['candidate_data'].get('title')}
- Années d'expérience: {state['candidate_data'].get('experience_years')}
- Résumé: {state['candidate_data'].get('summary', '')[:300]}
- Compétences: {', '.join(state['candidate_skills'][:20])}

Offre:
- Titre: {state['job_data'].get('title')}
- Expérience requise: {state['job_data'].get('experience_years')} ans
- Compétences requises: {', '.join(state.get('job_required_skills', [])[:20])}

Compétences couvertes: {', '.join(state['matched_skills'][:10])}
Compétences manquantes: {', '.join(state['missing_skills'][:10])}

Retournez UNIQUEMENT du JSON valide avec ces clés :
{{"strengths": ["..."], "gaps": ["..."], "explanation": "...", "llm_score": 75}}"""

    try:
        response = llm.invoke([
            ("system", "Vous êtes un assistant RH expert. Répondez UNIQUEMENT en JSON."),
            ("human", prompt)
        ])
        text = response.content
        start, end = text.find('{'), text.rfind('}') + 1
        if start != -1 and end > start:
            result = json.loads(text[start:end])
            state["strengths"] = result.get("strengths", state["matched_skills"])
            state["gaps"] = result.get("gaps", state["missing_skills"])
            state["explanation"] = result.get("explanation", "")
            state["llm_score"] = float(result.get("llm_score", 50.0))
        else:
            raise ValueError("No JSON in LLM response")
    except Exception:
        state["strengths"] = state["matched_skills"]
        state["gaps"] = state["missing_skills"]
        state["explanation"] = "Analyse automatique (IA temporairement indisponible)."
        state["llm_score"] = state["skill_score"]

    return state


def scoring_node(state: MatchingState) -> MatchingState:
    """
    Delegates final score computation to scoring_service.
    Stores a rich, explainable ScoreBreakdown in state.
    """
    breakdown = compute_score(
        vector_score=state.get("vector_score", 0.0),
        skill_score=state.get("skill_score", 0.0),
        experience_score=state.get("experience_score", 100.0),
        education_score=state.get("education_score", 100.0),
        certification_score=state.get("certification_score", 100.0),
        github_score=state.get("github_score", 0.0),
        llm_score=state.get("llm_score", 50.0),
        experience_gap=state.get("experience_gap", 0),
        matched_skills=state.get("matched_skills", []),
        missing_skills=state.get("missing_skills", []),
        candidate_years=state["candidate_data"].get("experience_years"),
        job_required_years=state["job_data"].get("experience_years"),
    )

    state["final_score"] = breakdown.final_score
    state["score_breakdown"] = breakdown.to_dict()
    state["score_label"] = score_label(breakdown.final_score)

    return state
