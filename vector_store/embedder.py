"""Embed schema documentation into PostgreSQL via PGVector.

Uses local sentence-transformers model BAAI/bge-base-en-v1.5 (768 dimensions).
"""

import time
import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import get_settings
from vector_store.schema_docs import SCHEMA_DOCS


def get_embeddings_model() -> HuggingFaceEmbeddings:
    """Get the BGE-base-en-v1.5 embeddings model (locally downloaded)."""
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_embedding(text: str, embeddings_model: HuggingFaceEmbeddings) -> list[float]:
    """Get embedding for a text string."""
    return embeddings_model.embed_query(text)


def embed_all_schema_docs() -> None:
    """Embed all schema docs and store in PostgreSQL schema_embeddings table.

    Idempotent -- skips docs that already exist by doc_id.
    """
    settings = get_settings()
    embeddings_model = get_embeddings_model()

    conn = psycopg2.connect(settings.postgres_url)
    register_vector(conn)
    cursor = conn.cursor()

    for doc in SCHEMA_DOCS:
        print(f"  Embedding: {doc['title']}")
        try:
            embedding = get_embedding(doc["content"], embeddings_model)
        except Exception as emb_err:
            print(f"    [FAIL] Could not embed {doc['doc_id']}: {emb_err}")
            continue
        embedding_array = np.array(embedding, dtype=np.float32)

        cursor.execute(
            """INSERT INTO schema_embeddings (doc_id, domain, title, content, embedding)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (doc_id) DO UPDATE SET
                   domain = EXCLUDED.domain,
                   title = EXCLUDED.title,
                   content = EXCLUDED.content,
                   embedding = EXCLUDED.embedding""",
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
