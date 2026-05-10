# Aide-mémoire Vue.js (Frontend)

Ce document récapitule les commandes essentielles pour le développement frontend avec Vue.js 3 et Vite.

## 1. Initialisation et Installation

```bash
# Installer les dépendances
npm install

# Mettre à jour les dépendances
npm update
```

## 2. Développement

```bash
# Lancer le serveur de développement (HMR activé)
npm run dev

# Lancer avec un hôte spécifique (ex: accès réseau local)
npm run dev -- --host
```

## 3. Build et Production

```bash
# Compiler pour la production (génère le dossier /dist)
npm run build

# Tester le build localement
npm run preview
```

## 4. Lint et Qualité

```bash
# Vérifier le code avec ESLint
npm run lint

# Formater le code avec Prettier
npm run format
```

## 5. Structure Recommandée

- **src/components/** : Composants réutilisables.
- **src/views/** : Pages principales (routage).
- **src/services/** : Appels API (Axios/Fetch).
- **src/store/** : Gestion d'état (Pinia).
- **src/assets/** : Images, styles globaux, polices.

## 6. Astuces Vite

- Les variables d'environnement doivent commencer par `VITE_` (ex: `VITE_API_URL`).
- Accessibles via `import.meta.env.VITE_API_URL`.
