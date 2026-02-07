import json
import re
from app.llm.ollama_client import get_llm
from app.config.constants import INTENT_RAG, INTENT_SQL, INTENT_GENERAL
from app.utils.logger import logger

def classify_intent(state):
    """
    Classifies the user question into 'rag', 'sql', or 'general'.
    """
    question = state["question"]
    llm = get_llm()
    
    prompt = f"""
    Tu es un expert en classification d'intention pour un système de recrutement IA.
    Ton but est d'orienter la question de l'utilisateur vers le bon agent spécialisé ou d'utiliser le mode HYBRIDE.

    CATÉGORIES :
    - '{INTENT_RAG}': Questions qualitatives ou narratives sur le parcours.
      Exemples: "Quels sont ses projets ?", "Décris ses missions", "Résumé du parcours".
    - '{INTENT_SQL}': Questions sur les compétences (SKILLS), les faits précis ou les listes.
      Exemples: "A-t-il des compétences en Python ?", "Liste ses diplômes", "Où habite-t-il ?".
    - 'hybrid': Questions complexes demandant à la fois des listes/faits ET des explications/contexte. 
      Exemples: "Quelles sont ses compétences et sur quels projets les a-t-il utilisées ?", "Parle-moi de son expérience en SQL".
    - '{INTENT_GENERAL}': Salutations ou discussion hors sujet.

    CRITIQUE :
    - Pour TOUTE question mélangeant compétences (SQL) et expérience détaillée (RAG), utilise 'hybrid'.
    - RENVOIE UNIQUEMENT LE NOM DE LA CATÉGORIE EN MINUSCULES.
    
    QUESTION: {question}
    INTENT:
    """
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        
        # Clean DeepSeek R1 output
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip().lower()
        
        # Ensure we only have the keyword
        if "hybrid" in content:
            intent = "hybrid"
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
