# Plan Project 3 — Corrections de Bugs, Sécurité et Tests

> Correction de tous les bugs, failles de sécurité et ajout de tests.  
> Branche : `fix/bugs-security`

---

## Objectif

Corriger les bugs identifiés, renforcer la sécurité de l'agent SQL, compléter les fichiers manquants et mettre en place une suite de tests pour garantir la stabilité du projet.

---

## Phase 1 — Bug Critique : Conflit dans le Graph LangGraph

### 1.1 Corriger `app/graph/graph.py`

- [ ] **Supprimer la ligne 61** (`workflow.add_edge("sql", "response")`) qui entre en conflit avec le `add_conditional_edges` des lignes 50-57
- [ ] Le flow hybride (SQL → RAG → Response) est déjà géré par `add_conditional_edges`, l'edge direct est redondant et cause un comportement indéterminé
- [ ] Vérifier que le flow reste correct :
  - `intent=sql` → SQL → Response ✅
  - `intent=hybrid` → SQL → RAG → Response ✅
  - `intent=rag` → RAG → Response ✅
  - `intent=general` → Response ✅

**Correction attendue :**

```diff
- workflow.add_edge("sql", "response")
```

### 1.2 Tester le graph corrigé

- [ ] Créer `tests/test_graph.py`
- [ ] Tester chaque chemin du graph (rag, sql, hybrid, general)
- [ ] Vérifier qu'il n'y a pas de `GraphRecursionError`

---

## Phase 2 — Sécurité : Agent SQL

### 2.1 Créer `app/sql/validators.py` (fichier planifié mais jamais implémenté)

- [ ] Validation stricte des requêtes SQL :

  ```python
  BLOCKED_KEYWORDS = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "EXEC", "UNION", "--", ";"]
  ```

- [ ] Whitelist des tables autorisées : `candidates`, `skills`, `experiences`, `education`, `projects`, `languages`
- [ ] Whitelist des colonnes par table
- [ ] Bloquer les subqueries (`SELECT` dans un `SELECT`)
- [ ] Limiter la longueur maximale de la requête (500 caractères)
- [ ] Parser SQL avec `sqlparse` pour validation structurelle

### 2.2 Intégrer le validateur dans `app/agents/sql_agent.py`

- [ ] Appeler `validate_sql_query(query)` après `extract_sql()` et avant `conn.execute()`
- [ ] Si la requête est invalide, retourner un message d'erreur clair au lieu de l'exécuter
- [ ] Logger les requêtes rejetées avec le motif

### 2.3 Tests de sécurité SQL

- [ ] Créer `tests/test_sql_security.py`
- [ ] Tester les injections SQL classiques :
  - `SELECT * FROM candidates; DROP TABLE candidates;`
  - `SELECT * FROM candidates WHERE 1=1 UNION SELECT * FROM sqlite_master`
  - `SELECT * FROM candidates -- commentaire malicieux`
- [ ] Tester la whitelist de tables
- [ ] Tester les subqueries bloquées

### 2.4 Ajouter `sqlparse` aux dépendances

- [ ] Ajouter `sqlparse>=0.5.0` dans `requirements.txt`

---

## Phase 3 — Modèle d'Embeddings

### 3.1 Remplacer le modèle dans `app/rag/embeddings.py`

- [ ] Remplacer `all-MiniLM-L6-v2` (anglophone) par un modèle adapté au français :
  - Option 1 : `paraphrase-multilingual-MiniLM-L12-v2` (multilingue, recommandé)
  - Option 2 : `dangvantuan/sentence-camembert-large` (spécialisé français)
- [ ] Tester la qualité de la recherche sémantique avec le nouveau modèle

### 3.2 Regénérer le vector store

- [ ] Supprimer l'ancien vector store (`data/vector_store/`)
- [ ] Relancer `python scripts/ingest_cv.py` avec le nouveau modèle
- [ ] Vérifier que la recherche sémantique fonctionne correctement

