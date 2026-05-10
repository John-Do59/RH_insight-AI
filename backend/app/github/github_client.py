"""
GitHub API Client — Récupération des données projets.

Encapsule les appels à l'API GitHub avec gestion du cache et des erreurs.
"""

import httpx
from datetime import datetime, timedelta
from cachetools import TTLCache
from typing import List, Dict, Any, Optional
from backend.app.config.settings import GITHUB_TOKEN, GITHUB_USERNAME
from backend.app.utils.logger import logger

class GitHubClient:
    """
    Client pour l'API GitHub (version synchrone).
    Utilise un cache TTL pour éviter les appels excessifs.
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self):
        # Cache de 1 heure
        self.cache = TTLCache(maxsize=100, ttl=timedelta(hours=1).total_seconds())
        
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RH-Insight-AI"
        }
        
        if GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {GITHUB_TOKEN}"
            logger.debug("GitHub Client: Using authenticated requests.")
        else:
            logger.warning("GitHub Client: No GITHUB_TOKEN provided. Rate limits will be restricted (60/h).")

    def get_all_repos(self, username: str = GITHUB_USERNAME) -> List[Dict[str, Any]]:
        """
        Récupère la liste des repositories (publics et privés si token présent).
        """
        # Si token présent, on utilise /user/repos pour inclure les privés
        key_suffix = "auth" if GITHUB_TOKEN else "public"
        cache_key = f"repos_{username}_{key_suffix}"
        
        if cache_key in self.cache:
            logger.debug(f"GitHub Client: Cache hit for repos of {username}")
            return self.cache[cache_key]
        
        # Endpoint différent selon l'auth
        if GITHUB_TOKEN:
            url = f"{self.BASE_URL}/user/repos"
            params = {"sort": "updated", "per_page": 100, "visibility": "all"}
        else:
            url = f"{self.BASE_URL}/users/{username}/repos"
            params = {"sort": "updated", "per_page": 100, "type": "public"}
        
        try:
            with httpx.Client() as client:
                response = client.get(url, headers=self.headers, params=params, timeout=10.0)
                response.raise_for_status()
                repos = response.json()
                
                processed_repos = []
                for r in repos:
                    # On ignore les forks pour ne garder que les projets originaux
                    if not r.get("fork"):
                        processed_repos.append({
                            "name": r.get("name"),
                            "description": r.get("description"),
                            "language": r.get("language"),
                            "stars": r.get("stargazers_count"),
                            "url": r.get("html_url"),
                            "updated_at": r.get("updated_at"),
                            "topics": r.get("topics", []),
                            "is_private": r.get("private", False)
                        })
                
                self.cache[cache_key] = processed_repos
                return processed_repos
                
        except httpx.HTTPStatusError as e:
            logger.error(f"GitHub API Error ({e.response.status_code}): {e.response.text}")
            return []
        except Exception as e:
            logger.error(f"GitHub Client Error: {e}")
            return []

# Singleton
github_client = GitHubClient()

