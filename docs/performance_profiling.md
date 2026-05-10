# Profiling et Performance (Étape 5)

Ce document explique comment le système de monitoring de **RH Insight AI** suit la latence et optimise les performances.

## 1. Décorateur `@profile_async`

Toutes les fonctions critiques du backend sont instrumentées avec un décorateur personnalisé situé dans `backend/app/core/monitoring.py`.

### Utilisation :
```python
from backend.app.core.monitoring import profile_async

@profile_async("Mon Agent")
async def mon_agent(state):
    # ... logique ...
```

## 2. Analyse de la Latence

Les logs affichent désormais le temps passé dans chaque composant. Exemple de sortie console :

```text
INFO:  [Intent Agent] executed in 0.45s
INFO:  [SQL Agent] executed in 0.12s
INFO:  [GitHub Agent] executed in 0.85s
INFO:  [Global Chat Request] executed in 1.54s
```

## 3. Optimisations Implémentées

### Async I/O
- **SQL** : Migration vers `aiosqlite` pour éviter de bloquer l'Event Loop lors des requêtes sur les candidats.
- **GitHub** : Utilisation de `httpx.AsyncClient` pour paralléliser les appels API si nécessaire.
- **RAG** : Recherche vectorielle asynchrone via ChromaDB.

### Token Streaming
L'endpoint `/api/v1/chat/` utilise `StreamingResponse`. Les tokens sont envoyés au fur et à mesure de leur génération par le LLM, ce qui réduit le **Time-To-First-Token (TTFT)** à moins de 500ms.

### Model Routing
Le système choisit le modèle le plus adapté :
- **Qwen 3.5 (4B)** : Modèle par défaut pour les tâches rapides (Intention, SQL, RAG simple).
- **DeepSeek-R1** : Activé uniquement pour les requêtes "hybrides" ou nécessitant un raisonnement complexe.

## 4. Résultats Attendus (Mac M4 Pro)

| Étape | Temps Moyen |
| :--- | :--- |
| Détection d'intention | ~0.3s |
| Récupération RAG | ~0.1s |
| Génération SQL | ~0.2s |
| Synthèse Finale (Qwen 3.5) | ~40 tokens/sec |
