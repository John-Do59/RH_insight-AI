# RH Insight AI — Vision Produit & Plan d'Évolution

## Objectif

Transformer RH Insight AI d'un simple chatbot RAG basé sur un CV personnel en une plateforme RH intelligente multi-agents capable d'assister les recruteurs dans la recherche, l'analyse, le matching et l'évaluation des candidats.

---

# Problème Actuel

L'application actuelle fonctionne principalement comme un assistant conversationnel connecté à un seul CV.

Architecture actuelle :

```text
CV Personnel
     ↓
    RAG
     ↓
 Chatbot IA
```

Limites :

* Un seul candidat est analysé.
* L'IA répond en se faisant passer pour le candidat.
* Peu de valeur métier pour un recruteur.
* Difficulté à démontrer un véritable cas d'usage RH.
* Scalabilité fonctionnelle limitée.

---

# Vision Cible

RH Insight AI doit devenir un copilote RH intelligent capable de :

* Analyser plusieurs candidats.
* Analyser plusieurs offres d'emploi.
* Réaliser du matching automatisé.
* Évaluer les compétences techniques.
* Interroger une base de candidats en langage naturel.
* Produire des recommandations RH exploitables.

Architecture cible :

```text
                    Recruteur
                         │
                         ▼
                  LangGraph Router
                         │
     ┌───────────────────┼───────────────────┐
     ▼                   ▼                   ▼
 CV Agent          Job Agent          Analytics Agent
     │                   │                   │
     └───────────┬───────┴───────────┬───────┘
                 ▼                   ▼
          Matching Agent      GitHub Agent
                 │
                 ▼
             PostgreSQL
              + pgvector
```

---

# Objectifs Fonctionnels

## 1. Recherche Sémantique de Candidats

Permettre à un recruteur de rechercher des profils en langage naturel.

Exemples :

* Trouve-moi un développeur Python à Lille.
* Quels candidats maîtrisent FastAPI et Docker ?
* Montre-moi les profils ayant une expérience en IA générative.

Le système doit :

1. Comprendre l'intention.
2. Filtrer les métadonnées.
3. Effectuer une recherche vectorielle.
4. Réordonner les résultats.
5. Présenter les meilleurs candidats.

---

## 2. Matching Automatique CV ↔ Offre

Le système doit calculer automatiquement un score d'adéquation.

Entrées :

* Offre d'emploi.
* CV candidat.

Sortie :

```json
{
  "score": 87,
  "strengths": [
    "Python",
    "Docker",
    "FastAPI"
  ],
  "missing_skills": [
    "Airflow",
    "Kubernetes"
  ]
}
```

Le score doit être explicable et justifiable.

---

## 3. Analyse GitHub

Le GitHub Agent doit :

* Récupérer les dépôts publics.
* Identifier les technologies utilisées.
* Mesurer l'activité.
* Détecter les projets significatifs.
* Générer un résumé technique.

Exemple :

```text
Compétences détectées :
- Python
- LangGraph
- Docker
- FastAPI

Niveau de confiance :
Élevé
```

---

## 4. Cartographie des Compétences

Construire automatiquement une base de compétences.

Exemples :

```text
Python
Docker
FastAPI
LangGraph
RAG
PostgreSQL
Kubernetes
Airflow
```

Le système doit :

* Détecter les compétences.
* Les normaliser.
* Les agréger.
* Les rendre interrogeables.

---

## 5. Analytics RH

Questions possibles :

* Combien de candidats Python ?
* Combien de profils IA ?
* Quelles sont les compétences les plus rares ?
* Quels profils ont le meilleur score moyen ?
* Quelles offres reçoivent le moins de candidats qualifiés ?

Ces analyses doivent être réalisées via SQL Agent.

---

# Architecture Technique Cible

## Backend

* FastAPI
* LangGraph
* PostgreSQL
* pgvector
* Redis
* Docker

---

## Base de Données

PostgreSQL devient la source unique de vérité.

Tables envisagées :

```text
users
candidates
candidate_skills
jobs
job_skills
candidate_embeddings
job_embeddings
candidate_job_matches
github_profiles
audit_logs
```

---

## Recherche Vectorielle

Utilisation de pgvector.

Fonctionnement :

```text
Question
     ↓
Embedding
     ↓
Recherche Vectorielle
     ↓
Top 20 résultats
     ↓
Re-Ranking
     ↓
Top 5 résultats
```

---

## Re-Ranking

Ajouter un reranker local :

* BGE Reranker

Objectif :

Améliorer la pertinence des résultats avant génération.

---

# Agents

## CV Agent

Responsabilités :

* Parsing CV.
* Extraction des compétences.
* Génération des embeddings.
* Indexation.

---

## Job Agent

Responsabilités :

* Analyse des offres.
* Extraction des compétences requises.
* Génération des embeddings.

---

## Matching Agent

Responsabilités :

* Comparaison CV ↔ Offre.
* Calcul du score.
* Explication du score.
* Classement des candidats.

---

## GitHub Agent

Responsabilités :

* Analyse des dépôts.
* Détection des technologies.
* Évaluation de l'activité open source.

---

## Analytics Agent

Responsabilités :

* Génération de rapports RH.
* Requêtes SQL.
* KPIs recrutement.

---

# Fonctionnalités Futures

## OCR

Support :

* PDF scannés
* Images

Technologies :

* Tesseract
* Modèles Vision

---

## Évaluation Continue

Métriques :

* Pertinence RAG
* Qualité du matching
* Hallucinations

Outils :

* RAGAS
* DeepEval

---

## Observabilité

Stack :

```text
Prometheus
Grafana
Loki
Promtail
```

Métriques :

* Temps de réponse
* Taux d'erreur
* Utilisation mémoire
* Utilisation CPU
* Performances des agents

---

# Objectif Final

Créer une plateforme RH augmentée par IA permettant :

* La recherche intelligente de candidats.
* Le matching automatique CV ↔ Offre.
* L'analyse GitHub.
* L'analyse RH conversationnelle.
* La recommandation de profils.
* L'explication des décisions de l'IA.

Le projet doit démontrer des compétences avancées en :

* IA Générative
* RAG
* LangGraph
* Agents IA
* PostgreSQL + pgvector
* Docker
* MLOps
* Observabilité
* Architecture logicielle moderne
