# Plan Project 2 — Architecture Multi-Agents avec Routage

> Base de connaissances multi-sources avec routeur intelligent.  
> Branche : `feature/multi-agent-router`

---

## Objectif

Transformer le chatbot actuel (RAG + SQL) en une **plateforme multi-agents** capable de :

1. **Router** les questions vers des agents spécialisés
2. **Interroger GitHub** sur les projets du candidat en temps réel
3. **Scraper/rechercher des offres d'emploi** via API
4. **Synthétiser** les réponses de multiples sources en une réponse cohérente

---

## Architecture Cible

```
User Input
    ↓
🧠 Router Agent (classification multi-domaine)
    ↓
┌──────────┬──────────┬──────────┬──────────┐
│ cv_rag   │ cv_sql   │ github   │ jobs     │
│ 📄 RAG   │ 🗃️ SQL   │ 🐙 GitHub│ 💼 Jobs  │
│ Agent    │ Agent    │ Agent    │ Scraper  │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┘
     └──────────┴──────────┴──────────┘
                    ↓
            ✨ Synthesis Agent
                    ↓
               Réponse finale
```

---

## Étapes d'Implémentation

### Phase 1 — Préparation de l'architecture (2-3h)

#### 1.1 Mise à jour du State (`app/graph/state.py`)

- [ ] Ajouter le champ `github_data: Any` pour les données GitHub
- [ ] Ajouter le champ `job_results: List[Dict]` pour les offres d'emploi
- [ ] Ajouter le champ `agent_sources: List[str]` pour tracer quels agents ont répondu

#### 1.2 Mise à jour des constantes (`app/config/constants.py`)

- [ ] Ajouter `INTENT_GITHUB = "github"`
- [ ] Ajouter `INTENT_JOBS = "jobs"`
- [ ] Ajouter les rôles agents `ROLE_GITHUB` et `ROLE_JOBS`

#### 1.3 Mise à jour de la config (`app/config/settings.py`)

- [ ] Ajouter `GITHUB_TOKEN` (optionnel, via `.env`)
- [ ] Ajouter `GITHUB_USERNAME = "John-Do59"`
- [ ] Ajouter `ADZUNA_APP_ID` et `ADZUNA_APP_KEY` (via `.env`)
- [ ] Ajouter `FRANCE_TRAVAIL_CLIENT_ID` et `FRANCE_TRAVAIL_CLIENT_SECRET` (via `.env`)

#### 1.4 Mise à jour du `.env.example`

- [ ] Ajouter les variables d'environnement pour GitHub et Job APIs

---

### Phase 2 — Agent GitHub (3-4h)

#### 2.1 Créer `app/agents/github_agent.py`

- [ ] Fonction `github_agent(state)` compatible LangGraph
- [ ] Appel API GitHub REST (`https://api.github.com/users/John-Do59/repos`)
- [ ] Extraction des infos pertinentes :
  - Nom du repo, description, langages, date de dernière activité
  - README.md (contenu résumé)
  - Nombre de commits, stars, forks
- [ ] Cache local (éviter les appels API à chaque question)
- [ ] Gestion de la rate limit GitHub (60 req/h sans token, 5000 avec token)

#### 2.2 Créer `app/github/github_client.py`

- [ ] Classe `GitHubClient` encapsulant les appels API
- [ ] Méthodes :
  - `get_repos()` → liste des repositories publics
  - `get_repo_details(repo_name)` → détails d'un repo spécifique
  - `get_repo_readme(repo_name)` → contenu du README
  - `get_repo_languages(repo_name)` → stack technique
- [ ] Gestion des erreurs et timeout
- [ ] Cache avec TTL (1 heure)

#### 2.3 Tests

- [ ] Créer `tests/test_github_agent.py`
- [ ] Mock des appels API GitHub
- [ ] Tester la récupération des repos
- [ ] Tester la gestion des erreurs (rate limit, repo inexistant)

---

### Phase 3 — Agent Job Scraper (4-5h)

#### 3.1 Créer `app/agents/job_scraper_agent.py`

- [ ] Fonction `job_scraper_agent(state)` compatible LangGraph
- [ ] Extraction de mots-clés de la question pour la recherche
- [ ] Paramètres par défaut : localisation = "Lille", domaine = "IA / Data / Développeur"
- [ ] Fusion et déduplication des résultats multi-sources
- [ ] Formatage des offres pour le LLM (titre, entreprise, lieu, date, lien)

#### 3.2 Créer `app/jobs/france_travail_client.py`

