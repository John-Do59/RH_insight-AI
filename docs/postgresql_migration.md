# Migration PostgreSQL + pgvector

> **Statut** : Implémenté ✅  
> **Branche** : `feature/database-design`

---

## Contexte

L'application fonctionnait initialement sur **SQLite** via un ORM basique.

La migration vers **PostgreSQL + pgvector** a été motivée par :

- Le passage à une architecture multi-agents (besoin de données structurées et relationnelles)
- La recherche sémantique par similarité vectorielle (embeddings 768 dimensions)
- La scalabilité SaaS (connexions concurrentes, volumes de données)
- La compatibilité avec LangGraph et les futurs agents IA

---

## Stack

| Composant | Version | Rôle |
|---|---|---|
| PostgreSQL | 16 | Base de données relationnelle |
| pgvector | 0.5+ | Extension pour embeddings et recherche vectorielle |
| SQLAlchemy | 2.0 | ORM Python (syntaxe `Mapped[]` moderne) |
| Alembic | Latest | Migrations de schéma |
| psycopg2 | Latest | Driver PostgreSQL synchrone |

---

## Modèles SQLAlchemy 2.0

Tous les modèles héritent d'une `Base` centralisée et d'un `BaseModelMixin` :

### `backend/app/models/base.py`

```python
class BaseModelMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

**Règles** :
- UUID obligatoire pour toutes les clés primaires
- `created_at` / `updated_at` automatiques via `server_default`

---

## Schéma des Tables

```
candidates ────────── candidate_skills ─── skills ─── job_skills ── jobs
     │                                                                 │
     ├── candidate_embeddings (Vector 768d, HNSW)                     ├── job_embeddings (Vector 768d, HNSW)
     │                                                                 │
     └── candidate_job_matches (score, strengths, gaps) ──────────────┘
     │
     └── github_profiles
```

### Tables principales

| Table | Clé | Description |
|---|---|---|
| `candidates` | UUID | Profil candidat + embedding global |
| `jobs` | UUID | Offre d'emploi + embedding global |
| `skills` | UUID | Catalogue de compétences (unique par nom) |
| `candidate_skills` | (candidate_id, skill_id) | Association M2M + niveau |
| `job_skills` | (job_id, skill_id) | Compétences requises par l'offre |
| `candidate_embeddings` | UUID | Chunks textuels + vecteurs (RAG) |
| `job_embeddings` | UUID | Chunks textuels + vecteurs (RAG) |
| `candidate_job_matches` | UUID | Cache des scores IA (unique par paire) |
| `github_profiles` | UUID | Données GitHub enrichies (1-to-1 candidat) |

---

## Stockage Vectoriel (pgvector)

Les embeddings sont stockés avec le type `Vector(768)` (compatible `nomic-embed-text`) :

```python
embedding: Mapped[Optional[list[float]]] = mapped_column(Vector(768), nullable=True)
```

### Index HNSW

Les tables d'embeddings utilisent l'index **HNSW** (Hierarchical Navigable Small World) pour des recherches ANN ultra-rapides :

```python
__table_args__ = (
    Index(
        "idx_candidate_embeddings_hnsw",
        "embedding",
        postgresql_using="hnsw",
        postgresql_with={"m": 16, "ef_construction": 64},
        postgresql_ops={"embedding": "vector_cosine_ops"},
    ),
)
```

**Paramètres** :
- `m=16` : Nombre de connexions par nœud (compromis mémoire/précision)
- `ef_construction=64` : Taille du graphe lors de la construction
- `vector_cosine_ops` : Distance cosine (optimal pour embeddings de texte normalisés)

---

## Connexion & Session

### `backend/app/database/session.py`

```python
DATABASE_URL = settings.DATABASE_URL  # depuis .env

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### URL de connexion `.env`

```env
DATABASE_URL=postgresql://rh_user:rh_password@localhost:5432/rh_insight
# En Docker
DATABASE_URL=postgresql://rh_user:rh_password@db:5432/rh_insight
```

---

## Migrations Alembic

### Configuration (`alembic/env.py`)

`env.py` est configuré pour importer toutes les métadonnées depuis le package de modèles :

```python
from backend.app.models import Base
target_metadata = Base.metadata
```

### Commandes utiles

```bash
# Génération automatique d'une migration
alembic revision --autogenerate -m "description"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1

# Historique
alembic history
```

> **Important** : En production Docker, les migrations sont exécutées manuellement avant le démarrage de l'app, ou via un script d'entrypoint.

---

## Activation de l'extension pgvector

L'extension doit être activée dans PostgreSQL avant les migrations :

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Avec l'image `pgvector/pgvector:pg16`, l'extension est disponible mais doit être créée dans la base. Cela peut être fait dans le premier script de migration Alembic :

```python
def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    # ... reste des migrations
```
