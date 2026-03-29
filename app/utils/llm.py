



import logging

import httpx
from openai import OpenAI

from langfuse import observe

from app.core.config import settings
from app.observability.tracing import langfuse

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    http_client=httpx.Client(verify=False),
)

COST_PER_TOKEN = 0.000001


def _cost(tokens: int) -> float:
    return tokens * COST_PER_TOKEN


def _safe_langfuse(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Langfuse call failed (non-blocking): {e}")


@observe(as_type="generation", name="openai-chat")
def call_llm(query: str, context: str) -> dict:
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    messages = [{"role": "user", "content": prompt}]

    _safe_langfuse(
        langfuse.update_current_generation,
        model=settings.OPENAI_MODEL,
        input=messages,
    )

    try:
        res = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
        )

        ans = res.choices[0].message.content or ""
        usage = res.usage
        prompt_tokens = usage.prompt_tokens if usage else 0
        completion_tokens = usage.completion_tokens if usage else 0
        total_tokens = usage.total_tokens if usage else 0
        cost = _cost(total_tokens)

        _safe_langfuse(
            langfuse.update_current_generation,
            output=ans,
            usage_details={
                "input": prompt_tokens,
                "output": completion_tokens,
                "total": total_tokens,
            },
            cost_details={"total": cost},
            metadata={"finish_reason": res.choices[0].finish_reason},
        )

        return {"answer": ans, "tokens": total_tokens, "cost": cost}

    except Exception as e:
        _safe_langfuse(
            langfuse.update_current_generation,
            level="ERROR",
            status_message=str(e),
        )
        return {"answer": f"LLM error: {e}", "tokens": 0, "cost": 0.0}
