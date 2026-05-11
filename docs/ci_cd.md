# CI/CD — RH Insight AI

Ce document décrit le pipeline d'intégration continue (CI) et les pratiques de déploiement (CD) du projet.

## 1. Vue d'ensemble

Le pipeline CI est géré par **GitHub Actions** et se déclenche automatiquement sur :

- Tout `push` sur les branches `develop` et `main`
- Toute `pull_request` ciblant `develop` ou `main`

**Fichier de configuration :** `.github/workflows/ci.yml`

## 2. Configuration pytest (`pyproject.toml`)

Le projet utilise un `pyproject.toml` à la racine pour configurer pytest. Ce fichier est **essentiel pour la CI** car il résout l'erreur `ModuleNotFoundError: No module named 'backend'` sur GitHub Actions.

```toml
[tool.pytest.ini_options]
pythonpath = ["."]       # Ajoute la racine au PYTHONPATH → "from backend.app..." fonctionne
testpaths = ["backend/tests"]
asyncio_mode = "auto"
```

> **Pourquoi ?** GitHub Actions exécute pytest depuis la racine du repo. Sans `pythonpath = ["."]`, Python ne sait pas que `backend/` est un package importable.

## 3. Étapes du Pipeline CI

```
push/PR → [1. Checkout] → [2. Setup Python] → [3. Install Deps]
        → [4. Lint (flake8)] → [5. Tests Sécurité] → [6. Tests Auth]
        → [7. Suite Complète] ✅ ou ❌
```

### Détail des étapes

| Étape | Outil | Bloquant ? |
|---|---|---|
| Checkout du code | `actions/checkout@v4` | ✅ |
| Installation Python 3.11 | `actions/setup-python@v5` | ✅ |
| Installation des dépendances | `pip install -r requirements.txt` | ✅ |
| Lint erreurs critiques | `flake8 --select=E9,F63,F7,F82` | ✅ Oui |
| Lint style général | `flake8 --max-line-length=120` | ⚠️ Warn seulement |
| Tests de sécurité | `pytest backend/tests/test_security.py` | ✅ Oui |
| Tests d'authentification | `pytest backend/tests/test_auth.py` | ✅ Oui |
| Suite complète | `pytest backend/tests/` | ⚠️ Non-bloquant* |

> *Les tests dépendants d'Ollama (LLM) ne peuvent pas s'exécuter sur GitHub Actions (pas de GPU). Ils sont marqués `continue-on-error: true`.

### Service PostgreSQL en CI

Le pipeline démarre automatiquement une base **PostgreSQL 15** pour les tests :

```yaml
services:
  postgres:
    image: postgres:15-alpine
    env:
      POSTGRES_USER: rh_user
      POSTGRES_PASSWORD: rh_password
      POSTGRES_DB: rh_insight_test
```

## 3. Stratégie de Branches (Git Flow)

```
main          ← Production (protégée)
  └── develop ← Intégration (branche par défaut des PR)
        ├── feat/xxx        ← Nouvelles fonctionnalités
        ├── fix/xxx         ← Corrections de bugs
        └── chore/xxx       ← Maintenance et refactoring
```

### Règles de contribution

1. **Jamais de commit direct sur `main` ou `develop`** — toujours passer par une PR.
2. **Toute PR doit être verte sur la CI** avant d'être mergée.
3. Nommage des branches : `feat/`, `fix/`, `chore/`, `docs/`

## 4. Déploiement Local (Développement)

```bash
# Backend FastAPI (avec auto-reload)
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend Vue.js
cd frontend/vue-app && npm run dev
```

Voir [commandes_utiles.md](commandes_utiles.md) pour le détail complet.

## 5. Déploiement Production (Docker)

```bash
# Construire et lancer tous les services
docker compose up -d --build

# Appliquer les migrations de base de données
docker exec rh-backend alembic upgrade head

# Ingérer les CV dans ChromaDB
docker exec rh-backend python -m backend.scripts.ingest_cv
```

## 6. Variables d'Environnement en CI

Les secrets sont définis directement dans le fichier `ci.yml` pour les valeurs de test non-sensibles. En production sur GitHub, utiliser **GitHub Secrets** :

```
Settings → Secrets and variables → Actions → New repository secret
```

| Variable CI (test) | À ajouter en GitHub Secret pour prod |
|---|---|
| `SECRET_KEY` (valeur de test) | `SECRET_KEY` |
| `DATABASE_URL` (PostgreSQL CI) | `DATABASE_URL` |

## 7. Roadmap CI/CD (Améliorations futures)

- [ ] Ajouter `pip-audit` dans le pipeline pour scanner les CVEs des dépendances
- [ ] Ajouter `trivy` pour scanner l'image Docker à chaque build
- [ ] Créer un workflow `cd.yml` de déploiement automatique sur merge dans `main`
- [ ] Intégrer les rapports de coverage (`pytest --cov`) avec badge README
