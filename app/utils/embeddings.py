

import logging

from langfuse import observe

from app.observability.tracing import langfuse

logger = logging.getLogger(__name__)


def _safe_langfuse(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Langfuse call failed (non-blocking): {e}")


@observe(as_type="embedding", name="text-embedding")
def get_embedding(text: str) -> list:
    if not text:
        _safe_langfuse(
            langfuse.update_current_span,
            level="WARNING",
            status_message="Empty input text",
        )
        return []

    embedding = [float(ord(c)) for c in text[:10]]

    _safe_langfuse(
        langfuse.update_current_span,
        metadata={"model": "char-ord-mock", "dimensions": len(embedding)},
    )

    return embedding
