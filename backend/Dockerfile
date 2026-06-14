# ═══════════════════════════════════════════════════════════════════════════
# Backend Dockerfile — Optimisé taille d'image
# Objectif cible : < 2.5GB (vs 9GB non-optimisé)
#
# Stratégie :
#   1. Builder stage: compile wheels en isolation (inclut build-essential)
#   2. Runtime stage: copie uniquement les wheels compilés, sans toolchain
#   3. Variables d'environnement agressives pour désactiver les caches PyTorch/HF
# ═══════════════════════════════════════════════════════════════════════════

# ── Stage 1 : Builder ──────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Dépendances de compilation (libpq-dev pour psycopg2-binary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip & wheel
RUN pip install --upgrade pip wheel setuptools

# Installer les dépendances dans un venv isolé
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copier uniquement le requirements de prod (pas dev)
COPY requirements.txt .

# Install avec options d'optimisation :
# --no-cache-dir   → pas de cache pip (réduit la taille du layer)
# Torch/HF sont installés sans les extras CUDA inutiles
RUN pip install --no-cache-dir -r requirements.txt

# Supprimer les fichiers inutiles du venv post-install pour réduire encore la taille :
# - tests des librairies
# - fichiers __pycache__
# - données de test de torch
RUN find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/venv -type d -name "tests" -path "*/site-packages/*" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/venv -name "*.dist-info" -type d | xargs -I{} find {} -name "RECORD" -delete 2>/dev/null || true

# ── Stage 2 : Runtime ──────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Uniquement les libs runtime (pas build-essential)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier le venv compilé depuis le builder
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Désactiver les téléchargements automatiques HuggingFace/sentence-transformers
# (les embeddings sont gérés par Ollama en production)
ENV TRANSFORMERS_OFFLINE=1
ENV HF_DATASETS_OFFLINE=1
ENV TOKENIZERS_PARALLELISM=false
# Désactiver la télémétrie Chromadb
ENV ANONYMIZED_TELEMETRY=false
# Désactiver la télémétrie LangChain
ENV LANGCHAIN_TRACING_V2=false

# Non-root user pour la sécurité
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Copier uniquement le code applicatif (pas venv, pas tests, pas data)
COPY --chown=appuser:appuser backend/ /app/backend/
COPY --chown=appuser:appuser alembic/ /app/alembic/
COPY --chown=appuser:appuser alembic.ini /app/alembic.ini

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "*"]
