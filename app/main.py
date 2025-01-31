from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import get_response

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    id: int

class QueryResponse(BaseModel):
    id: int
    answer: int
    reasoning: str
    sources: list

@app.post("/api/request", response_model=QueryResponse)
async def handle_request(request: QueryRequest):
    try:
        response = get_response(request.query, request.id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
