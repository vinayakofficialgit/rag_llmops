


import pymysql
from app.core.config import settings


def get_conn():
    print(f">>> [DB] Connecting via pymysql to {settings.DB_HOST}:{settings.DB_PORT or 3306}", flush=True)
    conn = pymysql.connect(
        host=settings.DB_HOST,
        port=int(settings.DB_PORT or 3306),
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        connect_timeout=5,
        read_timeout=5,
        write_timeout=5,
    )
    print(">>> [DB] Connected successfully", flush=True)
    return conn


def insert_log(data):
    conn = get_conn()
    cur = conn.cursor()
    q = """INSERT INTO query_logs(query,context,response,latency,tokens,cost,hallucination_score)
    VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(q, (
        data["query"], data["context"], data["response"],
        data["latency"], data["tokens"], data["cost"], data["hallucination_score"]
    ))
    conn.commit()
    cur.close()
    conn.close()
    print(">>> [DB] Insert complete", flush=True)