from app.sql.database import get_engine
from sqlalchemy import text
from app.utils.logger import logger

def init_db():
    engine = get_engine()
    schema_path = "app/sql/schema.sql"
    
    try:
        with open(schema_path, "r") as f:
            schema = f.read()
        
        with engine.connect() as conn:
            for statement in schema.split(";"):
                if statement.strip():
                    conn.execute(text(statement))
            conn.commit()
        logger.info("SQL database schema initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing DB schema: {e}")

if __name__ == "__main__":
    init_db()
