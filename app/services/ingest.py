



import logging

from langfuse import observe

from app.observability.tracing import langfuse
from app.utils.embeddings import get_embedding
from app.utils.vectorstore import upsert_vector

logger = logging.getLogger(__name__)


def _safe_langfuse(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Langfuse call failed (non-blocking): {e}")


@observe(name="rag-ingest-pipeline")
def ingest_data(payload: dict) -> dict:
    text = payload.get("text", "")

    if not text:
        _safe_langfuse(
            langfuse.update_current_span,
            level="ERROR",
            status_message="text field is required",
        )
        return {"error": "text field is required"}

    _safe_langfuse(
        langfuse.update_current_span,
        input={"text_preview": text[:200]},
        metadata={"text_length": len(text)},
    )

    embedding = get_embedding(text)
    upsert_vector(text, embedding)

    _safe_langfuse(
        langfuse.update_current_span,
        output={"status": "ingested", "embedding_dims": len(embedding)},
    )

    return {"status": "ingested"}
