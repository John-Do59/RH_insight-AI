import pytest
from backend.app.database.validators import validate_sql_query, SQLValidationError

def test_valid_sql():
    # Should not raise
    validate_sql_query("SELECT * FROM candidates")
    validate_sql_query("SELECT first_name, last_name FROM candidates WHERE id = 1")

def test_invalid_sql_delete():
    with pytest.raises(SQLValidationError) as excinfo:
        validate_sql_query("DELETE FROM candidates")
    assert "SELECT" in str(excinfo.value)

def test_invalid_sql_drop():
    with pytest.raises(SQLValidationError):
        validate_sql_query("DROP TABLE users")

def test_invalid_sql_semicolon():
    with pytest.raises(SQLValidationError):
        validate_sql_query("SELECT * FROM candidates; DROP TABLE users")

def test_invalid_sql_comment():
    with pytest.raises(SQLValidationError):
        validate_sql_query("SELECT * FROM candidates -- drop table users")
