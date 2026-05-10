from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.app.graph.graph import app as agent_graph
from backend.app.utils.logger import logger

app = FastAPI(title="RH Insight AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("question")
    
    initial_state = {
        "question": question,
        "messages": [{"role": "user", "content": question}],
        "documents": [],
        "sql_data": [],
        "sql_query": "",
        "github_data": [],
        "agent_sources": [],
        "intent": "general",
        "response": ""
    }
    
    # We will use streaming in a real scenario, but for now, simple invoke
    result = await agent_graph.ainvoke(initial_state)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
