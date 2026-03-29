import time

from langfuse import observe

from app.observability.tracing import langfuse
from app.utils.embeddings import get_embedding
from app.utils.vectorstore import search_vector
from app.utils.llm import call_llm
from app.utils.hallucination import score
from app.db.mysql import insert_log


@observe(name="rag-query-pipeline")
def query_data(p: dict) -> dict:
    """
    Root RAG pipeline trace.

    Langfuse trace hierarchy:
      rag-query-pipeline  (trace)
        ├── text-embedding        (embedding span)
        ├── vector-search         (retriever span)
        ├── openai-chat           (generation span)
        └── hallucination-check   (evaluator span)
    """
    st = time.time()
    q = p.get("query", "")

    # Annotate the root trace with the user query
    langfuse.update_current_span(input=q, metadata={"pipeline": "rag-v1"})

    # --- RAG steps (each is a child span via their own @observe decorators) ---
    embedding = get_embedding(q)
    ctx = search_vector(embedding)
    r = call_llm(q, ctx)

    latency = round(time.time() - st, 3)
    h_score = score(r["answer"], ctx)

    # Enrich root trace with final outputs and metrics
    langfuse.update_current_span(
        output=r["answer"],
        metadata={
            "latency_seconds": latency,
            "tokens_total": r["tokens"],
            "cost_usd": r["cost"],
            "hallucination_score": h_score,
        },
    )

    # Post hallucination evaluation score so it appears in Langfuse Scores tab
    trace_id = langfuse.get_current_trace_id()
    if trace_id:
        langfuse.create_score(
            trace_id=trace_id,
            name="hallucination_score",
            value=h_score,
            data_type="NUMERIC",
            comment="0 = fully grounded, 0.5 = potential hallucination",
        )

    insert_log(
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

    return {"answer": r["answer"], "tokens": r["tokens"], "cost": r["cost"]}
