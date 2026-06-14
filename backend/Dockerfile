# ═══════════════════════════════════════════════════════════════════════════
# Backend Dockerfile — Alpine optimisé
# Cible : 400–600 MB (vs 9GB initial, 803MB précédent)
#
# Gains vs slim :
#   alpine = 5MB base (vs 25MB slim)
#   musl libc = pas de glibc overhead
#   --no-compile + strip = .pyc au besoin uniquement
# ═══════════════════════════════════════════════════════════════════════════

# ── Stage 1 : Builder ──────────────────────────────────────────────────────
FROM python:3.11-alpine AS builder

WORKDIR /build

# Dépendances de compilation (dev-only, pas copiées en runtime)
RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    git

# Upgrade pip
RUN pip install --upgrade pip wheel setuptools

# Venv isolé
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installer les dépendances prod uniquement
COPY requirements.txt .
RUN pip install --no-cache-dir --no-compile -r requirements.txt

# Nettoyage post-install agressif
RUN find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/venv -type d -name "tests" -path "*/site-packages/*" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/venv -name "*.pyc" -delete 2>/dev/null || true
RUN find /opt/venv -name "*.pyo" -delete 2>/dev/null || true
# Supprimer docs embarquées dans les packages
RUN find /opt/venv -type d -name "docs" -path "*/site-packages/*" -exec rm -rf {} + 2>/dev/null || true
RUN find /opt/venv -type d -name "examples" -path "*/site-packages/*" -exec rm -rf {} + 2>/dev/null || true

# ── Stage 2 : Runtime ──────────────────────────────────────────────────────
FROM python:3.11-alpine

WORKDIR /app

# Uniquement les libs runtime (pas build-base)
RUN apk add --no-cache \
    libpq \
    curl \
    && rm -rf /var/cache/apk/*

# Copier le venv compilé
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Variables d'env pour désactiver les téléchargements lourds
ENV TRANSFORMERS_OFFLINE=1 \
    HF_DATASETS_OFFLINE=1 \
    TOKENIZERS_PARALLELISM=false \
    ANONYMIZED_TELEMETRY=false \
    LANGCHAIN_TRACING_V2=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Copier uniquement le code applicatif
COPY --chown=appuser:appgroup backend/ /app/backend/
COPY --chown=appuser:appgroup alembic/ /app/alembic/
COPY --chown=appuser:appgroup alembic.ini /app/alembic.ini

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "*"]
