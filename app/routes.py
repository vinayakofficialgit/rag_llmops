

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ingest import ingest_data
from app.services.query import query_data

router = APIRouter()

# ✅ Define request model
class QueryRequest(BaseModel):
    query: str

@router.post("/ingest")
def ingest(payload: dict):
    return ingest_data(payload)

@router.post("/query")
def query(payload: QueryRequest):
    return query_data(payload.dict())