

import httpx
from openai import OpenAI
from app.core.config import settings

# Langfuse v4
from langfuse import observe

# OpenAI client
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    http_client=httpx.Client(verify=False),
)

def cost_calc(tokens):
    return tokens * 0.000001


@observe()  
def call_llm(query, context):
    prompt = f"Context:\n{context}\n\nQ:{query}"

    try:
        res = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        ans = res.choices[0].message.content
        tokens = res.usage.total_tokens if res.usage else 0

        return {
            "answer": ans,
            "tokens": tokens,
            "cost": cost_calc(tokens)
        }

    except Exception as e:
        return {
            "answer": f"LLM error: {str(e)}",
            "tokens": 0,
            "cost": 0.0
        }

