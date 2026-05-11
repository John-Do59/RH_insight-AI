# RH Insight AI — Assistant de Recrutement Intelligent

Plateforme RAG multi-agents pour l'analyse de CV et l'assistance au recrutement, propulsée par des LLMs locaux via Ollama.

## Fonctionnalités

- **Chat RAG** : Interrogez les CV en langage naturel (recherche sémantique via ChromaDB)
- **Agent SQL** : Requêtes structurées sur la base de données des candidats
- **Agent GitHub** : Analyse de l'activité open-source des candidats
- **Multi-Agents** : Orchestration LangGraph avec routage intelligent selon l'intention
- **Streaming** : Réponses en temps réel token par token
- **Auth sécurisée** : JWT + Rate Limiting anti-brute force

## Stack Technique

| Couche | Technologie |
|---|---|
| Backend API | FastAPI + Python 3.11 |
| IA / LLM | Ollama (`qwen3.5:4b`, `nomic-embed-text`) |
| Orchestration | LangChain + LangGraph |
| Vector Store | ChromaDB |
| Base de données | PostgreSQL (prod) / SQLite (dev local) |
| Frontend | Vue.js 3 + Composition API |
| Auth | OAuth2 + JWT (bcrypt) |
| Sécurité | slowapi (Rate Limiting) |
| CI | GitHub Actions |
| Conteneurs | Docker + Docker Compose |

## Démarrage Rapide

### Prérequis

- [Ollama](https://ollama.com) installé avec les modèles téléchargés :
  ```bash
  ollama pull qwen3.5:4b
  ollama pull nomic-embed-text
  ```
- Docker & Docker Compose (pour le mode production)
- Python 3.11+ et Node.js 18+ (pour le mode local)

### Mode Local (Développement)

```bash
# 1. Cloner et configurer
git clone https://github.com/John-Do59/RH_insight-AI.git
cd RH_insight-AI
cp .env.example .env   # Éditer .env avec vos valeurs

# 2. Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Frontend (dans un autre terminal)
cd frontend/vue-app
npm install && npm run dev
```

> **Base de données** : En mode local, SQLite est utilisé automatiquement (via `DATABASE_URL=sqlite:///./rh_insight.db` dans `.env`). Aucun PostgreSQL requis.

### Mode Production (Docker)

```bash
# Lancer tous les services (FastAPI + Vue.js + PostgreSQL + ChromaDB)
docker compose up -d --build

# Initialiser la base de données
docker exec rh-backend alembic upgrade head

# Ingérer les CV dans ChromaDB
docker exec rh-backend python -m backend.scripts.ingest_cv
```

- Application : `http://localhost:5173`
- API Swagger : `http://localhost:8000/docs`

## ⚡ Optimisations pour Mac (Apple Silicon 16Go)

Le projet est optimisé pour tourner sur Mac M-series avec 16Go de RAM unifiée :

| Paramètre | Valeur | Raison |
|---|---|---|
| `num_ctx` | `2048` | Limite l'empreinte KV-Cache GPU |
| `num_predict` | `512` | Évite d'épuiser la RAM sur de longues réponses |
| `think` | `false` | Désactive le raisonnement interne de Qwen3.5 (économie de tokens) |

> **Modèles déconseillés sur 16Go** : `qwen3.5:9b`, `deepseek-r1:7b` (risque de swap et timeouts)

## Documentation

| Document | Description |
|---|---|
| [Architecture](docs/architecture.md) | Diagramme et détail des composants |
| [Commandes utiles](docs/commandes_utiles.md) | Référence des commandes dev et prod |
| [Sécurité](docs/security.md) | Rate limiting, JWT, gestion des secrets |
| [CI/CD](docs/ci_cd.md) | Pipeline GitHub Actions et stratégie de branches |

## Structure du Projet

```
RH_insight-AI/
├── backend/
│   ├── app/
│   │   ├── agents/      # Agents LangGraph (RAG, SQL, GitHub, Intent)
│   │   ├── api/         # Endpoints FastAPI (auth, chat)
│   │   ├── llm/         # Clients Ollama
│   │   ├── models/      # Modèles SQLAlchemy
│   │   ├── rag/         # Vector store ChromaDB
│   │   └── services/    # ChatService (streaming)
│   ├── scripts/         # Ingestion CV, seed DB, migration
│   └── tests/           # Tests unitaires et d'intégration
├── frontend/vue-app/    # Interface Vue.js 3
├── docs/                # Documentation technique
├── .github/workflows/   # Pipeline CI/CD
└── docker-compose.yml   # Orchestration production
```

## Auteur

Projet développé par **Amaury Rammanat** — Développeur IA (RNCP Niveau 6, Simplon)
