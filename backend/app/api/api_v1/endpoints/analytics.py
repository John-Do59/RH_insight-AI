"""
Analytics Endpoint — Phase 4
Fournit les données agrégées pour le Dashboard RH.
Toutes les requêtes sont optimisées avec SQLAlchemy pour éviter le N+1.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from backend.app.database.session import get_db
from backend.app.models.candidate import Candidate
from backend.app.models.job import Job
from backend.app.models.skill import Skill, CandidateSkill, JobSkill
from backend.app.models.matching import CandidateJobMatch
from backend.app.api.deps import get_current_user
from backend.app.models.user import User

router = APIRouter()


@router.get("/kpis", summary="KPIs principaux du dashboard")
def get_kpis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns main KPIs: counts and average match score."""
    total_candidates = db.query(func.count(Candidate.id)).scalar() or 0
    total_jobs = db.query(func.count(Job.id)).scalar() or 0
    total_matches = db.query(func.count(CandidateJobMatch.id)).scalar() or 0
    avg_score = db.query(func.avg(CandidateJobMatch.score)).scalar()

    return {
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "total_matches": total_matches,
        "avg_score": round(float(avg_score), 1) if avg_score else None,
    }


@router.get("/recent-activity", summary="Activité récente")
def get_recent_activity(
    limit: int = 8,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns the N most recently added candidates."""
    candidates = (
        db.query(Candidate)
        .order_by(Candidate.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": str(c.id),
            "name": f"{c.first_name or ''} {c.last_name or ''}".strip() or "Candidat inconnu",
            "initials": (
                (c.first_name or "?")[0].upper() +
                (c.last_name or "?")[0].upper()
            ),
            "title": c.title or "—",
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in candidates
    ]


@router.get("/top-matches", summary="Meilleurs matchs candidats-offres")
def get_top_matches(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns the top N candidate-job matches by score."""
    matches = (
        db.query(CandidateJobMatch)
        .order_by(CandidateJobMatch.score.desc())
        .limit(limit)
        .all()
    )
    result = []
    for m in matches:
        candidate = db.query(Candidate).filter(Candidate.id == m.candidate_id).first()
        job = db.query(Job).filter(Job.id == m.job_id).first()
        if candidate and job:
            result.append({
                "id": str(m.id),
                "candidate": f"{candidate.first_name or ''} {candidate.last_name or ''}".strip(),
                "job": job.title,
                "score": round(float(m.score), 1) if m.score else 0,
            })
    return result


@router.get("/skill-distribution", summary="Top 10 compétences candidates")
def get_skill_distribution(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns the top N most common candidate skills."""
    rows = (
        db.query(Skill.name, func.count(CandidateSkill.skill_id).label("count"))
        .join(CandidateSkill, Skill.id == CandidateSkill.skill_id)
        .group_by(Skill.name)
        .order_by(func.count(CandidateSkill.skill_id).desc())
        .limit(limit)
        .all()
    )
    return [{"skill": r.name, "count": r.count} for r in rows]


@router.get("/top-job-skills", summary="Top compétences demandées par les offres")
def get_top_job_skills(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns the top N most required skills across all job offers."""
    rows = (
        db.query(Skill.name, func.count(JobSkill.skill_id).label("count"))
        .join(JobSkill, Skill.id == JobSkill.skill_id)
        .filter(JobSkill.is_required == True)  # noqa
        .group_by(Skill.name)
        .order_by(func.count(JobSkill.skill_id).desc())
        .limit(limit)
        .all()
    )
    return [{"skill": r.name, "count": r.count} for r in rows]


@router.get("/score-distribution", summary="Distribution des scores de matching")
def get_score_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns the score histogram bucketed by 20-point ranges."""
    buckets = [
        ("0-20", 0, 20),
        ("20-40", 20, 40),
        ("40-60", 40, 60),
        ("60-80", 60, 80),
        ("80-100", 80, 101),
    ]
    result = []
    for label, low, high in buckets:
        count = (
            db.query(func.count(CandidateJobMatch.id))
            .filter(
                CandidateJobMatch.score >= low,
                CandidateJobMatch.score < high
            )
            .scalar() or 0
        )
        result.append({"range": label, "count": count})
    return result


@router.get("/funnel", summary="Entonnoir de recrutement")
def get_funnel(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns the recruitment funnel stages."""
    uploaded = db.query(func.count(Candidate.id)).scalar() or 0
    # Analysed = candidates with at least one skill
    analysed = (
        db.query(func.count(func.distinct(CandidateSkill.candidate_id)))
        .scalar() or 0
    )
    matched = db.query(func.count(CandidateJobMatch.id)).scalar() or 0
    # "Selected" = matches with score >= 70
    selected = (
        db.query(func.count(CandidateJobMatch.id))
        .filter(CandidateJobMatch.score >= 70)
        .scalar() or 0
    )
    return [
        {"label": "CV uploadés", "count": uploaded},
        {"label": "CV analysés", "count": analysed},
        {"label": "Matchs calculés", "count": matched},
        {"label": "Candidats sélectionnés (≥70)", "count": selected},
    ]
