from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router
from app.observability.tracing import flush_langfuse

app = FastAPI(title="RAG Production LLMOps")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"status": "running"}


@app.on_event("shutdown")
def shutdown():
    """Flush all buffered Langfuse events before the process exits."""
    flush_langfuse()
