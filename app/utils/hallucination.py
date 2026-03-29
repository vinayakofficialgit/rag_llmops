from langfuse import observe

from app.observability.tracing import langfuse


@observe(as_type="evaluator", name="hallucination-check")
def score(answer: str, context: str) -> float:
    """
    Simple grounding check tracked as a Langfuse *evaluator* span.

    Score interpretation:
      0.0 → answer is grounded in context
      0.5 → potential hallucination (context not found in answer)

    Replace with an LLM-based faithfulness scorer (e.g. RAGAS) for production.
    """
    result = 0.0 if context and context in answer else 0.5

    langfuse.update_current_span(
        input={"answer": answer, "context": context},
        output={"hallucination_score": result},
        metadata={
            "method": "substring-match",
            "interpretation": "0=grounded, 0.5=hallucinated",
        },
    )

    return result
