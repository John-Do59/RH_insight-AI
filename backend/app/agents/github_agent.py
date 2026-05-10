"""
GitHub Agent — Interroge GitHub pour obtenir des données sur les projets.
"""

from backend.app.github.github_client import github_client
from backend.app.utils.logger import logger

from backend.app.core.monitoring import profile_async

@profile_async("GitHub Agent")
async def github_agent(state: dict) -> dict:
    """
    Agent qui récupère les repositories GitHub de John-Do59.
    """
    logger.info("GitHub Agent: Fetching repositories...")
    
    try:
        repos = await github_client.get_all_repos()
        
        if not repos:
            logger.warning("GitHub Agent: No repositories found or error occurred.")
            return {
                "github_data": [],
                "agent_sources": state.get("agent_sources", []) + ["github"]
            }
        
        logger.info(f"GitHub Agent: Found {len(repos)} repositories.")
        
        return {
            "github_data": repos,
            "agent_sources": state.get("agent_sources", []) + ["github"]
        }
        
    except Exception as e:
        logger.error(f"Error in GitHub Agent: {e}")
        return {
            "github_data": [],
            "agent_sources": state.get("agent_sources", []) + ["github"]
        }
