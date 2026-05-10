# Audit Technique & Plan de Refactorisation

Ce document synthétise l'audit du projet **RH Insight AI** avant la phase de conteneurisation.

## 🛡️ Audit de Sécurité

### 1. Failles Critiques
- **CORS Permissif** : `allow_origins=["*"]` dans `main.py`. Doit être restreint en production.
- **Secrets par défaut** : La `SECRET_KEY` est en dur dans le code (même avec un fallback `os.getenv`).
- **SQL Injection** : Le validateur est présent mais rudimentaire. Une injection complexe pourrait passer si elle utilise des fonctions non listées.

### 2. Gestion des Identités
- Pas de validation de force de mot de passe à l'inscription.
- Pas de mécanisme de rafraîchissement de token (Refresh Token).

## 🏗️ Dette Technique & Duplication

### 1. Structure de l'Arborescence
- **Obsolescence** : `backend/app/core/config.py` est en doublon avec `backend/app/config/settings.py`.
- **Incohérence** : Séparation entre `db/` et `sql/`. Devrait être unifié sous `database/` ou `db/`.
- **Clients LLM** : `llm/ollama_client.py` crée plusieurs fonctions pour la même chose.

### 2. Code Duplication
- Logique d'initialisation de base de données répétée dans `sql/database.py` et `db/session.py`.
- Templates de prompts éparpillés dans les agents sans centralisation.

## 🧹 Plan de Nettoyage (Refactoring)

1.  **Suppression** :
    - `backend/app/core/config.py` (Doublon)
    - `backend/app/core/monitoring.py` (Si déplacé dans utils)
2.  **Unification** :
    - Fusionner `db/` et `sql/` dans un package unique `database/`.
    - Centraliser les Prompts dans `backend/app/llm/prompts.py`.
3.  **Sécurisation** :
    - Mettre à jour `main.py` pour charger les domaines autorisés depuis `.env`.
    - Ajouter une validation de mot de passe dans `auth.py`.

## 🧪 Plan de Tests

### 1. Tests Unitaires (Pytest)
- Validation SQL (Security tests).
- Modèles Pydantic.
- Utilitaires de parsing.

### 2. Tests d'Intégration
- Flow Auth : Register -> Login -> Me.
- Chat Flow : Question -> Agents -> Response.
- DB Migration : Vérifier que les modèles correspondent à PostgreSQL.
