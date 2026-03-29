from langfuse import observe

from app.observability.tracing import langfuse


@observe(as_type="embedding", name="text-embedding")
def get_embedding(text: str) -> list:
    """
    Embed text and track as a Langfuse *embedding* span.

    Replace the body with your real embedding provider
    (e.g. OpenAI text-embedding-3-small) when ready.
    """
    if not text:
        langfuse.update_current_span(
            level="WARNING", status_message="Empty input text"
        )
        return []

    embedding = [float(ord(c)) for c in text[:10]]

    langfuse.update_current_span(
        metadata={"model": "char-ord-mock", "dimensions": len(embedding)},
    )

    return embedding
