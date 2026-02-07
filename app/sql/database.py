import os
from sqlalchemy import create_engine
from app.config.settings import SQL_DB_PATH

def get_engine():
    """
    Creates and returns a SQLAlchemy engine for the SQLite database.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(SQL_DB_PATH), exist_ok=True)
    
    db_url = f"sqlite:///{SQL_DB_PATH}"
    return create_engine(db_url, echo=False)

def init_sql_db():
    """
    Initializes the database with the schema if it doesn't exist.
    """
    engine = get_engine()
    # Schema initialization logic will go here
    print(f"Database initialized at {SQL_DB_PATH}")
