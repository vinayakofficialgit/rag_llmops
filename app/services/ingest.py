
# from app.utils.embeddings import get_embedding
# from app.utils.vectorstore import upsert_vector

# def ingest_data(p):
#     t=p.get("text")
#     upsert_vector(t,get_embedding(t))
#     return {"status":"ingested"}


from app.utils.embeddings import get_embedding
from app.utils.vectorstore import upsert_vector

def ingest_data(payload):
    text = payload.get("text")

    if not text:
        return {"error": "text field is required"}

    embedding = get_embedding(text)
    upsert_vector(text, embedding)

    return {"status": "ingested"}