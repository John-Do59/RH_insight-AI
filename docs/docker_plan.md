# Infrastructure Docker : RH Insight AI Platform

Ce document détaille l'architecture Docker optimisée pour la production.

## 🏗️ Architecture des Services

| Service | Image Base | Rôle | Optimisation |
| :--- | :--- | :--- | :--- |
| **Backend** | `python:3.9-slim` | API FastAPI & Agents | Multi-stage build, non-root user |
| **Frontend** | `node:20-alpine` / `nginx:alpine` | App Vue.js | Multi-stage (Build Node -> Serve Nginx) |
| **Database** | `postgres:15-alpine` | Stockage PostgreSQL | Alpine base, volumes persistants |
| **Cache** | `redis:7-alpine` | Cache de latence & Sessions | Alpine base |
| **Ollama** | `ollama/ollama` | Inférence LLM locale | GPU passthrough (si disponible) |

## 🚀 Optimisations "Industrial-Grade"

1.  **Multi-Stage Builds** : Séparation des dépendances de build et de runtime pour réduire la taille des images (ex: suppression des compilateurs C après installation des libs Python).
2.  **Layers Caching** : Organisation du `Dockerfile` pour maximiser la réutilisation des layers (copy requirements d'abord).
3.  **Docker Compose Pro** :
    - Utilisation de `networks` isolés.
    - Gestion des `secrets` et `configs`.
    - `healthcheck` pour garantir l'ordre de démarrage (DB -> Backend).
4.  **Sécurité** :
    - Utilisateurs non-privilégiés dans les containers.
    - Montage en lecture seule pour les fichiers statiques.

## 🛠️ Plan d'Action

1.  **Dockerfile Backend** : Créer un build multi-étape avec `uvicorn`.
2.  **Dockerfile Frontend** : Créer un build Node.js dist servant via Nginx.
3.  **Docker Compose** : Orchestrer les 5 services.
4.  **Nginx Proxy** : (Optionnel) Ajouter un reverse proxy pour centraliser les accès.
5.  **Vérification** : Tester le déploiement local via `docker compose up`.
