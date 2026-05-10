# Audit du Projet et Optimisation de la Latence

## 1. État Actuel du Projet

### Points Forts
- **Architecture Modulaire** : L'utilisation de LangGraph permet une séparation claire des responsabilités entre les agents.
- **Interface Riche** : Streamlit est bien utilisé avec des fonctionnalités avancées (audio, CSS).
- **Multi-Sources** : Capacité à croiser SQL, RAG et GitHub.

### Points à Améliorer
- **Latence Élevée** : Les réponses sur les CV sont lentes.
- **Monolithe Streamlit** : Le fichier `streamlit_app.py` contient trop de logique métier qui devrait être déportée dans des modules.
- **Gestion des Modèles** : L'utilisation systématique de modèles "Reasoning" (DeepSeek-R1) pour toutes les réponses ralentit l'expérience utilisateur.

## 2. Analyse de la Latence

La lenteur actuelle s'explique par plusieurs facteurs techniques :

1.  **Modèle "Reasoning" (DeepSeek-R1)** : Ce modèle génère une "chaîne de pensée" (CoT) avant de répondre. Bien que performant pour le raisonnement, il est structurellement beaucoup plus lent qu'un modèle direct.
2.  **Inférence Locale (Ollama)** : Sans un GPU puissant (Apple Silicon M2/M3 Max ou NVIDIA RTX), l'exécution locale de modèles 7B+ est limitée par la bande passante mémoire.
3.  **Absence de Streaming** : L'interface attend que la réponse soit complète avant de l'afficher, donnant une impression de blocage.

## 3. Recommandations pour une Latence "Niveau Professionnel"

Pour atteindre une réactivité instantanée, voici les solutions préconisées par ordre de priorité :

### Solution A : Passer sur des APIs Cloud "Ultra-Fast" (Recommandé)
L'utilisation de services comme **Groq** ou **Together AI** permet d'obtenir des vitesses d'inférence dépassant les 300 tokens/seconde (quasi instantané).
- **Modèle conseillé** : `Llama 3.1 70B` ou `70B Versatile` sur Groq.
- **Coût** : Très faible, voire gratuit (tier gratuit généreux).

### Solution B : Optimisation de l'Inférence Locale
Si l'hébergement local est une contrainte :
- **Changer de modèle** : Utiliser `Llama 3.2 3B` ou `Mistral Nemo` à la place de DeepSeek-R1 pour les réponses RAG simples.
- **Quantification** : S'assurer d'utiliser des versions `q4_K_M` ou `q2` si la RAM est limitée.

### Solution C : Implémentation du Streaming
Modifier le backend et l'interface Streamlit pour afficher les mots au fur et à mesure de leur génération. Cela réduit la "latence perçue" à presque zéro.

### Solution D : Cache Sémantique
Mettre en place un cache (ex: Redis) pour stocker les réponses aux questions fréquentes. Si une question similaire est posée, la réponse est renvoyée instantanément sans appel au LLM.

## 4. Plan d'Action Proposé

1.  **Phase 1** : Intégrer le support du streaming dans `app/agents/response_agent.py`.
2.  **Phase 2** : Ajouter une option dans `.env` pour basculer vers un fournisseur cloud (Groq/OpenAI) pour les moments nécessitant une haute performance.
3.  **Phase 3** : Refactoriser `streamlit_app.py` pour séparer la vue de la logique.
