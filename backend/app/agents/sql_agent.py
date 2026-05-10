import re
from sqlalchemy import text
from backend.app.llm.ollama_client import get_fast_llm
from backend.app.sql.database import get_engine
from backend.app.sql.validators import validate_sql_query, SQLValidationError
from backend.app.utils.logger import logger

# SCHEMA ADAPTÉ AU CV
SCHEMA_INFO = """
TABLE candidates (mes informations personnelles):
  - id, first_name (Amaury), last_name (Rammanat)
  - email (rammanatamaury@gmail.com), phone (0601022320), city (Lille)
  - summary (résumé du profil)

TABLE skills (mes compétences techniques):
  - id, candidate_id, skill_name, level
  - Exemples: Python, SQL, Docker, Langchain, PyTorch, Streamlit, Git...

TABLE experiences (mes expériences pro):
  - id, candidate_id, company, job_title, start_date, end_date, description
  - Paysagiste (2020-2025), Gestionnaire milieux naturels (2010-2020)...

TABLE education (mes formations):
  - id, candidate_id, school, degree, field, start_year, end_year
  - Simplon (Dev IA), Apple Foundation, ULCO (Licence, DEUST)...

TABLE projects (mes projets):
  - id, candidate_id, name, description, technologies
  - Sport-Unity IA (iOS, chatbot fitness)...

TABLE languages (langues):
  - id, candidate_id, language, level
  - Anglais B1, Espagnol A2
"""

SQL_EXAMPLES = """
EXEMPLES DE REQUÊTES :

Question: "Quelles sont tes compétences ?"
SQL: SELECT skill_name, level FROM skills ORDER BY level DESC;

Question: "Tu connais Python ?"
SQL: SELECT skill_name, level FROM skills WHERE LOWER(skill_name) LIKE '%python%';

Question: "Quelles sont tes formations ?"
SQL: SELECT school, degree, field, start_year, end_year FROM education ORDER BY start_year DESC;

Question: "Où as-tu travaillé ?"
SQL: SELECT company, job_title, start_date, end_date FROM experiences ORDER BY start_date DESC;

Question: "Tu parles quelles langues ?"
SQL: SELECT language, level FROM languages;

Question: "Tes coordonnées ?"
SQL: SELECT first_name, last_name, email, phone, city FROM candidates LIMIT 1;

Question: "Compétences en IA ?"
SQL: SELECT skill_name, level FROM skills WHERE LOWER(skill_name) LIKE '%ia%' OR LOWER(skill_name) LIKE '%machine%' OR LOWER(skill_name) LIKE '%learning%' OR LOWER(skill_name) LIKE '%pytorch%' OR LOWER(skill_name) LIKE '%langchain%';
"""


from backend.app.core.monitoring import profile_async
from backend.app.sql.database import get_async_engine

@profile_async("SQL Agent")
async def sql_agent(state):
    """
    Génère et exécute une requête SQL pour le CV d'Amaury.
    """
    question = state["question"]
    llm = get_fast_llm()
    
    prompt = f"""Tu génères des requêtes SQL pour interroger le CV d'Amaury Rammanat.
Il n'y a qu'UN SEUL candidat, pas besoin de filtrer par nom.

{SCHEMA_INFO}

{SQL_EXAMPLES}

RÈGLES :
1. SELECT uniquement
2. Utilise LOWER() et LIKE pour les recherches texte
3. Renvoie UNIQUEMENT la requête SQL, rien d'autre

Question: {question}
SQL:"""
    
    try:
        response = await llm.ainvoke(prompt)
        query = extract_sql(response.content)
        
        # Validate query for safety before execution
        try:
            validate_sql_query(query)
        except SQLValidationError as e:
            logger.warning(f"SQL query rejected: {e} — Query: {query}")
            return {"sql_data": [], "sql_query": f"Rejected: {e}"}
        
        logger.info(f"SQL: {query}")
        
        engine = get_async_engine()
        async with engine.connect() as conn:
            result = await conn.execute(text(query))
            rows = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        
        return {
            "sql_data": rows,
            "sql_query": query,
            "agent_sources": state.get("agent_sources", []) + ["sql"]
        }
        
    except Exception as e:
        logger.error(f"Error in SQL agent: {e}")
        return {
            "sql_data": [], 
            "sql_query": "Error",
            "agent_sources": state.get("agent_sources", []) + ["sql"]
        }


def extract_sql(content: str) -> str:
    """Extrait la requête SQL."""
    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    
    if "```sql" in content:
        match = re.search(r'```sql\s*(.*?)\s*```', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    
    if "```" in content:
        match = re.search(r'```\s*(.*?)\s*```', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return content.strip()
