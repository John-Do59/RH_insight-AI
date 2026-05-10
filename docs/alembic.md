# Aide-mémoire Alembic (Migrations)

Alembic gère les versions de votre schéma de base de données PostgreSQL.

## 1. Initialisation

```bash
# Vérifier l'état actuel
alembic current

# Voir l'historique des migrations
alembic history --verbose
```

## 2. Création de Migrations

```bash
# Générer une migration automatique (après modif des modèles SQLAlchemy)
alembic revision --autogenerate -m "description du changement"

# Créer une migration vide (manuelle)
alembic revision -m "titre de la migration"
```

## 3. Application des Migrations

```bash
# Mettre à jour la base vers la dernière version
alembic upgrade head

# Revenir d'une version en arrière
alembic downgrade -1

# Aller vers une révision spécifique
alembic upgrade <revision_id>
```

## 4. Bonnes Pratiques

- **Toujours vérifier** le fichier généré dans `alembic/versions/` avant de l'appliquer.
- Ne jamais modifier une migration déjà commitée et partagée.
- S'assurer que la `DATABASE_URL` dans `.env` est correcte avant de lancer `upgrade`.
