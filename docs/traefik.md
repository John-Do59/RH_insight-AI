# Traefik — Reverse Proxy & HTTPS

> **Statut** : Implémenté ✅  
> **Branche** : `feature/docker-production-infrastructure`

---

## Rôle

Traefik est le **point d'entrée unique** de l'infrastructure. Il agit comme :

- **Reverse proxy** : route les requêtes HTTP/HTTPS vers les bons conteneurs
- **Gestionnaire SSL** : génère et renouvelle automatiquement les certificats Let's Encrypt
- **Middleware de sécurité** : applique les headers HTTP de sécurité

---

## Architecture

```
Internet (ports 80/443)
        ↓
     Traefik
        ├── Host(`domain.com`) → Frontend (Nginx :80)
        └── Host(`domain.com`) && PathPrefix(`/api`) → Backend (Uvicorn :8000)

     [DB & Redis : internes, jamais exposés]
```

---

## Fichiers de Configuration

### Configuration Statique : `docker/traefik/traefik.yml`

```yaml
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https   # Redirection HTTP → HTTPS automatique
  websecure:
    address: ":443"

providers:
  docker:
    exposedByDefault: false   # Les services doivent opt-in via labels
    network: rh-insight-net

certificatesResolvers:
  letsencrypt:
    acme:
      email: "${ACME_EMAIL}"
      storage: /etc/traefik/acme/acme.json
      httpChallenge:
        entryPoint: web
```

**Points clés** :
- `exposedByDefault: false` → sécurité par défaut, seuls les services avec `traefik.enable=true` sont routés
- Dashboard Traefik désactivé en production
- Certificats persistés dans le volume `traefik_certificates`

---

### Configuration Dynamique : `docker/traefik/dynamic.yml`

Définit les middlewares réutilisables :

```yaml
http:
  middlewares:
    security-headers:
      headers:
        forceSTSHeader: true
        stsIncludeSubdomains: true
        stsSeconds: 31536000       # HSTS 1 an
        contentTypeNosniff: true
        browserXssFilter: true
        referrerPolicy: "strict-origin-when-cross-origin"

    rate-limit:
      rateLimit:
        average: 100
        burst: 50
```

---

## Labels Docker (Routage)

Le routage est configuré directement dans le `docker-compose.prod.yml` via des labels :

### Backend

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.backend.rule=Host(`${DOMAIN}`) && PathPrefix(`/api`)"
  - "traefik.http.routers.backend.entrypoints=websecure"
  - "traefik.http.routers.backend.tls.certresolver=letsencrypt"
  - "traefik.http.routers.backend.middlewares=security-headers@file"
  - "traefik.http.services.backend.loadbalancer.server.port=8000"
```

### Frontend

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.frontend.rule=Host(`${DOMAIN}`)"
  - "traefik.http.routers.frontend.entrypoints=websecure"
  - "traefik.http.routers.frontend.tls.certresolver=letsencrypt"
  - "traefik.http.routers.frontend.middlewares=security-headers@file"
  - "traefik.http.services.frontend.loadbalancer.server.port=80"
```

---

## Simulation Locale (sans domaine)

Dans `docker-compose.local-prod.yml`, le routing est adapté pour `localhost` via HTTP :

```yaml
- "traefik.http.routers.backend-local.rule=Host(`localhost`) && PathPrefix(`/api`, `/docs`, `/openapi.json`)"
- "traefik.http.routers.backend-local.entrypoints=web"
```

Accès : `http://localhost/` → Frontend, `http://localhost/api/` → Backend

---

## Démarrage

Traefik nécessite l'accès au socket Docker pour la découverte automatique des services :

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock:ro
```

> Le montage en `:ro` (read-only) est une bonne pratique de sécurité.
