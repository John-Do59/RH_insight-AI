from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from backend.app.api.api_v1.api import api_router
from backend.app.utils.logger import logger
from backend.app.config.settings import BACKEND_CORS_ORIGINS

# Rate limiter instance partagé dans toute l'application
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="RH Insight AI API",
    description="Backend API for RH Insight AI Platform",
    version="1.0.0",
)

# Attach the rate limiter to the app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "healthy"}

# Include all API routes
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
