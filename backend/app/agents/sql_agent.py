import re
from sqlalchemy import text
from backend.app.llm.ollama_client import get_fast_llm
from backend.app.database.engine import get_engine
from backend.app.database.validators import validate_sql_query, SQLValidationError
from backend.app.utils.logger import logger

# SCHEMA D'INFORMATIONS RH
SCHEMA_INFO = """
TABLE candidates (candidats):
  - id, first_name, last_name
  - email, phone, city
  - summary (résumé du profil)

TABLE skills (compétences techniques):
  - id, candidate_id, skill_name, level

TABLE experiences (expériences pro):
  - id, candidate_id, company, job_title, start_date, end_date, description

TABLE education (formations):
  - id, candidate_id, school, degree, field, start_year, end_year

TABLE projects (projets du candidat):
  - id, candidate_id, name, description, technologies

TABLE languages (langues):
  - id, candidate_id, language, level
"""

SQL_EXAMPLES = """
EXEMPLES DE REQUÊTES :

Question: "Quels sont les candidats avec Python ?"
SQL: SELECT c.first_name, c.last_name FROM candidates c JOIN skills s ON c.id = s.candidate_id WHERE LOWER(s.skill_name) LIKE '%python%';

Question: "Quelles sont les formations de Jean Dupont ?"
SQL: SELECT e.school, e.degree FROM education e JOIN candidates c ON e.candidate_id = c.id WHERE LOWER(c.first_name) = 'jean' AND LOWER(c.last_name) = 'dupont';

Question: "Combien y a-t-il de candidats ?"
SQL: SELECT COUNT(*) FROM candidates;
"""


from backend.app.core.monitoring import profile_async
from backend.app.database.engine import get_async_engine

@profile_async("SQL Agent")
async def sql_agent(state):
    """
    Génère et exécute une requête SQL pour la base de données RH.
    """
    question = state["question"]
    llm = get_fast_llm()
    
    prompt = f"""Tu génères des requêtes SQL (PostgreSQL) pour interroger une base de données de recrutement contenant plusieurs candidats.

{SCHEMA_INFO}

{SQL_EXAMPLES}

RÈGLES :
1. SELECT uniquement
2. Utilise LOWER() et LIKE pour les recherches texte
3. Fais des JOIN si nécessaire pour relier les compétences/expériences aux candidats
4. Renvoie UNIQUEMENT la requête SQL, rien d'autre

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
