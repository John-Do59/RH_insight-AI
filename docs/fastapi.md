# Aide-mémoire FastAPI (Backend)

Ce document récapitule les commandes essentielles pour le développement backend avec FastAPI.

## 1. Environnement Virtuel

```bash
# Créer l'environnement
python3 -m venv venv

# Activer l'environnement (Mac/Linux)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 2. Lancement du Serveur

```bash
# Lancer avec rechargement automatique (Dev)
uvicorn backend.app.main:app --reload

# Lancer sur un port spécifique
uvicorn backend.app.main:app --port 8080

# Lancer avec plusieurs workers (Prod)
uvicorn backend.app.main:app --workers 4
```

## 3. Documentation API (Automatique)

Une fois le serveur lancé :
- **Swagger UI** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc** : [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 4. Commandes Utiles

```bash
# Vérifier les dépendances installées
pip list

# Générer un nouveau requirements.txt
pip freeze > requirements.txt

# Lancer les tests avec Pytest
pytest
```

## 5. Variables d'Environnement

Le projet utilise `python-dotenv`. Assurez-vous d'avoir un fichier `.env` à la racine contenant :
- `DATABASE_URL`
- `GITHUB_TOKEN`
- `SECRET_KEY`
- `OLLAMA_BASE_URL`
