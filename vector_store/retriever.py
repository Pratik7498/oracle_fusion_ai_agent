"""Retrieve relevant schema context via PGVector cosine similarity search.

Switched from OpenAI text-embedding-3-large to HuggingFace BAAI/bge-base-en-v1.5.
"""

import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from vector_store.embedder import get_embeddings_model
from config.settings import get_settings

# BGE models require this prefix for retrieval queries
_BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# Module-level caching for speed
_cached_model = None
_cached_conn = None


def _get_model():
    global _cached_model
    if _cached_model is None:
        _cached_model = get_embeddings_model()
    return _cached_model


def _get_conn():
    global _cached_conn
    settings = get_settings()
    if _cached_conn is None or _cached_conn.closed:
        _cached_conn = psycopg2.connect(settings.postgres_url)
        register_vector(_cached_conn)
    return _cached_conn

def retrieve_schema_context(
    query: str, domain: str, top_k: int = 3
) -> list[dict]:
    """Retrieve top-k most relevant schema documents for a query within a domain.

    Uses cosine similarity search via PGVector (<=> operator).
    Falls back to returning all schema docs if embeddings are not available.

    Args:
        query: Natural language query from user.
        domain: One of HCM, FINANCE, PROCUREMENT, CROSS_DOMAIN.
        top_k: Number of chunks to return.

    Returns:
        List of dicts with keys: title, content, domain, similarity.
    """
    settings = get_settings()

    # Check if schema_embeddings has data
    try:
        conn = _get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM schema_embeddings")
        count = cursor.fetchone()[0]
    except Exception:
        # If table doesn't exist or connection fails, use fallback
        from vector_store.schema_docs import SCHEMA_DOCS
        results = []
        for doc in SCHEMA_DOCS:
            if domain == "CROSS_DOMAIN" or doc["domain"] == domain or doc["domain"] == "ALL":
                results.append({
                    "title": doc["title"],
                    "content": doc["content"],
                    "domain": doc["domain"],
                    "similarity": 1.0,
                })
        return results[:top_k]

    # Fallback if no embeddings stored yet
    if count == 0:
        cursor.close()
        from vector_store.schema_docs import SCHEMA_DOCS
        results = []
        for doc in SCHEMA_DOCS:
            if domain == "CROSS_DOMAIN" or doc["domain"] == domain or doc["domain"] == "ALL":
                results.append({
                    "title": doc["title"],
                    "content": doc["content"],
                    "domain": doc["domain"],
                    "similarity": 1.0,
                })
        return results[:top_k]

    # Embed the query using local BGE model with query prefix
    embeddings_model = _get_model()
    prefixed_query = _BGE_QUERY_PREFIX + query
    raw_embedding = embeddings_model.embed_query(prefixed_query)
    query_embedding = np.array(raw_embedding, dtype=np.float32)

    if domain == "CROSS_DOMAIN":
        cursor.execute(
            """SELECT title, content, domain,
                      1 - (embedding <=> %s::vector) AS similarity
               FROM schema_embeddings
               ORDER BY embedding <=> %s::vector
               LIMIT %s""",
            (query_embedding, query_embedding, top_k),
        )
    else:
        cursor.execute(
            """SELECT title, content, domain,
                      1 - (embedding <=> %s::vector) AS similarity
               FROM schema_embeddings
               WHERE domain = %s
               ORDER BY embedding <=> %s::vector
               LIMIT %s""",
            (query_embedding, domain, query_embedding, top_k),
        )

    rows = cursor.fetchall()
    cursor.close()

    return [
        {
            "title": row[0],
            "content": row[1],
            "domain": row[2],
            "similarity": float(row[3]),
        }
        for row in rows
    ]
