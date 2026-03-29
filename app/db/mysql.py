
import mysql.connector
from app.core.config import settings

def get_conn():
    return mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        connection_timeout=5,
    )

def insert_log(data):
    conn=get_conn()
    cur=conn.cursor()
    q="""INSERT INTO query_logs(query,context,response,latency,tokens,cost,hallucination_score)
    VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(q,(
        data["query"],data["context"],data["response"],
        data["latency"],data["tokens"],data["cost"],data["hallucination_score"]
    ))
    conn.commit()
    cur.close(); conn.close()
