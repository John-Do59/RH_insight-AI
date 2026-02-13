"""
Tests pour le routeur d'intentions (router.py).
Vérifie le routage vers les bons agents selon l'intention détectée.
"""

import pytest
from app.graph.router import router, sql_router
from app.config.constants import INTENT_RAG, INTENT_SQL, INTENT_GENERAL


class TestRouter:
    """Tests du routeur principal (intent → agent)."""

    def test_route_rag(self):
        state = {"intent": INTENT_RAG}
        assert router(state) == "rag"

    def test_route_sql(self):
        state = {"intent": INTENT_SQL}
        assert router(state) == "sql"

    def test_route_general(self):
        state = {"intent": INTENT_GENERAL}
        assert router(state) == "response"

    def test_route_hybrid(self):
        state = {"intent": "hybrid"}
        assert router(state) == "sql"

    def test_route_unknown_defaults_to_response(self):
        state = {"intent": "unknown_intent"}
        assert router(state) == "response"

    def test_route_empty_intent_defaults_to_response(self):
        state = {"intent": ""}
        assert router(state) == "response"

    def test_route_missing_intent_defaults_to_response(self):
        state = {}
        assert router(state) == "response"


class TestSqlRouter:
    """Tests du routeur post-SQL (sql → rag ou response)."""

    def test_hybrid_routes_to_rag(self):
        state = {"intent": "hybrid"}
        assert sql_router(state) == "rag"

    def test_sql_routes_to_response(self):
        state = {"intent": INTENT_SQL}
        assert sql_router(state) == "response"

    def test_general_routes_to_response(self):
        state = {"intent": INTENT_GENERAL}
        assert sql_router(state) == "response"

    def test_missing_intent_routes_to_response(self):
        state = {}
        assert sql_router(state) == "response"
