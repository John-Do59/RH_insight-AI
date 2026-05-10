# Guide d'Exécution du Projet

Ce document détaille les commandes nécessaires pour initialiser, configurer et lancer le projet **RH Insight AI**.

## 1. Préparation de l'Environnement

### Installation des dépendances
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration des variables d'environnement
```bash
cp .env.example .env
# Éditez le fichier .env avec vos clés (GitHub, etc.)
```

## 2. Initialisation des Données

Avant de lancer l'application, les bases de données doivent être préparées.

### Base de données SQL (SQLite)
Initialise la structure et insère des données de test pour les candidats.
```bash
python scripts/init_db.py
python scripts/seed_db.py
```

### Base de données Vectorielle (Chroma)
Indexe les fichiers PDF présents dans le dossier `data/cv/`.
```bash
python scripts/ingest_cv.py
```

## 3. Lancement de l'Application

### Via Streamlit (Recommandé)
```bash
streamlit run app/streamlit_app.py
```

### Via le script d'automatisation
```bash
bash run.sh
```

## 4. Tests et Maintenance

### Exécution des tests unitaires
```bash
pytest tests/
```

### Vérification de l'indexation
Vous pouvez vérifier le nombre de documents indexés dans Chroma :
```bash
python scripts/check_vector_store.py
```
