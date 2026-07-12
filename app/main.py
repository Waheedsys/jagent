from fastapi import FastAPI
from app.agents.graph import app_graph
from app.api.schemas import ScoreRequest
from fastapi import HTTPException

app = FastAPI(title="j-agent")

@app.post("/process-lead")
async def process_lead(request: ScoreRequest):
    try:
        result = await app_graph.ainvoke(request.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))