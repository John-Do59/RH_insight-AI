# Guide d'Exécution du Projet

Ce document détaille les commandes nécessaires pour initialiser, configurer et lancer le projet **RH Insight AI**.

## 1. Préparation de l'Environnement

### Installation des dépendances Backend
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Installation des dépendances Frontend
```bash
cd frontend/vue-app
npm install
```

### Configuration des variables d'environnement
```bash
cp .env.example .env
# Éditez le fichier .env avec vos clés (GITHUB_TOKEN, SECRET_KEY, etc.)
```

## 2. Infrastructure et Services

### Ollama (LLM)
Assurez-vous qu'Ollama est lancé et que les modèles sont téléchargés :
```bash
ollama pull deepseek-r1:7b
ollama pull qwen3.5:4b
```

### PostgreSQL (Database)
Le projet utilise désormais **PostgreSQL**. Pour lancer une instance locale rapidement :
```bash
docker run --name rh-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rh_insight -p 5432:5432 -d postgres
```

## 3. Initialisation des Données
```bash
alembic upgrade head
python scripts/seed_db.py
```

### Base de données Vectorielle (Chroma)
```bash
python scripts/ingest_cv.py
```

## 3. Lancement de l'Application

### Backend (FastAPI)
```bash
# Depuis la racine
source venv/bin/activate
uvicorn backend.app.main:app --reload
```

### Frontend (Vue.js)
```bash
cd frontend/vue-app
npm run dev
```

## 4. Tests et Maintenance

### Exécution des tests unitaires
```bash
pytest tests/
```

### Profiling et Performance (Étape 5)
L'application enregistre désormais les temps de latence dans les logs :
- Intent Agent Detection
- SQL Execution (Async)
- RAG Retrieval (Async)
- LLM Streaming (DeepSeek-R1 vs Llama 1B)
