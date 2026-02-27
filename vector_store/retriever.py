"""Retrieve relevant schema context via PGVector cosine similarity search."""

import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from openai import OpenAI
from config.settings import get_settings


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
        conn = psycopg2.connect(settings.postgres_url)
        register_vector(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM schema_embeddings")
        count = cursor.fetchone()[0]
    except Exception:
        # If table doesn't exist or connection fails, use fallback
        from vector_store.schema_docs import SCHEMA_DOCS
        results = []
        for doc in SCHEMA_DOCS:
            if domain == "CROSS_DOMAIN" or doc["domain"] == domain:
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
        conn.close()
        from vector_store.schema_docs import SCHEMA_DOCS
        results = []
        for doc in SCHEMA_DOCS:
            if domain == "CROSS_DOMAIN" or doc["domain"] == domain:
                results.append({
                    "title": doc["title"],
                    "content": doc["content"],
                    "domain": doc["domain"],
                    "similarity": 1.0,
                })
        return results[:top_k]

    # Embed the query
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(
        input=[query],
        model="text-embedding-3-large",
    )
    query_embedding = np.array(response.data[0].embedding, dtype=np.float32)

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
    conn.close()

    return [
        {
            "title": row[0],
            "content": row[1],
            "domain": row[2],
            "similarity": float(row[3]),
        }
        for row in rows
    ]
