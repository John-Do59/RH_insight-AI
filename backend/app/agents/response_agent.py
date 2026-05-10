import re
from backend.app.llm.ollama_client import get_llm
from backend.app.utils.logger import logger

# VOS INFORMATIONS PERSONNELLES
PERSONAL_INFO = """
PROFIL :
- Nom : Amaury Rammanat
- Poste recherché : Développeur IA en alternance (Data Analyst, Data Scientist junior, ou Développeur IA)
- Disponibilité : Septembre 2026 (alternance 1 an)
- Localisation : Lille
- Email : rammanatamaury@gmail.com
- Téléphone : 06 01 02 23 20
- LinkedIn : linkedin.com/in/amaury-r-1bb0b032b/
- GitHub : John-Do59
"""

SYSTEM_PROMPT = """Tu es l'assistant IA d'Amaury Rammanat, développeur IA en formation.
Tu réponds aux questions des recruteurs comme si tu ÉTAIS Amaury.

TON RÔLE :
- Représenter Amaury auprès des recruteurs
- Mettre en valeur son profil de reconversion vers l'IA
- Parler à la première personne ("Je suis...", "J'ai travaillé...", "Je maîtrise...")

POINTS FORTS À METTRE EN AVANT :
- Reconversion réussie vers l'IA après 15 ans d'expérience professionnelle
- Formation intensive chez Simplon (Développeur IA - RNCP niveau 6)
- Autodidacte motivé (RAG, LLM, Agents IA, MCP)
- Profil polyvalent : logistique + tech + IA
- Passionné et curieux (veille techno, projets persos)

RÈGLES :
1. Réponds EXCLUSIVEMENT en français de haute qualité.
2. Utilise un ton professionnel, courtois et engageant.
3. Utilise "je", "mon", "mes" pour parler au nom d'Amaury.
4. Évite les anglicismes inutiles et soigne l'orthographe.
5. Base-toi uniquement sur le contexte fourni.
6. Si des projets GitHub sont présents, cite-les par leur nom exact.
7. Si une info manque : "Cette information n'est pas précisée dans mon CV."
"""


def response_agent(state):
    """
    Génère une réponse en tant qu'Amaury Rammanat.
    """
    question = state["question"]
    intent = state.get("intent", "general")
    rag_docs = state.get("documents", [])
    sql_data = state.get("sql_data", [])
    github_data = state.get("github_data", [])
    
    llm = get_llm()
    context = build_context(rag_docs, sql_data, github_data)
    
    if intent == "general":
        prompt = build_greeting_prompt(question)
    else:
        prompt = build_cv_prompt(question, context, intent)
    
    return {
        "final_prompt": prompt,
        "agent_sources": state.get("agent_sources", []) + ["response"]
    }


def build_greeting_prompt(question: str) -> str:
    """Prompt pour salutations et présentations."""
    return f"""{SYSTEM_PROMPT}

{PERSONAL_INFO}

L'utilisateur te salue ou demande une présentation générale.

Question: {question}

Réponds de manière chaleureuse, présente-toi brièvement et propose d'en dire plus sur ton parcours, tes compétences ou ta recherche d'alternance.

Réponse (en français, première personne) :"""


def build_cv_prompt(question: str, context: str, intent: str) -> str:
    """Prompt pour les questions sur le CV."""
    
    intent_hints = {
        "sql": "Réponds précisément sur mes compétences techniques, mes diplômes ou mes informations factuelles.",
        "rag": "Rédige une réponse narrative sur mon parcours, mes expériences ou mes motivations.",
        "github": "Donne une liste détaillée de mes projets GitHub, cite leurs noms et explique brièvement les technologies utilisées.",
        "hybrid": "Fais une synthèse complète incluant mon parcours de reconversion, mes hard skills (SQL) et mes réalisations concrètes sur GitHub."
    }
    
    hint = intent_hints.get(intent, "")
    
    return f"""{SYSTEM_PROMPT}

{PERSONAL_INFO}

CONSIGNE : {hint}

INFORMATIONS DE MON CV (À UTILISER EN PRIORITÉ) :
{context}

QUESTION DU RECRUTEUR :
{question}

MA RÉPONSE (précise, professionnelle, à la première personne) :"""


def build_context(rag_docs: list, sql_data: list, github_data: list) -> str:
    """Construit le contexte à partir de multiples sources."""
    parts = []
    
    if sql_data:
        parts.append("DONNÉES DU CV (Compétences/Faits) :")
        for row in sql_data[:15]:
            if isinstance(row, dict):
                formatted = " | ".join([f"{k}: {v}" for k, v in row.items() if v])
                parts.append(f"  • {formatted}")
    
    if rag_docs:
        parts.append("\nEXTRAITS DESCRIPTIFS DU CV :")
        for i, doc in enumerate(rag_docs[:5], 1):
            doc_clean = doc[:600] + "..." if len(doc) > 600 else doc
            parts.append(f"  [{i}] {doc_clean}")

    if github_data:
        parts.append("\nPROJETS GITHUB RÉCENTS (À CITER PAR LEURS NOMS) :")
        for repo in github_data[:10]:
            name = repo.get("name")
            desc = repo.get("description") or "Pas de description"
            lang = repo.get("language") or "N/A"
            stars = repo.get("stars", 0)
            url = repo.get("url")
            topics = ", ".join(repo.get("topics", []))
            tags = f" (Tags: {topics})" if topics else ""
            status = "Privé" if repo.get("is_private") else "Public"
            parts.append(
                f"  - REPO: {name}\n"
                f"    ACCÈS: {status}\n"
                f"    LANGAGE: {lang}{tags}\n"
                f"    DESCRIPTION: {desc}\n"
                f"    LIEN: {url}\n"
                f"    STARS: {stars}"
            )
    
    return "\n".join(parts) if parts else "Aucune information trouvée."


def clean_response(content: str) -> str:
    """Nettoie la réponse."""
    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    content = content.strip()
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content
