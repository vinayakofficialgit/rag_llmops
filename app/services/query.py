
import time
from app.utils.embeddings import get_embedding
from app.utils.vectorstore import search_vector
from app.utils.llm import call_llm
from app.utils.hallucination import score
from app.db.mysql import insert_log

def query_data(p):
    st=time.time()
    q=p.get("query")
    ctx=search_vector(get_embedding(q))
    r=call_llm(q,ctx)

    lat=time.time()-st
    h=score(r["answer"],ctx)

    log={
        "query":q,"context":ctx,"response":r["answer"],
        "latency":lat,"tokens":r["tokens"],"cost":r["cost"],
        "hallucination_score":h
    }
    insert_log(log)

    return {"answer":r["answer"],"tokens":r["tokens"],"cost":r["cost"]}
