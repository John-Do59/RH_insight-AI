import re
from typing import Optional, Union
from backend.app.llm.ollama_client import get_fast_llm
from backend.app.config.constants import INTENT_RAG, INTENT_SQL, INTENT_GENERAL, INTENT_GITHUB
from backend.app.utils.logger import logger
from backend.app.core.monitoring import profile_async

# ── Keyword rules (< 1ms, no LLM call needed) ────────────────────────────────
_RAG_KEYWORDS = [
    "parcours", "formation", "diplôme", "école", "université", "étude",
    "expérience", "poste", "mission", "projet", "réalisation", "stage",
    "cv", "profil", "candidat", "offre", "job", "description",
    "compétence", "skill", "technologie", "outil", "langage", "framework",
    "python", "fastapi", "vue", "docker", "langchain", "sql", "machine learning",
    "ia", "intelligence artificielle", "développeur", "ingénieur",
    "soft skill", "qualité", "atout", "force", "point fort",
    "certification", "langue", "anglais", "français",
]

_SQL_KEYWORDS = [
    "combien", "nombre", "liste tous", "moyenne", "total", "classement",
    "statistique", "rapport", "recrut", "candidature",
]

_GITHUB_KEYWORDS = [
    "github", "repo", "dépôt", "commit", "pull request", "code source",
    "contribution", "open source",
]

_GENERAL_KEYWORDS = [
    "bonjour", "salut", "hello", "merci", "aide", "comment ça va",
    "qui es-tu", "que fais-tu", "présente-toi",
]

def _keyword_classify(question: str) -> Optional[str]:
    """Fast O(n) keyword scan. Returns intent or None if ambiguous."""
    q = question.lower()
    
    scores = {
        INTENT_RAG: sum(1 for kw in _RAG_KEYWORDS if kw in q),
        INTENT_SQL: sum(1 for kw in _SQL_KEYWORDS if kw in q),
        INTENT_GITHUB: sum(1 for kw in _GITHUB_KEYWORDS if kw in q),
        INTENT_GENERAL: sum(1 for kw in _GENERAL_KEYWORDS if kw in q),
    }
    
    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]
    
    # Only trust keyword match if score >= 1 and clearly wins
    if best_score == 0:
        return None  # No keyword matched → fall back to LLM
    
    return best_intent


@profile_async("Intent Agent")
async def classify_intent(state):
    """
    Classifies user question intent using fast keyword rules first,
    with LLM fallback only for truly ambiguous cases.
    """
    question = state["question"]

    # ── 1. Fast path: keyword classification (< 1ms) ─────────────────────────
    intent = _keyword_classify(question)
    
    if intent is not None:
        logger.info(f"[FAST] Intent: {intent} for: {question}")
        return {"intent": intent}

    # ── 2. Slow path: LLM fallback for ambiguous questions ───────────────────
    logger.info(f"[LLM] Ambiguous question, using LLM for: {question}")
    llm = get_fast_llm()
    
    prompt = (
        "Tu es un classificateur d'intention pour un assistant IA de recrutement (RH).\n"
        "Réponds avec UN SEUL MOT parmi: rag, sql, github, general\n"
        "- rag: questions sur les compétences d'un candidat, une analyse de CV ou la description d'une offre d'emploi\n"
        "- sql: requêtes statistiques ou recherches précises sur la base de données RH (ex: combien de candidats avec Python ?)\n"
        "- github: questions sur des projets open source ou dépôts GitHub d'un candidat\n"
        "- general: salutations, questions hors sujet, ou présentation de tes capacités\n"
        f"Question: {question}\n"
        "Intention:"
    )

    try:
        response = await llm.ainvoke(prompt)
        content = re.sub(r'<think>.*?</think>', '', response.content, flags=re.DOTALL).strip().lower()

        if "hybrid" in content:
            intent = "hybrid"
        elif INTENT_GITHUB in content:
            intent = INTENT_GITHUB
        elif INTENT_RAG in content:
            intent = INTENT_RAG
        elif INTENT_SQL in content:
            intent = INTENT_SQL
        else:
            intent = INTENT_GENERAL

        logger.info(f"[LLM] Detected intent: {intent} for: {question}")
        return {"intent": intent}

    except Exception as e:
        logger.error(f"Error in LLM intent classification: {e}")
        # Default to RAG for questions about a person (most common case)
        return {"intent": INTENT_RAG}
