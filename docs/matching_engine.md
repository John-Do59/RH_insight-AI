# Matching Engine — Moteur IA de Compatibilité

> **Statut** : Implémenté ✅  
> **Branche** : `feature/matching-engine-v1`

---

## Vue d'ensemble

Le Matching Engine est le **cœur métier de RH Insight AI**. Il calcule automatiquement un score de compatibilité entre un candidat et une offre d'emploi, avec explication IA.

---

## Architecture du Pipeline

```
POST /api/match
      ↓
Cache check (candidate_job_matches)
      ↓ [si pas en cache]
LangGraph Matching Agent
      ├── load_data     → Candidat + Job + Skills (Postgres)
      ├── vector_retrieval → Score cosine (pgvector)
      ├── skill_comparison → Gaps & Matches
      ├── reasoning     → LLM (explication + llm_score)
      └── scoring       → Score final hybride
      ↓
Sauvegarde en DB (cache)
      ↓
Response JSON
```

---

## Fichiers Implémentés

| Fichier | Rôle |
|---|---|
| `backend/app/graph/matching_state.py` | Définition du `TypedDict` d'état LangGraph |
| `backend/app/graph/matching_nodes.py` | Implémentation des 5 nœuds du pipeline |
| `backend/app/graph/matching_graph.py` | Compilation du graphe LangGraph |
| `backend/app/api/api_v1/endpoints/match.py` | API REST (`POST /match`, `GET /match/...`) |

---

## Formule de Scoring Hybride

```
final_score =
  0.40 × vector_score     (similarité cosine embeddings pgvector)
+ 0.30 × skill_score      (ratio compétences matchées / requises)
+ 0.15 × experience_score (ratio années expérience)
+ 0.10 × github_score     (activité GitHub, si disponible)
+ 0.05 × llm_score        (note du LLM sur la cohérence globale)
```

> Si le profil GitHub est absent, les poids sont renormalisés automatiquement.

---

## Nœuds LangGraph

### 1. `load_data_node`

Charge depuis PostgreSQL :
- `Candidate` (titre, expérience, embedding, résumé)
- `Job` (titre, description, embedding)
- `Skill` associés au candidat et à l'offre via les tables de liaison
- `GithubProfile` si disponible

### 2. `vector_retrieval_node`

Calcule la similarité cosine entre les embeddings du candidat et de l'offre :

```python
similarity = dot(v1, v2) / (norm(v1) * norm(v2))
vector_score = max(0.0, similarity) * 100
```

### 3. `skill_comparison_node`

```python
matched = job_skills ∩ candidate_skills
missing = job_skills - candidate_skills
skill_score = len(matched) / len(job_skills) * 100
```

Calcule aussi `experience_score` et `github_score`.

### 4. `reasoning_node`

Appelle le LLM via `ollama_client` avec un prompt expert RH. Retourne un JSON structuré :

```json
{
  "strengths": ["Python", "Docker"],
  "gaps": ["Airflow"],
  "explanation": "Le candidat présente...",
  "llm_score": 85
}
```

**Fallback** : Si le LLM est indisponible ou retourne du JSON invalide, les `strengths`/`gaps` sont remplacés par les listes algorithmiques de `skill_comparison_node`.

### 5. `scoring_node`

Applique la formule hybride et normalise le score entre 0 et 100.

---

## API Endpoints

### `POST /api/match`

```json
// Request
{ "candidate_id": "uuid", "job_id": "uuid" }

// Response
{
  "candidate_id": "...",
  "job_id": "...",
  "score": 87.4,
  "strengths": ["Python", "FastAPI"],
  "gaps": ["Airflow"],
  "explanation": "...",
  "computed_at": "2026-06-12T22:00:00"
}
```

### `GET /api/match/candidate/{candidate_id}`

Retourne tous les matchs pré-calculés pour un candidat, triés par score décroissant.

### `GET /api/match/job/{job_id}`

Retourne les candidats correspondant à une offre, triés par score décroissant.

---

## Cache (table `candidate_job_matches`)

- Clé : `(candidate_id, job_id)` unique
- **Premier appel** : LangGraph exécuté, résultat sauvegardé
- **Appels suivants** : récupération directe depuis la DB (< 10ms)
- **Invalidation** : manuelle pour l'instant (à automatiser lors de modification du CV/offre)

---

## Job Intake Chat Agent

> Extension du Matching Engine pour l'interface conversationnelle.

**Fichiers** :
- `backend/app/graph/job_parser.py` : Parser LLM → JSON structuré
- `backend/app/api/api_v1/endpoints/job_agent.py` : `POST /job-agent/analyze`
- `frontend/vue-app/src/views/JobAgentView.vue` : Interface chat

**Flow** :
1. L'utilisateur colle une offre brute en texte
2. Le LLM extrait `{title, skills, experience, location}`
3. Les candidats sont récupérés (SQL + pgvector)
4. Chaque candidat est scoré via `skill_comparison_node` + `reasoning_node` + `scoring_node`
5. Les 5 meilleurs profils sont retournés avec score, forces et manques
