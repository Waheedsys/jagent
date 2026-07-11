from fastapi import FastAPI
from app.agents.graph import app_graph
from app.agents.state import OutreachState

app = FastAPI(title="j-agent")

@app.post("/score")
async def score(state: OutreachState):
    result = await app_graph.ainvoke(state)
    return result