- [ ] Authentification OAuth2 sur `entreprise.francetravail.fr`
- [ ] Recherche d'offres via l'API Offres d'emploi v2
- [ ] Filtrage par :
  - Mots-clés (développeur IA, data analyst, data scientist)
  - Localisation (Lille, Hauts-de-France)
  - Type de contrat (alternance, CDI, CDD)
- [ ] Parsing de la réponse JSON

#### 3.3 Créer `app/jobs/adzuna_client.py`

- [ ] Appel API Adzuna (`api.adzuna.com/v1/api/jobs/fr/search`)
- [ ] Paramètres : keywords, location, category
- [ ] Parsing et normalisation des résultats
- [ ] Fallback si France Travail est indisponible

#### 3.4 Tests

- [ ] Créer `tests/test_job_agent.py`
- [ ] Mock des APIs France Travail et Adzuna
- [ ] Tester la recherche, le filtrage et la déduplication
- [ ] Tester les cas d'erreur (API down, quota dépassé)

---

### Phase 4 — Router et Orchestration (3-4h)

#### 4.1 Mettre à jour `app/agents/intent_agent.py`

- [ ] Étendre le prompt de classification pour inclure `github` et `jobs`
- [ ] Ajouter des exemples de questions pour chaque nouvelle catégorie :
  - `github` : "Montre-moi tes projets GitHub", "Quels repos as-tu ?", "Ton code est dispo ?"
  - `jobs` : "Y a-t-il des offres en IA à Lille ?", "Cherche des alternances data", "Le marché de l'emploi IA ?"
- [ ] Gérer le mode `hybrid` étendu (ex: "Montre tes projets GitHub et les offres qui matchent")

#### 4.2 Refactorer `app/graph/graph.py`

- [ ] Ajouter les nœuds `github` et `jobs`
- [ ] Mettre à jour le routeur conditionnel avec les nouvelles routes
- [ ] Implémenter le flow hybride multi-agents :

  ```
  hybrid → parallel(sql, rag, github?) → synthesis
  ```

- [ ] Corriger le bug existant (conflit `add_conditional_edges` / `add_edge` sur SQL)

#### 4.3 Mettre à jour `app/agents/response_agent.py`

- [ ] Étendre `build_context()` pour inclure `github_data` et `job_results`
- [ ] Ajouter `build_github_prompt()` pour les questions GitHub
- [ ] Ajouter `build_jobs_prompt()` pour les questions offres d'emploi
- [ ] Gérer la synthèse multi-sources (quand hybrid + plusieurs agents)

#### 4.4 Tests d'intégration

- [ ] Créer `tests/test_router_extended.py`
- [ ] Tester le routage vers chaque agent
- [ ] Tester les flux hybrides
- [ ] Vérifier qu'aucune régression sur RAG/SQL

---

### Phase 5 — UI et intégration finale (2-3h)

#### 5.1 Mettre à jour `app/streamlit_app.py`

- [ ] Ajouter les exemples de questions GitHub et Jobs dans les suggestion cards
- [ ] Afficher la source de la réponse dans le panneau Debug (quel(s) agent(s) ont répondu)
- [ ] Icône/badge indiquant la source (📄 RAG, 🗃️ SQL, 🐙 GitHub, 💼 Jobs)
- [ ] Afficher les offres d'emploi avec des cartes cliquables (lien vers l'offre)

#### 5.2 Mettre à jour `requirements.txt`

- [ ] Ajouter `httpx` (pour les appels API)
- [ ] Ajouter `cachetools` (pour le cache TTL)

#### 5.3 Documentation

- [ ] Mettre à jour `README.md` avec la nouvelle architecture
- [ ] Créer `docs/architecture.md` avec le diagramme mis à jour
- [ ] Documenter les variables d'environnement nécessaires

---

## Dépendances à Installer

```txt
httpx>=0.27.0        # Client HTTP async pour les APIs
cachetools>=5.3.0    # Cache avec TTL pour GitHub/Jobs
```

---

## Variables d'environnement requises

```env
# GitHub (optionnel, augmente la rate limit)
GITHUB_TOKEN=ghp_xxxxx
GITHUB_USERNAME=John-Do59

# France Travail API
FRANCE_TRAVAIL_CLIENT_ID=xxxxx
FRANCE_TRAVAIL_CLIENT_SECRET=xxxxx

# Adzuna API
ADZUNA_APP_ID=xxxxx
ADZUNA_APP_KEY=xxxxx
```

---

## Estimation Totale : ~15-20h de développement
