from fastapi import APIRouter
from backend.app.api.api_v1.endpoints import chat, auth, match, job_agent, ranking, search, jobs, candidates, analytics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(match.router, prefix="/match", tags=["match"])
api_router.include_router(job_agent.router, prefix="/job-agent", tags=["job-agent"])
api_router.include_router(ranking.router, prefix="/ranking", tags=["ranking"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
