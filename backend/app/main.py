from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.api_v1.api import api_router
from backend.app.utils.logger import logger

app = FastAPI(
    title="RH Insight AI API",
    description="Backend API for RH Insight AI Platform",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
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
