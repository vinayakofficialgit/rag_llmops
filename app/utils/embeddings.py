
# def get_embedding(t): return [float(ord(c)) for c in t[:10]]

def get_embedding(text):
    if not text:
        return []
    return [float(ord(c)) for c in text[:10]]