from typing import TypedDict, List, Dict, Any, Optional
from uuid import UUID

class MatchingState(TypedDict):
    """
    Represents the state of the Matching LangGraph Agent — Phase 3.
    LangGraph nodes pass this dict between them; services are called from within nodes.
    """
    # Inputs
    candidate_id: UUID
    job_id: UUID

    # Loaded data (load_data_node)
    candidate_data: Optional[Dict[str, Any]]
    job_data: Optional[Dict[str, Any]]

    # Skills lists
    candidate_skills: List[str]
    job_skills: List[str]
    job_required_skills: List[str]

    # Comparison results (skill_comparison_node → matching_service)
    matched_skills: List[str]
    missing_skills: List[str]
    bonus_skills: List[str]

    # Sub-scores
    vector_score: float
    skill_score: float
    experience_score: float
    education_score: float
    certification_score: float
    github_score: float
    llm_score: float
    experience_gap: int

    # LLM reasoning (reasoning_node)
    strengths: List[str]
    gaps: List[str]
    explanation: str

    # Final score (scoring_node → scoring_service)
    final_score: float
    score_breakdown: Dict[str, Any]   # rich breakdown dict from ScoreBreakdown.to_dict()
    score_label: str                   # "Excellent" / "Très bon" / etc.
