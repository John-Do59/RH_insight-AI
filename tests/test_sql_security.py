"""
Tests de sécurité SQL — Validation des requêtes.
Vérifie que le validateur bloque les injections et requêtes dangereuses.
"""

import pytest
from app.sql.validators import validate_sql_query, SQLValidationError


class TestValidQueries:
    """Requêtes qui DOIVENT passer la validation."""

    def test_simple_select(self):
        assert validate_sql_query("SELECT * FROM candidates") is True

    def test_select_with_where(self):
        assert validate_sql_query(
            "SELECT skill_name, level FROM skills WHERE LOWER(skill_name) LIKE '%python%'"
        ) is True

    def test_select_with_order(self):
        assert validate_sql_query(
            "SELECT company, job_title FROM experiences ORDER BY start_date DESC"
        ) is True

    def test_select_with_limit(self):
        assert validate_sql_query(
            "SELECT first_name, last_name FROM candidates LIMIT 1"
        ) is True

    def test_select_with_join(self):
        assert validate_sql_query(
            "SELECT s.skill_name, c.first_name FROM skills s JOIN candidates c ON s.candidate_id = c.id"
        ) is True

    def test_select_from_education(self):
        assert validate_sql_query(
            "SELECT school, degree, field FROM education ORDER BY start_year DESC"
        ) is True

    def test_select_from_projects(self):
        assert validate_sql_query(
            "SELECT name, technologies FROM projects"
        ) is True

    def test_select_from_languages(self):
        assert validate_sql_query(
            "SELECT language, level FROM languages"
        ) is True


class TestBlockedKeywords:
    """Requêtes avec des mots-clés dangereux qui DOIVENT être bloquées."""

    def test_drop_table(self):
        with pytest.raises(SQLValidationError, match="DROP"):
            validate_sql_query("SELECT * FROM candidates; DROP TABLE candidates")

    def test_delete(self):
        with pytest.raises(SQLValidationError, match="DELETE"):
            validate_sql_query("DELETE FROM candidates WHERE id = 1")

    def test_insert(self):
        with pytest.raises(SQLValidationError, match="INSERT"):
            validate_sql_query("INSERT INTO candidates (first_name) VALUES ('hacker')")

    def test_update(self):
        with pytest.raises(SQLValidationError, match="UPDATE"):
            validate_sql_query("UPDATE candidates SET first_name = 'hacked'")

    def test_alter(self):
        with pytest.raises(SQLValidationError, match="ALTER"):
            validate_sql_query("ALTER TABLE candidates ADD COLUMN malicious TEXT")

    def test_create(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query("CREATE TABLE evil (data TEXT)")

    def test_truncate(self):
        with pytest.raises(SQLValidationError, match="TRUNCATE"):
            validate_sql_query("TRUNCATE TABLE candidates")

    def test_pragma(self):
        with pytest.raises(SQLValidationError, match="PRAGMA"):
            validate_sql_query("PRAGMA table_info(candidates)")


class TestInjectionPatterns:
    """Patterns d'injection SQL qui DOIVENT être bloqués."""

    def test_semicolon_chaining(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query("SELECT * FROM candidates; SELECT * FROM skills")

    def test_comment_injection(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query("SELECT * FROM candidates -- WHERE id = 1")

    def test_union_select(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query(
                "SELECT * FROM candidates UNION SELECT * FROM sqlite_master"
            )

    def test_sqlite_master_access(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query("SELECT * FROM sqlite_master")

    def test_subquery(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query(
                "SELECT * FROM candidates WHERE id IN (SELECT candidate_id FROM skills)"
            )


class TestTableWhitelist:
    """Vérification de la whitelist des tables."""

    def test_unauthorized_table(self):
        with pytest.raises(SQLValidationError, match="non autorisée"):
            validate_sql_query("SELECT * FROM users")

    def test_unauthorized_system_table(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query("SELECT * FROM sqlite_master")


class TestEdgeCases:
    """Cas limites et validations générales."""

    def test_empty_query(self):
        with pytest.raises(SQLValidationError, match="vide"):
            validate_sql_query("")

    def test_none_query(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query(None)

    def test_whitespace_only(self):
        with pytest.raises(SQLValidationError):
            validate_sql_query("   ")

    def test_not_select(self):
        with pytest.raises(SQLValidationError, match="SELECT"):
            validate_sql_query("SHOW TABLES")

    def test_query_too_long(self):
        long_query = "SELECT * FROM candidates WHERE " + " OR ".join(
            [f"first_name = 'test{i}'" for i in range(100)]
        )
        with pytest.raises(SQLValidationError, match="trop longue"):
            validate_sql_query(long_query)
