# RH Insight AI — Architecture Globale (v2)

> **Mis à jour le** : Juin 2026  
> **Version** : 2.0 — Architecture Multi-Agents

---

## Résumé de l'Évolution

| Version | Architecture | Base de données | Infra |
|---|---|---|---|
| v1 (origine) | RAG simple + Chatbot | SQLite | Serveur local |
| **v2 (actuelle)** | **Multi-agents LangGraph** | **PostgreSQL + pgvector** | **Docker + Traefik** |

---

## Vue Système Globale

```
Utilisateur (Browser)
        ↓ HTTPS
     Traefik (Reverse Proxy + Let's Encrypt)
        ├── /            → Frontend (Vue.js 3 via Nginx)
        └── /api         → Backend (FastAPI via Uvicorn)
                                ↓
                         LangGraph Agents
                          ├── Chat Agent (RAG + SQL + GitHub)
                          ├── Matching Agent (Scoring IA)
                          └── Job Parser Agent (Extraction LLM)
                                ↓
                    ┌───────────────────────────┐
                    │   PostgreSQL + pgvector   │
                    │   (Données + Embeddings)  │
                    └───────────────────────────┘
                                ↓
                           Redis (Cache)
                                ↓
                        Ollama (LLM local)
```

---

## Branches et Fonctionnalités Implémentées

| Branche | Fonctionnalité | Doc |
|---|---|---|
| `feature/database-design` | Modèles SQLAlchemy 2.0, pgvector, Alembic | [postgresql_migration.md](./postgresql_migration.md) |
| `feature/docker-production-infrastructure` | Dockerfiles, compose dev/prod, Nginx | [docker.md](./docker.md) |
| `feature/docker-production-infrastructure` | Traefik reverse proxy + HTTPS | [traefik.md](./traefik.md) |
| `feature/cicd-production-ready` | GitHub Actions, GHCR, simulation VPS | [cicd.md](./cicd.md) |
| `feature/matching-engine-v1` | LangGraph Matching Agent + API | [matching_engine.md](./matching_engine.md) |
| `feature/matching-engine-e2e-tests` | Suite de tests E2E complète | [tests_e2e.md](./tests_e2e.md) |
| `feature/job-intake-chat-agent` | Job Parser + Interface Chat IA | [matching_engine.md](./matching_engine.md#job-intake-chat-agent) |

---

## Stack Technique Complète

### Backend
- **Framework** : FastAPI (async)
- **ORM** : SQLAlchemy 2.0 (Mapped[], déclaratif moderne)
- **Agents IA** : LangGraph (StateGraph)
- **LLM** : Ollama (Qwen 3.5 4B + DeepSeek-R1 7B)
- **Migrations** : Alembic

### Frontend
- **Framework** : Vue.js 3 (Composition API)
- **State** : Pinia
- **Routing** : Vue Router
- **HTTP** : Axios

### Infrastructure
- **Conteneurisation** : Docker + Docker Compose
- **Reverse Proxy** : Traefik v2.10
- **Registry** : GHCR (GitHub Container Registry)
- **CI/CD** : GitHub Actions

### Base de Données
- **SGBD** : PostgreSQL 16
- **Extension vectorielle** : pgvector (HNSW, cosine similarity)
- **Cache** : Redis 7

---

## Démarrage Rapide

### Développement local

```bash
# 1. Cloner et configurer
cp .env.example .env  # Remplir les variables

# 2. Activer venv et installer les dépendances
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Lancer les migrations
alembic upgrade head

# 4. Démarrer les services (hot-reload)
docker compose -f docker/docker-compose.dev.yml up

# 5. Backend séparément (optionnel, si pas dans Docker)
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Simulation VPS locale

```bash
docker compose -f docker/docker-compose.local-prod.yml up -d
# → Frontend : http://localhost/
# → API : http://localhost/api/
# → Docs : http://localhost/docs
```

### Tests E2E

```bash
python backend/tests/utils/test_runner.py
```

---

## Prochaines Étapes

- [ ] Monitoring : Prometheus + Grafana + Loki
- [ ] Déploiement VPS réel + configuration DNS + SSH deploy
- [ ] Dashboard RH (ranking global, métriques candidats)
- [ ] Agent de recherche avancée (filtres, full-text)
- [ ] Indexation automatique des embeddings lors de l'ajout d'un candidat
