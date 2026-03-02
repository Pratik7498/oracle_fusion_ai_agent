-- ============================================================
-- PGVector Extension + Schema Embeddings Table
-- ============================================================

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS schema_embeddings (
    id          SERIAL PRIMARY KEY,
    doc_id      VARCHAR(100) UNIQUE NOT NULL,
    domain      VARCHAR(30) NOT NULL,
    title       VARCHAR(200),
    content     TEXT NOT NULL,
    -- embedding   vector(3072),  -- OpenAI text-embedding-3-large (commented out)
    embedding   vector(768),     -- HuggingFace BAAI/bge-base-en-v1.5
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_schema_emb_domain ON schema_embeddings(domain);

-- IVFFlat index for cosine similarity search
-- Note: requires at least 10 rows before this index becomes useful
CREATE INDEX IF NOT EXISTS idx_schema_emb_vector ON schema_embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 10);
