import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration SQLite
SQLITE_DB = "data/sql/recruiter.db"

# Configuration PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "rh_insight")

def migrate():
    if not os.path.exists(SQLITE_DB):
        print(f"SQLite database not found at {SQLITE_DB}")
        return

    print(f"Connecting to SQLite: {SQLITE_DB}")
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()

    print(f"Connecting to PostgreSQL: {POSTGRES_DB}")
    pg_conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_SERVER,
        port=POSTGRES_PORT
    )
    pg_cursor = pg_conn.cursor()

    # Liste des tables à migrer
    tables = ["candidates", "skills", "experiences", "education", "projects", "languages"]

    for table in tables:
        print(f"Migrating table: {table}...")
        
        # Lire depuis SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"  No data in {table}")
            continue

        # Préparer l'insertion PostgreSQL
        columns = rows[0].keys()
        cols_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"

        for row in rows:
            pg_cursor.execute(insert_query, tuple(row))

    pg_conn.commit()
    print("Migration completed successfully!")

    sqlite_conn.close()
    pg_conn.close()

if __name__ == "__main__":
    migrate()
