


import logging

from langfuse import observe

from app.observability.tracing import langfuse

logger = logging.getLogger(__name__)


def _safe_langfuse(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Langfuse call failed (non-blocking): {e}")


@observe(as_type="evaluator", name="hallucination-check")
def score(answer: str, context: str) -> float:
    result = 0.0 if context and context in answer else 0.5

    _safe_langfuse(
        langfuse.update_current_span,
        input={"answer": answer, "context": context},
        output={"hallucination_score": result},
        metadata={
            "method": "substring-match",
            "interpretation": "0=grounded, 0.5=hallucinated",
        },
    )

    return result
