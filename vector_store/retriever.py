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

    Args:
        query: Natural language query from user.
        domain: One of HCM, FINANCE, PROCUREMENT, CROSS_DOMAIN.
        top_k: Number of chunks to return.

    Returns:
        List of dicts with keys: title, content, domain, similarity.
    """
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    # Embed the query
    response = client.embeddings.create(
        input=[query],
        model="text-embedding-3-large",
    )
    query_embedding = np.array(response.data[0].embedding, dtype=np.float32)

    conn = psycopg2.connect(settings.postgres_url)
    register_vector(conn)
    cursor = conn.cursor()

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
