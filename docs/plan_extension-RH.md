# Plan d'Implémentation : Extension RH (Recherche Multi-Candidats)

Ce document détaille la stratégie pour transformer l'assistant initialement conçu pour un profil unique en un outil de recrutement capable de gérer et d'interroger une base de multiples candidats.

## Objectifs de l'extension

- Permettre la recherche sémantique multi-profils via RAG.
- Automatiser le scoring des candidats par rapport à une requête spécifique.
- Maintenir l'interaction vocale pour la restitution des résultats.

## Modifications Structurales

### 1. Ingestion des données (scripts/ingest_cv.py)

Actuellement, les données sont traitées sans distinction forte de profil.

- **Action** : Garantir que chaque chunk dans la base vectorielle Chroma possède une métadonnée `candidate_id` correspondant à l'ID généré dans la base SQLite lors de l'ingestion.

### 2. Classification des intentions (app/agents/intent_agent.py)

Le système doit maintenant distinguer une question sur un profil précis d'une recherche transversale.

- **Nouvelle catégorie** : `hr_search` (ex: "Quels candidats maîtrisent le Machine Learning ?").

### 3. Nouvel Agent RH (app/agents/hr_agent.py)

Développement d'un agent spécialisé pour :

- Effectuer une recherche de similarité sur l'ensemble de la base documentaire.
- Agréger les scores de pertinence par candidat.
- Croiser les résultats avec les données structurées SQL (Identité, Contact).
- Générer un résumé comparatif des profils les plus adaptés.

### 4. Interface Utilisateur (app/streamlit_app.py)

- Refonte de l'affichage pour présenter les candidats sous forme de liste avec scores de matching.
- Intégration de la synthèse vocale pour annoncer les meilleurs profils trouvés.

## Complexité et Limitations

- **Volume** : Le résumé par LLM est limité aux 3-5 meilleurs profils pour des raisons de performance (DeepSeek R1).
- **Précision** : La pertinence dépendra de la qualité du découpage (chunking) et de l'indexation initiale.