### 3.3 Tests du RAG

- [ ] Créer `tests/test_rag.py`
- [ ] Tester la recherche sémantique avec des questions en français
- [ ] Comparer la pertinence des résultats avant/après changement de modèle

---

## Phase 4 — Corrections Mineures

### 4.1 Corriger le nom de fichier photo

- [ ] Dans `app/streamlit_app.py` ligne 34 : renommer le fichier `app/assets/photo_amaury.jpg .png` → `app/assets/photo_amaury.png` (supprimer l'espace)
- [ ] Mettre à jour la référence dans le code

### 4.2 Ajouter les dépendances manquantes dans `requirements.txt`

- [ ] Ajouter `langchain-huggingface` (utilisé par `embeddings.py` mais absent)
- [ ] Ajouter `langchain-text-splitters` (utilisé par `chunking.py`)
- [ ] Piner les versions majeures pour la reproductibilité :

  ```txt
  langchain>=0.3.0
  langgraph>=0.2.0
  langchain-ollama>=0.2.0
  langchain-huggingface>=0.1.0
  langchain-text-splitters>=0.3.0
  chromadb>=0.5.0
  sqlalchemy>=2.0.0
  sqlparse>=0.5.0
  ```

### 4.3 Optimiser le client LLM (`app/llm/ollama_client.py`)

- [ ] Implémenter un pattern singleton pour éviter de recréer l'instance à chaque appel

  ```python
  _llm_instance = None
  
  def get_llm():
      global _llm_instance
      if _llm_instance is None:
          _llm_instance = ChatOllama(...)
      return _llm_instance
  ```

### 4.4 Ajouter les fichiers manquants

- [ ] Créer `app/graph/router.py` (planifié dans `plan_Project.md` mais jamais créé — extraire la logique de routage de `graph.py`)
- [ ] Créer `app/sql/validators.py` (cf. Phase 2)
- [ ] Créer `docs/architecture.md` avec le diagramme d'architecture
- [ ] Créer `docs/decisions.md` avec les choix techniques justifiés

---

## Phase 5 — Suite de Tests

### 5.1 Installer les outils de test

- [ ] Ajouter `pytest>=8.0.0` et `pytest-cov` dans `requirements.txt` (section dev)

### 5.2 Créer les fichiers de test

- [ ] `tests/test_graph.py` — Test du graph LangGraph (chaque chemin)
- [ ] `tests/test_router.py` — Test de la classification d'intention
- [ ] `tests/test_sql_agent.py` — Test de l'agent SQL (génération + exécution)
- [ ] `tests/test_sql_security.py` — Tests d'injection SQL
- [ ] `tests/test_rag.py` — Test de la recherche sémantique RAG
- [ ] `tests/test_preprocess.py` — Test du nettoyage de texte

### 5.3 Exécuter et valider

- [ ] `python -m pytest tests/ -v --cov=app`
- [ ] Objectif : couverture minimale de 60%
- [ ] Tous les tests doivent passer avant merge

---

## Ordre de Priorité

| Priorité | Phase | Risque |
|----------|-------|--------|
| 🔴 P0 | Phase 1 — Bug graph.py | Comportement indéterminé en production |
| 🔴 P0 | Phase 2 — Sécurité SQL | Injection SQL possible |
| 🟡 P1 | Phase 3 — Embeddings | Dégradation qualité recherche FR |
| 🟢 P2 | Phase 4 — Corrections mineures | Maintenance et robustesse |
| 🟢 P2 | Phase 5 — Tests | Couverture et CI/CD |

---

## Commandes de Validation

```bash
# Lancer tous les tests
python -m pytest tests/ -v

# Avec couverture
python -m pytest tests/ -v --cov=app --cov-report=term-missing

# Test spécifique sécurité
python -m pytest tests/test_sql_security.py -v

# Regénérer le vector store après changement modèle
rm -rf data/vector_store/
python scripts/ingest_cv.py
```
