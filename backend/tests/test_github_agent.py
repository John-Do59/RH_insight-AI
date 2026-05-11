"""
Tests unitaires pour l'Agent GitHub et le client GitHub.
"""

import pytest
from unittest.mock import MagicMock, patch
from backend.app.github.github_client import GitHubClient
from backend.app.agents.github_agent import github_agent

@pytest.fixture
def mock_github_client():
    with patch('app.github.github_client.httpx.Client') as mock_client:
        yield mock_client

def test_github_client_parsing():
    """Vérifie que le client traite correctement la réponse JSON de GitHub."""
    client = GitHubClient()
    
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"name": "repo1", "fork": False, "stargazers_count": 10, "language": "Python", "html_url": "url1", "description": "desc1"},
        {"name": "repo2", "fork": True, "stargazers_count": 5, "language": "JS", "html_url": "url2", "description": "desc2"}
    ]
    mock_response.status_code = 200
    
    with patch('httpx.Client.get', return_value=mock_response):
        repos = client.get_public_repos("testuser")
        
        assert len(repos) == 1
        assert repos[0]["name"] == "repo1"
        assert repos[0]["stars"] == 10
        assert repos[0]["language"] == "Python"

def test_github_agent_integration():
    """Vérifie que l'agent met à jour le state correctement."""
    mock_repos = [{"name": "project-ai", "language": "Python", "stars": 100}]
    
    with patch('app.github.github_client.github_client.get_public_repos', return_value=mock_repos):
        state = {"question": "Quels sont tes projets ?", "agent_sources": ["intent"]}
        result = github_agent(state)
        
        assert "github_data" in result
        assert len(result["github_data"]) == 1
        assert "github" in result["agent_sources"]
        assert result["github_data"][0]["name"] == "project-ai"

def test_github_agent_error_handling():
    """Vérifie la robustesse en cas d'erreur API."""
    with patch('app.github.github_client.github_client.get_public_repos', side_effect=Exception("API Down")):
        state = {"question": "Quels sont tes projets ?", "agent_sources": []}
        result = github_agent(state)
        
        assert result["github_data"] == []
        assert "github" in result["agent_sources"]
