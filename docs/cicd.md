# CI/CD GitHub Actions — Build & Push GHCR

> **Statut** : Implémenté ✅  
> **Branche** : `feature/cicd-production-ready`  
> **Fichier** : `.github/workflows/cd.yml`

---

## Vue d'ensemble

Le pipeline CI/CD automatise le cycle de build et de déploiement :

```
git push main
      ↓
GitHub Actions : Tests + Lint
      ↓
Docker Build (Backend + Frontend)
      ↓
Push → GHCR (ghcr.io/<user>/rh-backend:latest)
      ↓
[futur] VPS : docker compose pull && up -d
```

---

## Déclencheur

```yaml
on:
  push:
    branches:
      - main
```

Le pipeline se déclenche uniquement sur la branche `main`.

---

## Job 1 : Tests & Linting

### Service PostgreSQL de test

Un service PostgreSQL avec pgvector est démarré temporairement pour les tests :

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    env:
      POSTGRES_USER: rh_user
      POSTGRES_PASSWORD: rh_password
      POSTGRES_DB: rh_insight_test
    options: --health-cmd pg_isready
```

### Variables d'environnement CI

```yaml
env:
  DATABASE_URL: postgresql://rh_user:rh_password@localhost:5432/rh_insight_test
  SECRET_KEY: ci-test-secret-key
```

### Étapes

1. **Checkout** du code
2. **Setup Python 3.11** avec cache pip
3. **Installation** des dépendances + `flake8` + `pytest`
4. **Lint** : `flake8` bloquant sur les erreurs critiques (`E9`, `F63`, etc.)
5. **Tests** : `pytest backend/tests/ -v --tb=short`

> Note : `continue-on-error: true` sur les tests pour gérer les cas où Ollama n'est pas disponible en CI.

---

## Job 2 : Build & Push GHCR

### Authentification

Utilise le `GITHUB_TOKEN` automatique (pas de secret supplémentaire nécessaire) :

```yaml
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

### Images produites

| Image | Tags |
|---|---|
| `ghcr.io/<user>/rh_insight-ai-backend` | `latest`, `sha-<short_commit>` |
| `ghcr.io/<user>/rh_insight-ai-frontend` | `latest`, `sha-<short_commit>` |

Le double tagging `latest` + `sha` permet :
- Rollback immédiat vers n'importe quelle version
- Traçabilité précise (quel commit a produit quelle image)

### Configuration

```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    file: backend/Dockerfile
    push: true
    tags: ${{ steps.meta-backend.outputs.tags }}
```

---

## Utilisation des images GHCR sur VPS

Pour utiliser les images pré-buildées au lieu du build local, modifier `docker-compose.prod.yml` :

```yaml
# Remplacer le bloc `build:` par :
backend:
  image: ghcr.io/<user>/rh_insight-ai-backend:latest
```

```bash
# Sur le VPS
echo $GHCR_TOKEN | docker login ghcr.io -u <user> --password-stdin
docker compose -f docker/docker-compose.prod.yml pull
docker compose -f docker/docker-compose.prod.yml up -d
```

---

## Étape suivante : Déploiement automatique VPS

Pour compléter le pipeline avec un déploiement SSH automatique, ajouter un job supplémentaire :

```yaml
deploy:
  needs: build-and-push
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to VPS
      uses: appleboy/ssh-action@v1
      with:
        host: ${{ secrets.VPS_HOST }}
        username: ${{ secrets.VPS_USER }}
        key: ${{ secrets.VPS_SSH_KEY }}
        script: |
          cd /opt/rh-insight-ai
          docker compose -f docker/docker-compose.prod.yml pull
          docker compose -f docker/docker-compose.prod.yml up -d --remove-orphans
```

> Secrets à configurer dans GitHub : `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`
