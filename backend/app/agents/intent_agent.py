import json
import re
from backend.app.llm.ollama_client import get_fast_llm
from backend.app.config.constants import INTENT_RAG, INTENT_SQL, INTENT_GENERAL, INTENT_GITHUB
from backend.app.utils.logger import logger

from backend.app.core.monitoring import profile_async

@profile_async("Intent Agent")
async def classify_intent(state):
    """
    Classifies the user question into 'rag', 'sql', or 'general'.
    """
    question = state["question"]
    llm = get_fast_llm()
    
    prompt = f"""Classification rapide d'intention pour assistant IA :
    RAG: Questions narratives/missions. SQL: compétences/faits. GITHUB: ses projets/repos. hybrid: mélange compétences+missions. general: salutations.
    RÈGLES: UN SEUL MOT EN RÉPONSE, MINUSCULE. PAS DE BLA-BLA.
    QUESTION: {question}
    INTENT:"""
    
    try:
        response = await llm.ainvoke(prompt)
        content = response.content
        
        # Clean DeepSeek R1 output
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip().lower()
        
        # Ensure we only have the keyword
        if "hybrid" in content:
            intent = "hybrid"
        elif INTENT_GITHUB in content or "github" in content:
            intent = INTENT_GITHUB
        elif INTENT_RAG in content:
            intent = INTENT_RAG
        elif INTENT_SQL in content:
            intent = INTENT_SQL
        else:
            intent = INTENT_GENERAL

            
        logger.info(f"Detected intent: {intent} for question: {question}")
        return {"intent": intent}
    except Exception as e:
        logger.error(f"Error in intent classification: {e}")
        return {"intent": INTENT_GENERAL}
