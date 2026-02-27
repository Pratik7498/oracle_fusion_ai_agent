"""Embed schema documentation into PostgreSQL via PGVector."""

import os
import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from openai import OpenAI
from config.settings import get_settings
from vector_store.schema_docs import SCHEMA_DOCS


def get_embedding(text: str, client: OpenAI) -> list[float]:
    """Get text-embedding-3-large embedding for a text string."""
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-large",
    )
    return response.data[0].embedding


def embed_all_schema_docs() -> None:
    """Embed all schema docs and store in PostgreSQL schema_embeddings table.

    Idempotent — skips docs that already exist by doc_id.
    """
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    conn = psycopg2.connect(settings.postgres_url)
    register_vector(conn)
    cursor = conn.cursor()

    for doc in SCHEMA_DOCS:
        # Check if already exists
        cursor.execute(
            "SELECT 1 FROM schema_embeddings WHERE doc_id = %s", (doc["doc_id"],)
        )
        if cursor.fetchone():
            print(f"  Skipping {doc['doc_id']} — already embedded")
            continue

        print(f"  Embedding: {doc['title']}")
        embedding = get_embedding(doc["content"], client)
        embedding_array = np.array(embedding, dtype=np.float32)

        cursor.execute(
            """INSERT INTO schema_embeddings (doc_id, domain, title, content, embedding)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (doc_id) DO NOTHING""",
            (
                doc["doc_id"],
                doc["domain"],
                doc["title"],
                doc["content"],
                embedding_array,
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("  Schema embedding complete.")
