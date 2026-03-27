
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="RAG Production LLMOps")
app.include_router(router)

@app.get("/")
def root():
    return {"status":"running"}
