
store=[]
def upsert_vector(text,emb): store.append((text,emb))
def search_vector(e): return store[0][0] if store else ""
