"""Embed schema documentation into PostgreSQL via PGVector.

Switched from OpenAI text-embedding-3-large to HuggingFace BAAI/bge-base-en-v1.5.
"""

import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
# from openai import OpenAI  # commented out -- switched to HuggingFace
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from config.settings import get_settings
from vector_store.schema_docs import SCHEMA_DOCS


def get_embedding(text: str, embeddings_model: HuggingFaceEndpointEmbeddings) -> list[float]:
    """Get BGE-base-en-v1.5 embedding for a text string via HuggingFace Inference API."""
    # OpenAI version (commented out):
    # response = client.embeddings.create(input=[text], model="text-embedding-3-large")
    # return response.data[0].embedding
    return embeddings_model.embed_query(text)


def embed_all_schema_docs() -> None:
    """Embed all schema docs and store in PostgreSQL schema_embeddings table.

    Idempotent -- skips docs that already exist by doc_id.
    """
    settings = get_settings()
    # OpenAI client (commented out):
    # client = OpenAI(api_key=settings.openai_api_key)

    embeddings_model = HuggingFaceEndpointEmbeddings(
        model="BAAI/bge-base-en-v1.5",
        huggingfacehub_api_token=settings.huggingface_api_key,
    )

    conn = psycopg2.connect(settings.postgres_url)
    register_vector(conn)
    cursor = conn.cursor()

    for doc in SCHEMA_DOCS:
        # Check if already exists
        cursor.execute(
            "SELECT 1 FROM schema_embeddings WHERE doc_id = %s", (doc["doc_id"],)
        )
        if cursor.fetchone():
            print(f"  Skipping {doc['doc_id']} -- already embedded")
            continue

        print(f"  Embedding: {doc['title']}")
        embedding = get_embedding(doc["content"], embeddings_model)
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
