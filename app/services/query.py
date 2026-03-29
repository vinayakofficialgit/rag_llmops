



import time
import logging
import concurrent.futures

from langfuse import observe

from app.observability.tracing import langfuse
from app.utils.embeddings import get_embedding
from app.utils.vectorstore import search_vector
from app.utils.llm import call_llm
from app.utils.hallucination import score
from app.db.mysql import insert_log

logger = logging.getLogger(__name__)

# Thread pool for non-blocking DB writes
_db_executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)


def _safe_langfuse(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        logger.warning(f"Langfuse call failed (non-blocking): {e}")


def _safe_insert_log(data: dict) -> None:
    """Run insert_log with a hard 5-second timeout so it never blocks the response."""
    future = _db_executor.submit(insert_log, data)
    try:
        future.result(timeout=5)
        print(">>> [11] mysql log done", flush=True)
    except concurrent.futures.TimeoutError:
        future.cancel()
        print(">>> [11] mysql log TIMED OUT (skipped)", flush=True)
        logger.warning("MySQL insert_log timed out after 5s — skipped")
    except Exception as e:
        print(f">>> [11] mysql log FAILED: {e}", flush=True)
        logger.warning(f"MySQL insert_log failed: {e}")


@observe(name="rag-query-pipeline")
def query_data(p: dict) -> dict:
    print(">>> [1] query_data ENTERED", flush=True)
    st = time.time()
    q = p.get("query", "")
    print(f">>> [2] query = {q}", flush=True)

    _safe_langfuse(
        langfuse.update_current_span, input=q, metadata={"pipeline": "rag-v1"}
    )
    print(">>> [3] langfuse span updated", flush=True)

    embedding = get_embedding(q)
    print(f">>> [4] embedding done, len={len(embedding)}", flush=True)

    ctx = search_vector(embedding)
    print(f">>> [5] vector search done, ctx_len={len(ctx)}", flush=True)

    print(">>> [6] calling LLM...", flush=True)
    r = call_llm(q, ctx)
    print(f">>> [7] LLM done, answer_len={len(r.get('answer',''))}", flush=True)

    latency = round(time.time() - st, 3)
    h_score = score(r["answer"], ctx)
    print(f">>> [8] hallucination scored: {h_score}", flush=True)

    _safe_langfuse(
        langfuse.update_current_span,
        output=r["answer"],
        metadata={
            "latency_seconds": latency,
            "tokens_total": r["tokens"],
            "cost_usd": r["cost"],
            "hallucination_score": h_score,
        },
    )
    print(">>> [9] langfuse enrichment done", flush=True)

    try:
        trace_id = langfuse.get_current_trace_id()
        if trace_id:
            langfuse.create_score(
                trace_id=trace_id,
                name="hallucination_score",
                value=h_score,
                data_type="NUMERIC",
                comment="0 = fully grounded, 0.5 = potential hallucination",
            )
    except Exception as e:
        logger.warning(f"Langfuse score creation failed: {e}")
    print(">>> [10] langfuse score done", flush=True)

    # Non-blocking MySQL insert with timeout
    _safe_insert_log(
        {
            "query": q,
            "context": ctx,
            "response": r["answer"],
            "latency": latency,
            "tokens": r["tokens"],
            "cost": r["cost"],
            "hallucination_score": h_score,
        }
    )

    print(">>> [12] RETURNING RESPONSE", flush=True)
    return {"answer": r["answer"], "tokens": r["tokens"], "cost": r["cost"]}