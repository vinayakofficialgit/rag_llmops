from langfuse import observe

from app.observability.tracing import langfuse
from app.utils.embeddings import get_embedding
from app.utils.vectorstore import upsert_vector


@observe(name="rag-ingest-pipeline")
def ingest_data(payload: dict) -> dict:
    """
    Document ingest pipeline tracked as a Langfuse trace.

    Span hierarchy:
      rag-ingest-pipeline  (trace)
        └── text-embedding  (embedding span)
    """
    text = payload.get("text", "")

    if not text:
        langfuse.update_current_span(
            level="ERROR",
            status_message="text field is required",
        )
        return {"error": "text field is required"}

    langfuse.update_current_span(
        input={"text_preview": text[:200]},
        metadata={"text_length": len(text)},
    )

    embedding = get_embedding(text)
    upsert_vector(text, embedding)

    langfuse.update_current_span(
        output={"status": "ingested", "embedding_dims": len(embedding)},
    )

    return {"status": "ingested"}
