from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    id: int

class QueryResponse(BaseModel):
    id: int
    answer: Optional[int]  # Allow None for the answer field
    reasoning: Optional[str]
    sources: List[str]