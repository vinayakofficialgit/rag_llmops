"""
Langfuse v4 client initialization.

Reads credentials from environment variables:
    LANGFUSE_PUBLIC_KEY
    LANGFUSE_SECRET_KEY
    LANGFUSE_HOST  (default: https://cloud.langfuse.com)

The singleton client is shared across the app and used with:
  - @observe() decorator for automatic span creation
  - langfuse.update_current_span() / update_current_generation() for enrichment
  - langfuse.create_score() for evaluation scores
  - langfuse.get_current_trace_id() for correlating logs
"""

import os
from langfuse import Langfuse, get_client

# Initialise once at import time; uses env vars automatically.
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)


def flush_langfuse() -> None:
    """Flush all pending Langfuse events (call on app shutdown)."""
    get_client().flush()
