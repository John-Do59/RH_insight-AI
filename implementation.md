# Prompt de Référence — Conception du Projet  

## Chatbot IA Recruteur (LangGraph + RAG + Agent SQL + CV PDF)

---

## Contexte général

Tu es un ingénieur IA chargé de concevoir un **chatbot intelligent destiné aux recruteurs**.  
Le chatbot permet d’interroger un **CV au format PDF** via une interface **Streamlit**, en **texte ou en vocal**, et retourne des réponses **fiables, traçables et sans hallucination**.

L’architecture repose exclusivement sur des **agents LangGraph**, exécutés avec un **LLM local via Ollama (DeepSeek R1 Q4)**.

---

## Stack technique imposée

- Python
- Streamlit (interface utilisateur)
- LangGraph (orchestration agentique)
- Ollama + DeepSeek R1 Q4 (LLM local)
- Base vectorielle (RAG)
- Base SQL (SQLite ou Postgres)
- CV source au format PDF

---

## Étape 1 — Objectifs fonctionnels

Définir précisément les fonctionnalités attendues :

- Répondre aux questions d’un recruteur sur le CV
- Supporter les questions :
  - factuelles (dates, expériences, compétences)
  - explicatives (parcours, projets, contexte)
- Interaction en :
  - texte
  - vocal
- Téléchargement direct du CV en PDF
- Réponses cohérentes, vérifiables et sans hallucination

---

## Étape 2 — Gestion du CV en PDF

Définir une stratégie pour :

- Stocker le CV en PDF comme **source de vérité unique**
- Gérer les versions du CV
- Rendre le PDF téléchargeable depuis l’interface Streamlit

Contraintes :

- Le LLM ne doit pas interroger directement le PDF brut
- Le PDF sert uniquement à l’ingestion et au téléchargement

---

## Étape 3 — Extraction et préparation des données

À partir du PDF :

- Extraire le texte du CV
- Nettoyer et normaliser le contenu
- Séparer le texte en deux flux distincts :
  - flux **RAG**
  - flux **SQL**

---

## Étape 4 — Agent RAG (LangGraph)

Concevoir un **agent RAG implémenté comme un nœud LangGraph**.

Responsabilités :

- Découper le texte en chunks
- Vectoriser le contenu
- Stocker les embeddings
- Récupérer le contexte pertinent selon la question

Objectif :

- Répondre aux questions narratives et explicatives
- Garantir la fidélité au contenu du CV

---

## Étape 5 — Modélisation de la base SQL

Concevoir une base SQL structurée à partir du CV.

Tables attendues (exemples) :

- `experiences`
- `competences`
- `formations`
- `projets`

Contraintes :

- Données normalisées
- Lecture seule pour les agents
- Cohérence stricte avec le CV PDF

---

## Étape 6 — Agent SQL custom (LangGraph)

Concevoir un **agent SQL LangGraph** capable de :

- Identifier les questions factuelles
- Générer des requêtes SQL contrôlées
- Valider les requêtes (sécurité)
- Exécuter les requêtes sur la base SQL
- Retourner des résultats déterministes

Objectif :

- Fournir des réponses exactes et vérifiables
- Éliminer toute hallucination sur les chiffres et dates

---

## Étape 7 — Détection d’intention et routage (LangGraph)

Concevoir un **agent de détection d’intention** qui :

- Analyse la question utilisateur
- Détermine si la question doit être traitée par :
  - l’agent RAG
  - l’agent SQL

Le routage doit être :

- explicite
- traçable
- conditionnel

---

## Étape 8 — Orchestration globale avec LangGraph

Définir le graphe LangGraph complet :

User Input
↓
Intent Detection Agent
↓
───────────────
↓ ↓
RAG Agent SQL Agent
↓ ↓
└──── Aggregation ────┘
↓
Final Response Agent

LangGraph doit gérer :

- les transitions conditionnelles
- la modularité des agents
- l’évolutivité de l’architecture

---

## Étape 9 — Intégration du LLM local

Configurer l’utilisation de :

- Ollama
- DeepSeek R1 Q4

Rôles du LLM :

- reformulation des réponses SQL
- génération de réponses RAG
- cohérence du dialogue

Contraintes :

- Exécution locale
- Aucune donnée envoyée à un service externe

---

## Étape 10 — Interface utilisateur (Streamlit)

Concevoir une interface Streamlit permettant :

- Saisie de questions en texte
- Interaction vocale (optionnelle)
- Affichage conversationnel des réponses
- Streaming de la réponse
- Bouton de téléchargement du CV en PDF

Streamlit agit uniquement comme **couche UI**.

---

## Étape 11 — Sécurité, fiabilité et qualité

Mettre en place :

- accès SQL en lecture seule
- whitelist des tables
- validation des requêtes
- cohérence entre :
  - PDF
  - RAG
  - SQL

---

## Étape 12 — Tests et validation

Définir des tests :

- fonctionnels (parcours recruteur)
- de cohérence factuelle
- de routage LangGraph
- de cas ambigus

---

## Étape 13 — Scalabilité et évolutions

Prévoir :

- multi-CV
- multi-utilisateur
- authentification recruteur
- version SaaS
- intégration ATS / RH
- remplacement futur de Streamlit par un frontend dédié

---

## Résultat attendu

Le projet final doit :

- répondre précisément aux questions des recruteurs
- s’appuyer sur des données vérifiables
- démontrer une architecture IA agentique avancée
- être compréhensible, maintenable et industrialisable

---
