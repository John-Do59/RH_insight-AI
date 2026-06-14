# Tests E2E — Matching Engine

> **Statut** : Implémenté ✅  
> **Branche** : `feature/matching-engine-e2e-tests`

---

## Structure des Tests

```
backend/tests/
├── e2e/
│   ├── test_mock_data_factory.py     → Validation du seeding
│   ├── test_matching_pipeline.py     → Pipeline complet LangGraph
│   ├── test_cache_behavior.py        → Stratégie de cache
│   └── test_matching_consistency.py  → Stabilité des résultats IA
└── utils/
    ├── mock_embeddings.py            → Générateur d'embeddings mock 768d
    ├── seed_database.py              → Injecteur de données de test
    └── test_runner.py                → Runner global avec rapport
```

---

## Données de Test

Le seeder injecte un jeu de données RH réaliste :

**Candidats** :
- Data Engineer Python (4 ans, compétences : Python, SQL)
- Fullstack JS (3 ans)
- Backend FastAPI (5 ans, compétences : FastAPI, Python)

**Offres** :
- Data Engineer (requiert : Python, Airflow)
- Backend Engineer (requiert : FastAPI, Docker)

**Compétences** : Python, Docker, FastAPI, Airflow, Kubernetes, SQL, ML, NLP

**Embeddings** : Vecteurs aléatoires normalisés 768 dimensions (compatible pgvector sans dépendance modèle IA)

---

## Lancer les Tests

### Option 1 — Test Runner global (recommandé)

```bash
cd /Users/amaury/RH_insight-AI
source venv/bin/activate
python backend/tests/utils/test_runner.py
```

**Sortie attendue** :
```
========================================
RH Insight AI - Matching Engine Test Suite
========================================

[1/4] Seeding the mock database...
✔ Database seeded successfully.

[2/4] Running E2E Test Suite...
...
✔ Matching pipeline OK
✔ Cache behavior OK
✔ Consistency OK
✔ No critical failures

SUCCESS RATE: 100%

Status: STABLE | Tests: PASSED | Pipeline: OPERATIONAL | Cache: ACTIVE
```

### Option 2 — pytest directement

```bash
# Seeder d'abord
python backend/tests/utils/seed_database.py

# Lancer un test spécifique
pytest backend/tests/e2e/test_matching_pipeline.py -v

# Tous les tests E2E
pytest backend/tests/e2e/ -v --tb=short
```

---

## Description des Tests

### `test_mock_data_factory.py`

Valide que le seeding a correctement injecté les entités en base.

**Assertions** :
- `len(candidates) > 0`
- `len(jobs) > 0`
- `len(skills) > 0`
- `len(candidate.embedding) == 768`

---

### `test_matching_pipeline.py`

Exécute le pipeline complet LangGraph pour un candidat et une offre.

**Assertions** :
- La réponse contient `final_score`, `strengths`, `gaps`, `explanation`
- `0 <= score <= 100`
- `intersection(strengths, gaps) == ∅` (logique métier)

---

### `test_cache_behavior.py`

**Scénario** :
1. Nettoie le cache pour la paire testée
2. Premier appel → LangGraph exécuté, score calculé, enregistré en DB
3. Deuxième appel → récupération DB directe

**Assertions** :
- Le cache est présent après le premier appel
- Le score est identique
- La latence du second appel est inférieure à 100ms

---

### `test_matching_consistency.py`

Exécute deux fois le même matching et compare les résultats.

**Assertions** :
- `|score1 - score2| ≤ 2.0` (variance LLM acceptable)
- `set(strengths1) == set(strengths2)` (compétences stables)
- `set(gaps1) == set(gaps2)` (gaps stables)

> Note : La stabilité est haute car `skill_comparison_node` est déterministe. La variance peut venir uniquement du `llm_score` (poids : 5%).

---

## Embeddings Mock

Le module `mock_embeddings.py` génère des vecteurs normalisés sans dépendance externe :

```python
def generate_mock_embedding(dim: int = 768) -> list[float]:
    vec = np.random.rand(dim)
    return (vec / np.linalg.norm(vec)).tolist()
```

Cela permet d'exécuter les tests en CI sans Ollama ni modèle d'embedding.
