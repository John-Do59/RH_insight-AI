# RH Insight AI - Chatbot Recruteur

Assistant intelligent utilisant **LangGraph**, **RAG**, et un **Agent SQL** pour l'analyse de CV et de données recrutement.

## Architecture

- **LangGraph**: Orchestration du flux de décision.
- **RAG Agent**: Analyse du contenu textuel des CV (PDF).
- **SQL Agent**: Requêtage structuré sur la base de données candidats.
- **LLM**: DeepSeek R1 via Ollama.
- **UI**: Streamlit.

## Installation

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `pip install sentence-transformers`
5. `cp .env.example .env` (Configurez vos variables)
6. `export PYTHONPATH=$PYTHONPATH:.`
7. `python scripts/init_db.py`
8. `python scripts/ingest_cv.py`
9. `streamlit run app/streamlit_app.py`
