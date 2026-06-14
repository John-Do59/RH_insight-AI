import json
from backend.app.llm.ollama_client import get_fast_llm

def parse_candidate_resume(message: str) -> dict:
    """
    Transforms raw resume text into structured Candidate JSON data using LLM.
    """
    prompt = f"""
    Tu es un expert en recrutement RH.
    Extrais les informations suivantes du CV ci-dessous :
    - prenom
    - nom
    - email
    - titre_poste (le titre du poste actuel ou visé)
    - competences (liste de mots clés)
    - annees_experience (entier estimé, 0 si inconnu)
    - localisation
    - resume (un court paragraphe résumant le profil)

    Retourne UNIQUEMENT du JSON valide avec les clés suivantes :
    "first_name", "last_name", "email", "title", "skills", "experience_years", "location", "summary"

    CV :
    {message}
    """
    
    llm = get_fast_llm()
    response = llm.invoke([
        ("system", "Vous êtes un assistant RH expert. Répondez UNIQUEMENT en JSON."),
        ("human", prompt)
    ])
    response_text = response.content
    
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            raise ValueError("Invalid JSON format from LLM")
            
    except Exception as e:
        # Fallback
        return {
            "first_name": "Inconnu",
            "last_name": "",
            "email": "",
            "title": "Candidat",
            "skills": [],
            "experience_years": 0,
            "location": "",
            "summary": "Parsing failed."
        }
