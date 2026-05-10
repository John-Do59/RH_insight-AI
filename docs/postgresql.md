# Aide-mémoire PostgreSQL

Commandes pour gérer la base de données PostgreSQL du projet.

## 1. Lancement via Docker (Recommandé pour le Dev)

```bash
# Lancer PostgreSQL
docker run --name rh-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=rh_insight \
  -p 5432:5432 \
  -d postgres

# Arrêter le conteneur
docker stop rh-postgres

# Relancer le conteneur existant
docker start rh-postgres
```

## 2. Interaction avec la CLI (psql)

```bash
# Entrer dans le shell PostgreSQL du conteneur
docker exec -it rh-postgres psql -U postgres -d rh_insight

# Commandes utiles dans psql :
#  \dt       : Lister les tables
#  \d <table> : Voir la structure d'une table
#  \q       : Quitter
```

## 3. Sauvegarde et Restauration

```bash
# Sauvegarder la base (Dump)
docker exec -t rh-postgres pg_dumpall -c -U postgres > dump.sql

# Restaurer une base
cat dump.sql | docker exec -i rh-postgres psql -U postgres
```

## 4. Maintenance

```bash
# Voir les processus actifs
SELECT * FROM pg_stat_activity;

# Nettoyer l'espace (Vacuum)
VACUUM ANALYZE;
```
