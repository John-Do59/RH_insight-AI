# RH Insight AI - Assistant de Recrutement Intelligent

![RH Insight AI Cover](app/assets/cover.png)

Plateforme d'analyse et d'interaction avec les données de recrutement utilisant l'intelligence artificielle générative. Ce projet combine le traitement de documents (RAG), les requêtes structurées (SQL) et l'analyse de projets open-source (GitHub) pour offrir une vue complète sur un profil de candidat.

## Présentation du Projet

RH Insight AI est un assistant conçu pour faciliter le travail des recruteurs et des gestionnaires de talents. Il permet d'interroger à la fois le contenu textuel des CV (expériences, compétences, formations) et les données structurées (statuts, dates, informations de contact) ainsi que l'activité technique sur GitHub à travers une interface naturelle et fluide.

### Fonctionnalités Clés

- **Analyse de documents (RAG)** : Recherche sémantique et extraction d'informations directement depuis les fichiers PDF des CV.
- **Requêtes de données (SQL)** : Analyse statistique et recherche de critères précis dans la base de données des candidats.
- **Agent GitHub** : Récupération et analyse en temps réel des dépôts (publics et privés), langages et descriptions de projets.
- **Orchestration Multi-Agents** : Utilisation de LangGraph pour router les questions vers l'agent le plus pertinent avec un flux hybride séquentiel (SQL -> RAG -> GitHub).
- **Interface Premium** : Design Vue.js 3 moderne avec Tailwind/CSS natif, animations fluides et terminal interactif.
- **Support Docker** : Architecture entièrement conteneurisée pour un déploiement "plug and play".

## Architecture Technique

Le projet repose sur une architecture multi-agents moderne :

- **Moteur d'exécution** : Python 3.13+
- **Framework IA** : LangChain et LangGraph
- **Modèles de langage** : DeepSeek R1 (via Ollama)
- **Base de données Vectorielle** : Chroma (Vector Database)
- **Base de données Relationnelle** : PostgreSQL avec validation SQLAlchemy/Pydantic
- **API Externes** : GitHub REST API avec caching
- **Frontend** : Vue.js 3 avec Composition API et Pinia
- **Orchestration** : Docker et Docker Compose

## 🛠️ Installation et Démarrage

### Choix de l'Environnement (Local vs Docker)
Le projet est conçu pour fonctionner de deux manières sans conflit de configuration :

1. **Docker (Recommandé - Production)** : Lance une base de données **PostgreSQL**.
2. **Local (Développement Rapide)** : Utilise automatiquement une base de données **SQLite** via `.env`.

### ⚡ Optimisations Ollama (Mac 16Go)
Pour éviter la saturation de la mémoire unifiée (RAM/Swap) et garantir un streaming instantané (TTFT < 1s) :
- Les appels à `qwen3.5:4b` ont le mode *Thinking* désactivé (`think: False`) pour préserver les tokens.
- Le contexte LLM est optimisé (`num_ctx: 2048`, `num_predict: 512`) pour éviter de dépasser la mémoire disponible du GPU.

### Démarrage Rapide (avec Docker) (Recommandé)

1. **Cloner le projet**

   ```bash
   git clone <url-du-repo>
   cd RH_insight-AI
   ```

2. **Configuration**

   ```bash
   cp .env.example .env
   # Modifiez le fichier .env (Les modèles Ollama par défaut sont qwen3.5:4b et nomic-embed-text)
   ```

3. **Lancer l'application**

   ```bash
   docker compose up -d
   ```

4. **Initialiser les données (PostgreSQL & ChromaDB)**

   Une fois les conteneurs lancés, initialisez la base de données et ingérez les CV :
   ```bash
   docker exec rh-backend alembic upgrade head
   docker exec rh-backend python3 scripts/ingest_cv.py
   ```

L'application est maintenant accessible sur `http://localhost:5173`.
L'API Swagger est disponible sur `http://localhost:8000/docs`.

## Documentation détaillée

- [Architecture détaillée](docs/architecture.md)
- [Commandes utiles](docs/commandes_utiles.md)

## Auteur

Projet développé par Amaury Rammanat
