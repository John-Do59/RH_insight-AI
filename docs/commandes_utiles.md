# Commandes Utiles RH Insight AI

Ce fichier regroupe l'ensemble des commandes nécessaires pour la gestion, le développement et le déploiement du projet RH Insight AI.

💡 **Choix d'Architecture (Local vs Docker)** : Le projet est intelligemment configuré pour supporter deux modes d'exécution sans conflit :
1. **Mode Local (Sans Docker)** : Utilise automatiquement une base de données **SQLite** (définie dans `.env`). Idéal pour un développement rapide.
2. **Mode Docker (Recommandé)** : Surcharge automatiquement la configuration pour utiliser **PostgreSQL**. Idéal pour la production.

## Docker (Orchestration Globale)

Le projet utilise Docker Compose pour orchestrer l'ensemble des services (Backend, Frontend, Base de données, Redis).

### Lancement et Arrêt
- Démarrer tous les services en tâche de fond :
  ```bash
  docker compose up -d
  ```
- Démarrer les services avec rebuild (utile si vous avez modifié un `Dockerfile` ou ajouté des dépendances `pip`/`npm`) :
  ```bash
  docker compose up -d --build
  ```
- Arrêter et supprimer tous les conteneurs :
  ```bash
  docker compose down
  ```
- Arrêter les conteneurs en supprimant également les volumes (⚠️ **Supprime les données de la base de données et de ChromaDB**) :
  ```bash
  docker compose down -v
  ```

### Logs et Debug
- Afficher les logs de tous les services en temps réel :
  ```bash
  docker compose logs -f
  ```
- Afficher les logs d'un service spécifique (ex: le backend) :
  ```bash
  docker logs -f rh-backend
  ```
- Entrer dans un conteneur pour debug (ex: backend) :
  ```bash
  docker exec -it rh-backend /bin/bash
  ```

## Backend (FastAPI)

Toutes ces commandes sont à exécuter depuis la racine du projet, avec l'environnement virtuel activé (si vous ne passez pas par Docker) ou à l'intérieur du conteneur `rh-backend`.

### Initialisation et Données
- Initialiser la base de données PostgreSQL via Alembic :
  ```bash
  docker exec rh-backend alembic upgrade head
  ```
- Ingérer les CV dans la base vectorielle ChromaDB :
  ```bash
  docker exec rh-backend python3 scripts/ingest_cv.py
  ```

### Développement
- Lancer le serveur backend localement (hors Docker) :
  ```bash
  cd backend
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

## Frontend (Vue.js)

Ces commandes sont à utiliser principalement si vous développez le frontend hors de Docker.

### Gestion
- Installer les dépendances :
  ```bash
  cd frontend/vue-app
  npm install
  ```
- Lancer le serveur de développement avec Hot-Reload :
  ```bash
  cd frontend/vue-app
  npm run dev
  ```
- Construire l'application pour la production :
  ```bash
  cd frontend/vue-app
  npm run build
  ```

## Modèles IA (Ollama)

Le projet s'appuie sur Ollama fonctionnant nativement sur le Mac hôte.

- Lister les modèles téléchargés :
  ```bash
  ollama list
  ```
- Voir les modèles actuellement chargés en mémoire (GPU) :
  ```bash
  ollama ps
  ```
- Démarrer l'API Ollama (généralement géré automatiquement par l'application Mac) :
  ```bash
  ollama serve
  ```

### 🧠 Optimisations pour Qwen3.5 (Mac 16Go)
Pour éviter la saturation de la RAM (swap massif) et accélérer les réponses :
- Gardez `num_ctx: 2048` et `num_predict: 512` dans `chat_service.py`.
- **Désactivez le "thinking"** (`think: False`) lors des appels API à `qwen3.5` pour éviter que le modèle ne génère un long raisonnement interne invisible qui épuise les tokens.
