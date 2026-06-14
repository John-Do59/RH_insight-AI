# Infrastructure Docker — Guide Complet

> **Statut** : Implémenté ✅  
> **Branche** : `feature/docker-production-infrastructure`

---

## Vue d'ensemble

L'infrastructure Docker de RH Insight AI est conçue pour fonctionner à trois niveaux :

| Environnement | Fichier | Usage |
|---|---|---|
| **Développement** | `docker/docker-compose.dev.yml` | Hot-reload, ports exposés, volumes locaux |
| **Simulation VPS** | `docker/docker-compose.local-prod.yml` | Test prod en local, Traefik actif |
| **Production VPS** | `docker/docker-compose.prod.yml` | Déploiement serveur, HTTPS Let's Encrypt |

---

## 1. Services Docker

### Backend (FastAPI)

- **Dockerfile** : `backend/Dockerfile`
- **Build** : Multi-stage (`python:3.11-slim` builder → runtime)
- **Optimisations** :
  - Couche `requirements.txt` séparée pour maximiser le cache des layers
  - Virtual environment isolé dans `/opt/venv`
  - Utilisateur non-root `appuser` pour la sécurité
  - `libpq5` uniquement (pas les dev headers) en runtime
- **Runtime** : `uvicorn` avec 4 workers en production

```dockerfile
# Exemple commande prod
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers"]
```

### Frontend (Vue.js + Nginx)

- **Dockerfile** : `frontend/Dockerfile`
- **Build** : Multi-stage (`node:18-alpine` builder → `nginx:alpine` runtime)
- **Configuration Nginx** : `frontend/nginx.conf`
  - Gzip activé (JS, CSS, SVG, fonts)
  - Cache assets statiques : 1 an (`Cache-Control: immutable`)
  - Fallback SPA : `try_files $uri $uri/ /index.html`

### PostgreSQL + pgvector

```yaml
image: pgvector/pgvector:pg16
```

- Extension `vector` disponible nativement
- Volume persistant : `postgres_data`
- Healthcheck : `pg_isready`
- Config prod : `max_connections=200`, `shared_buffers=256MB`

### Redis

```yaml
image: redis:7-alpine
```

- Usage futur : cache embeddings, queues LangGraph
- Volume persistant : `redis_data`

---

## 2. Réseau Docker

Tous les services partagent un réseau bridge isolé :

```yaml
networks:
  rh-insight-net:
    driver: bridge
```

En production, **aucun port backend/DB n'est exposé** directement sur l'hôte. Seul Traefik expose les ports 80 et 443.

---

## 3. Volumes

| Volume | Service | Contenu |
|---|---|---|
| `postgres_data` | PostgreSQL | Données métier |
| `redis_data` | Redis | Cache |
| `traefik_certificates` | Traefik | Certificats Let's Encrypt |

---

## 4. Configuration via `.env`

Aucun secret dans les images Docker. Toutes les variables sensibles sont injectées via un fichier `.env` à la racine :

```env
POSTGRES_USER=rh_user
POSTGRES_PASSWORD=<secret>
POSTGRES_DB=rh_insight
SECRET_KEY=<jwt_secret>
DOMAIN=mondomaine.com
ACME_EMAIL=admin@mondomaine.com
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

---

## 5. Environnement de Développement

```bash
docker compose -f docker/docker-compose.dev.yml up
```

**Spécificités dev** :
- Backend avec `--reload` activé
- Volume bind-mount `../backend:/app/backend` pour hot-reload
- Frontend via `node:18-alpine` + `npm run dev`
- Ports exposés localement : `8000` (API), `5173` (Vue), `5432` (Postgres), `6379` (Redis)
- `host.docker.internal:host-gateway` pour accéder à Ollama sur la machine hôte

---

## 6. Simulation VPS Locale

```bash
docker compose -f docker/docker-compose.local-prod.yml up -d
```

**Comportement identique à un VPS** :
- Traefik route `localhost/api` → Backend, `localhost/` → Frontend
- Aucun port backend exposé directement
- Images buildées depuis les Dockerfiles locaux (ou GHCR en prod)

---

## 7. Déploiement VPS Production

```bash
# Sur le VPS, après push GHCR
docker compose -f docker/docker-compose.prod.yml pull
docker compose -f docker/docker-compose.prod.yml up -d
```

> HTTPS est géré automatiquement par Traefik + Let's Encrypt dès que le domaine pointe vers l'IP du serveur.
