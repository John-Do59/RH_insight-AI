# Structure du projet — Chatbot IA Recruteur

Cette structure sert de **référence officielle** pour implémenter le projet  
**LangGraph + Agent RAG + Agent SQL + Streamlit + CV PDF**.

---

## Arborescence générale

```text
chatbot-cv-ai/
│
├── app/
│   ├── streamlit_app.py          # Interface Streamlit (UI uniquement)
│   │
│   ├── config/
│   │   ├── settings.py           # Config globale (paths, modèles, DB)
│   │   └── constants.py          # Constantes métier (tables, rôles agents)
│   │
│   ├── graph/
│   │   ├── graph.py              # Définition du graphe LangGraph
│   │   ├── state.py              # State partagé LangGraph
│   │   └── router.py             # Détection d’intention / routage
│   │
│   ├── agents/
│   │   ├── rag_agent.py          # Agent RAG LangGraph
│   │   ├── sql_agent.py          # Agent SQL custom LangGraph
│   │   ├── intent_agent.py       # Agent de classification d’intention
│   │   └── response_agent.py     # Agent de réponse finale
│   │
│   ├── rag/
│   │   ├── ingest.py             # Ingestion du CV pour le RAG
│   │   ├── chunking.py           # Découpage du texte
│   │   ├── embeddings.py         # Génération des embeddings
│   │   └── vector_store.py       # Base vectorielle
│   │
│   ├── sql/
│   │   ├── schema.sql            # Schéma de la base SQL
│   │   ├── database.py           # Connexion DB
│   │   ├── ingest.py             # Insertion des données CV
│   │   └── validators.py         # Validation des requêtes SQL
│   │
│   ├── pdf/
│   │   ├── cv.pdf                # CV source (PDF)
│   │   └── extractor.py          # Extraction texte du PDF
│   │
│   ├── audio/
│   │   ├── speech_to_text.py     # Entrée vocale (optionnel)
│   │   └── text_to_speech.py     # Sortie vocale (optionnel)
│   │
│   ├── llm/
│   │   └── ollama_client.py      # Client Ollama (DeepSeek R1 Q4)
│   │
│   └── utils/
│       ├── logger.py             # Logging
│       └── helpers.py            # Fonctions utilitaires
│
├── data/
│   ├── vector_store/             # Données embeddings
│   └── sql/                      # Base SQLite / dumps
│
├── scripts/
│   ├── ingest_cv.py              # Pipeline complet d’ingestion du CV
│   └── init_db.py                # Initialisation DB SQL
│
├── tests/
│   ├── test_rag_agent.py
│   ├── test_sql_agent.py
│   ├── test_router.py
│   └── test_graph.py
│
├── docs/
│   ├── architecture.md           # Description architecture globale
│   ├── agents.md                 # Détails des agents LangGraph
│   └── decisions.md              # Choix techniques justifiés
│
├── requirements.txt              # Dépendances Python
├── .env.example                  # Variables d’environnement
├── README.md                     # Présentation du projet
└── Makefile                      # Commandes utiles (run, ingest, test)
