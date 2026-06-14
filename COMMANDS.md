# 🚀 RH Insight AI - Guide des Commandes (Cheatsheet)

Ce document regroupe toutes les commandes utiles pour lancer, gérer et débugger le projet **RH Insight AI**, que ce soit en local (dev) ou via Docker.

---

## 🛠 1. Lancement avec Docker (Recommandé)

Ces commandes utilisent `docker-compose.yml` pour lancer toute la stack (Frontend, Backend, Postgres+pgvector, Redis).

| Action | Commande |
| :--- | :--- |
| **Lancer tout le projet** (en tâche de fond) | `docker compose up -d` |
| **Lancer et forcer la reconstruction** des images | `docker compose up -d --build` |
| **Reconstruire uniquement le backend** sans cache | `docker compose build --no-cache backend` |
| **Arrêter le projet** (conserve les données) | `docker compose down` |
| **Arrêter et supprimer les volumes** (⚠️ reset total DB) | `docker compose down -v` |

---

## 💻 2. Lancement en Local (Développement manuel)

Si vous développez sans Docker, voici comment lancer les briques indépendamment.
*(Nécessite d'avoir au moins la base de données et redis qui tournent via Docker : `docker compose up -d db redis`)*

### Backend (FastAPI)
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Vue.js / Vite)
```bash
cd frontend/vue-app
npm run dev
```

---

## 🔍 3. Logs et Débogage Docker

Indispensable pour comprendre pourquoi un conteneur plante ou ne répond pas.

| Action | Commande |
| :--- | :--- |
| **Voir tous les logs en direct** | `docker compose logs -f` |
| **Voir les logs du Backend** | `docker logs rh-backend -f` |
| **Voir les logs du Frontend** | `docker logs rh-frontend -f` |
| **Voir les logs de la Base de Données** | `docker logs rh-postgres -f` |
| **Tester si le backend est "Healthy"** | `curl -s http://localhost:8000/health` |

---

## 🗄 4. Base de Données & Migrations (Alembic)

Commandes pour gérer le schéma PostgreSQL. À exécuter pendant que le conteneur `rh-backend` tourne.

| Action | Commande |
| :--- | :--- |
| **Appliquer les migrations** (Mettre à jour la DB) | `docker exec rh-backend alembic upgrade head` |
| **Générer une nouvelle migration** (Après un chgt de modèle)| `docker exec rh-backend alembic revision --autogenerate -m "nom"` |
| **Annuler la dernière migration** | `docker exec rh-backend alembic downgrade -1` |
| **Ouvrir une console SQL (psql)** | `docker exec -it rh-postgres psql -U postgres -d rh_insight` |

---

## 🐳 5. Gestion et Nettoyage des Images Docker

Suite à nos optimisations, l'image backend est passée de ~9GB à ~800MB. Voici comment surveiller l'espace disque.

| Action | Commande |
| :--- | :--- |
| **Voir la taille des images Docker** | `docker images` |
| **Voir l'espace disque utilisé par Docker** | `docker system df` |
| **Nettoyer les images non utilisées** (Dangling) | `docker image prune -a` |
| **Nettoyage profond** (Volumes orphelins, cache build) | `docker system prune -a --volumes` |

---

## 🧠 6. Rappel sur Ollama (Modèles Locaux)

Le backend utilise Ollama installé directement sur votre Mac (pour profiter de l'accélération matérielle de la puce M4).
Le conteneur Docker Backend communique avec votre Mac via `host.docker.internal`.

- **Vérifier qu'Ollama tourne sur le Mac** : `curl http://localhost:11434/api/tags`
- **Lancer Ollama si éteint** : Ouvrez l'application "Ollama" depuis le dossier Applications de votre Mac.
