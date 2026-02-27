"""Database connection and query helpers using SQLAlchemy + psycopg2."""

import logging
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from config.settings import get_settings

logger = logging.getLogger(__name__)

_engine = None


def get_engine():
    """Return a singleton SQLAlchemy engine."""
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(
            settings.postgres_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )
    return _engine


def execute_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Execute a read-only SQL query and return results as a DataFrame.

    Returns an empty DataFrame on error — never raises.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text(sql), conn, params=params)
        return df
    except Exception as exc:
        logger.error("execute_query failed: %s | SQL: %s", exc, sql[:200])
        return pd.DataFrame()


def execute_write(sql: str, params: tuple | None = None) -> None:
    """Execute a write operation (INSERT / DDL) using psycopg2 directly."""
    settings = get_settings()
    conn = psycopg2.connect(settings.postgres_url)
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()
    except Exception as exc:
        conn.rollback()
        logger.error("execute_write failed: %s", exc)
    finally:
        conn.close()


def log_query(
    user_query: str,
    domain: str,
    generated_sql: str,
    response_summary: str,
    execution_time_ms: int,
) -> None:
    """Insert a row into ai_query_log for audit/debugging."""
    try:
        execute_write(
            """INSERT INTO ai_query_log
               (user_query, detected_domain, generated_sql, response_summary, execution_time_ms)
               VALUES (%s, %s, %s, %s, %s)""",
            (user_query, domain, generated_sql, response_summary, execution_time_ms),
        )
    except Exception as exc:
        logger.error("log_query failed: %s", exc)
