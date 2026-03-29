from langfuse import observe

from app.observability.tracing import langfuse

# In-memory store: list of (text, embedding) tuples
_store: list = []


def upsert_vector(text: str, emb: list) -> None:
    _store.append((text, emb))


@observe(as_type="retriever", name="vector-search")
def search_vector(query_embedding: list) -> str:
    """
    Retrieve the most relevant chunk and track as a Langfuse *retriever* span.

    Replace with a real vector DB (Pinecone, Weaviate, pgvector…) when ready.
    """
    if not _store:
        langfuse.update_current_span(
            output={"retrieved_chunks": [], "total_chunks": 0},
            level="WARNING",
            status_message="Vector store is empty",
        )
        return ""

    result = _store[0][0]

    langfuse.update_current_span(
        output={"retrieved_chunks": [result], "total_chunks": len(_store)},
        metadata={"store_size": len(_store), "strategy": "first-match-mock"},
    )

    return result
