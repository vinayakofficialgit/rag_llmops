


"""
Langfuse v4 client initialization with SSL bypass for corporate networks.
"""

import os
from dotenv import load_dotenv

# ── Load .env FIRST so all env vars are available ──
load_dotenv()

# ── OTEL SSL bypass — must be set BEFORE importing langfuse ──
os.environ.setdefault("OTEL_EXPORTER_OTLP_TRACES_INSECURE", "true")
os.environ.setdefault("OTEL_EXPORTER_OTLP_INSECURE", "true")

import httpx
from langfuse import Langfuse, get_client

_httpx_client = httpx.Client(
    verify=False,
    timeout=httpx.Timeout(10.0, connect=5.0),
)

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
    httpx_client=_httpx_client,
)


def flush_langfuse() -> None:
    """Flush all pending Langfuse events (call on app shutdown)."""
    try:
        get_client().flush()
    except Exception:
        pass