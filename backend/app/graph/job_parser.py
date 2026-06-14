import json
from backend.app.llm.ollama_client import get_fast_llm

def parse_job_description(message: str) -> dict:
    """
    Transforms raw job text into structured HR JSON data using LLM.
    """
    prompt = f"""
    Tu es un expert RH.
    Extrais les informations suivantes de l'offre d'emploi ci-dessous :
    - titre du poste
    - compétences techniques (liste de mots clés)
    - niveau d'expérience (entier, 0 si non mentionné)
    - localisation (chaine vide si non mentionné)
    - type de contrat (chaine vide si non mentionné)

    Retourne UNIQUEMENT du JSON valide avec les clés suivantes :
    "title", "skills", "experience", "location", "contract_type"

    Offre :
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
        # Fallback in case of failure
        return {
            "title": "Titre non identifié",
            "skills": [],
            "experience": 0,
            "location": "",
            "contract_type": ""
        }
