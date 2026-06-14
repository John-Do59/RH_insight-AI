# ═══════════════════════════════════════════════════════════════════════════
# Backend Dockerfile — Optimisé (Debian Slim)
#
# Note: Alpine a été abandonné car des librairies ML comme `onnxruntime`
# (requise par ChromaDB) n'ont pas de wheels pré-compilés pour musl (Alpine).
# Debian Slim offre les wheels binaires et reste très léger.
# ═══════════════════════════════════════════════════════════════════════════

# ── Stage 1 : Builder ──────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Dépendances de compilation (dev-only, pas copiées en runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip wheel setuptools

# Venv isolé
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installer les dépendances prod uniquement
COPY requirements.txt .
RUN pip install --no-cache-dir --compile -r requirements.txt

# Nettoyage post-install agressif
RUN find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/venv -type d -name "tests" -path "*/site-packages/*" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/venv -type d -name "docs" -path "*/site-packages/*" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/venv -type d -name "examples" -path "*/site-packages/*" -exec rm -rf {} + 2>/dev/null || true

# ── Stage 2 : Runtime ──────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Uniquement les libs runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier le venv compilé
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Variables d'env pour désactiver les téléchargements lourds
ENV TRANSFORMERS_OFFLINE=1 \
    HF_DATASETS_OFFLINE=1 \
    TOKENIZERS_PARALLELISM=false \
    ANONYMIZED_TELEMETRY=false \
    LANGCHAIN_TRACING_V2=false \
    PYTHONUNBUFFERED=1

# Non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Copier uniquement le code applicatif
COPY --chown=appuser:appuser backend/ /app/backend/
COPY --chown=appuser:appuser alembic/ /app/alembic/
COPY --chown=appuser:appuser alembic.ini /app/alembic.ini

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "*"]
