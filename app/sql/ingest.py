import json
import re
from langchain_core.prompts import PromptTemplate
from app.llm.ollama_client import get_llm
from app.utils.logger import logger

def extract_structured_data(text: str):
    """
    Uses the LLM to extract structured data from the CV text.
    Handles Ollama/DeepSeek R1 specific output (think tags, backticks).
    """
    llm = get_llm()
    
    prompt_template = """
    Extract EXHAUSTIVE structured information from the following CV text.
    
    CRITICAL INSTRUCTIONS:
    - RECONSTRUCTION: Reconstruct spaced-out characters correctly (e.g., 'D é v e l o p p e u r' -> 'Développeur').
    - SKILLS: Be very exhaustive. Look for:
        1. Technical skills (Python, SQL, Docker, etc.) -> category: 'technical'
        2. Soft skills (Savoir-être like Adaptabilité, Travail d'équipe) -> category: 'soft_skill'
        3. Languages (Anglais B1, Espagnol A2) -> category: 'language'
        4. Autodidact skills (N8N, MCP, Langchain, etc. from 'Apprentissage autodidacte' section) -> category: 'technical'
    - EDUCATION: Capture full degree names, schools, and dates precisely.
    - RETURN ONLY A RAW JSON OBJECT. NO MARKDOWN, NO EXPLANATION.

    Return the result in JSON format with these keys:
    - first_name, last_name, email, phone, city, summary
    - looking_for (goal, e.g., 'Alternance Développeur IA sept 2026')
    - experiences (list of: company, job_title, start_date, end_date, description)
    - education (list of: school, degree, field, start_year, end_year)
    - projects (list of: name, description, technologies)
    - skills (list of: skill_name, level)
    - languages (list of: language, level)

    CV TEXT:
    {text}

    JSON RESULT:
    """
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["text"]
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"text": text})
        content = response.content
        
        # Remove <think>...</think> blocks
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        
        # Remove markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        logger.error(f"Error extracting structured data: {e}")
        logger.debug(f"Raw content: {content if 'content' in locals() else 'N/A'}")
        return None
