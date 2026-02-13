"""
Tests du module de prétraitement (preprocess.py).
Vérifie la reconstruction de texte avec espaces intercalés.
"""

import pytest
from app.utils.preprocess import clean_spaced_text


class TestCleanSpacedText:
    """Tests du nettoyage de texte espacé."""

    def test_spaced_word(self):
        """Texte avec des espaces entre les caractères doit être reconstruit."""
        text = "D é v e l o p p e u r"
        result = clean_spaced_text(text)
        assert result == "Développeur"

    def test_normal_text_unchanged(self):
        """Texte normal ne doit pas être modifié."""
        text = "Bonjour le monde"
        result = clean_spaced_text(text)
        assert result == "Bonjour le monde"

    def test_empty_string(self):
        """Chaîne vide retourne chaîne vide."""
        assert clean_spaced_text("") == ""

    def test_none_input(self):
        """None retourne chaîne vide."""
        assert clean_spaced_text(None) == ""

    def test_multiline_spaced(self):
        """Texte multi-lignes avec espaces intercalés."""
        text = "P y t h o n\nS Q L"
        result = clean_spaced_text(text)
        assert "Python" in result
        assert "SQL" in result

    def test_mixed_content(self):
        """Mélange de texte normal et espacé."""
        text = "Compétences: P y t h o n, SQL, D o c k e r"
        result = clean_spaced_text(text)
        # Should reconstruct spaced words (comma boundary may affect results)
        assert "Docker" in result
