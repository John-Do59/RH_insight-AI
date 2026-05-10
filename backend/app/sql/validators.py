"""
SQL Query Validator — Sécurité contre les injections SQL.

Valide les requêtes SQL générées par le LLM avant exécution.
Whitelist de tables/colonnes, blocage de mots-clés dangereux.
"""

import re
from backend.app.utils.logger import logger


# Tables autorisées et leurs colonnes
ALLOWED_TABLES = {
    "candidates": [
        "id", "first_name", "last_name", "email", "phone",
        "city", "summary", "looking_for", "extracted_at"
    ],
    "skills": ["id", "candidate_id", "skill_name", "level"],
    "experiences": [
        "id", "candidate_id", "company", "job_title",
        "start_date", "end_date", "description"
    ],
    "education": [
        "id", "candidate_id", "school", "degree",
        "field", "start_year", "end_year"
    ],
    "projects": ["id", "candidate_id", "name", "description", "technologies"],
    "languages": ["id", "candidate_id", "language", "level"],
}

# Mots-clés SQL dangereux (case-insensitive)
BLOCKED_KEYWORDS = [
    "DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE",
    "EXEC", "EXECUTE", "TRUNCATE", "REPLACE", "MERGE",
    "GRANT", "REVOKE", "ATTACH", "DETACH", "PRAGMA",
]

# Patterns dangereux
BLOCKED_PATTERNS = [
    r";\s*\w",          # Multiple statements (semicolon followed by keyword)
    r"--",              # SQL comments
    r"/\*",             # Block comments
    r"UNION\s+SELECT",  # UNION injection
    r"INTO\s+OUTFILE",  # File write
    r"LOAD_FILE",       # File read
    r"SLEEP\s*\(",      # Time-based injection
    r"BENCHMARK\s*\(",  # Time-based injection
    r"sqlite_master",   # Schema introspection
]

MAX_QUERY_LENGTH = 500


class SQLValidationError(Exception):
    """Raised when a SQL query fails validation."""
    pass


def validate_sql_query(query: str) -> bool:
    """
    Validates a SQL query for safety before execution.

    Args:
        query: The SQL query string to validate.

    Returns:
        True if the query passes all validation checks.

    Raises:
        SQLValidationError: If the query fails any validation check.
    """
    if not query or not query.strip():
        raise SQLValidationError("Requête SQL vide.")

    query_clean = query.strip()
    query_upper = query_clean.upper()

    # 1. Must start with SELECT
    if not query_upper.startswith("SELECT"):
        raise SQLValidationError(
            f"Seules les requêtes SELECT sont autorisées. "
            f"Reçu: {query_clean[:20]}..."
        )

    # 2. Max length check
    if len(query_clean) > MAX_QUERY_LENGTH:
        raise SQLValidationError(
            f"Requête trop longue ({len(query_clean)} caractères, "
            f"max {MAX_QUERY_LENGTH})."
        )

    # 3. Blocked keywords check
    for keyword in BLOCKED_KEYWORDS:
        # Match whole words only (not substrings)
        pattern = rf"\b{keyword}\b"
        if re.search(pattern, query_upper):
            raise SQLValidationError(
                f"Mot-clé interdit détecté: {keyword}"
            )

    # 4. Blocked patterns check
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, query_upper):
            raise SQLValidationError(
                f"Pattern dangereux détecté: {pattern}"
            )

    # 5. Table whitelist check
    # Extract table names from FROM and JOIN clauses
    table_pattern = r"\b(?:FROM|JOIN)\s+(\w+)"
    tables_used = re.findall(table_pattern, query_upper)
    for table in tables_used:
        if table.lower() not in ALLOWED_TABLES:
            raise SQLValidationError(
                f"Table non autorisée: {table}. "
                f"Tables autorisées: {', '.join(ALLOWED_TABLES.keys())}"
            )

    # 6. No subqueries (nested SELECT)
    # Count SELECT occurrences — only 1 allowed
    select_count = len(re.findall(r"\bSELECT\b", query_upper))
    if select_count > 1:
        raise SQLValidationError(
            "Les sous-requêtes (SELECT imbriqués) ne sont pas autorisées."
        )

    # 7. No semicolons (prevent statement chaining)
    if ";" in query_clean:
        raise SQLValidationError(
            "Les requêtes multiples (;) ne sont pas autorisées."
        )

    logger.debug(f"SQL query validated: {query_clean}")
    return True
