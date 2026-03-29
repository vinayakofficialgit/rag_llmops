



import logging

from langfuse import observe

from app.observability.tracing import langfuse

logger = logging.getLogger(__name__)

_store: list = []


def _safe_langfuse(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Langfuse call failed (non-blocking): {e}")


def upsert_vector(text: str, emb: list) -> None:
    _store.append((text, emb))


@observe(as_type="retriever", name="vector-search")
def search_vector(query_embedding: list) -> str:
    if not _store:
        _safe_langfuse(
            langfuse.update_current_span,
            output={"retrieved_chunks": [], "total_chunks": 0},
            level="WARNING",
            status_message="Vector store is empty",
        )
        return ""

    result = _store[0][0]

    _safe_langfuse(
        langfuse.update_current_span,
        output={"retrieved_chunks": [result], "total_chunks": len(_store)},
        metadata={"store_size": len(_store), "strategy": "first-match-mock"},
    )

    return result
