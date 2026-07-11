import sqlite3
from typing import Dict, Any
from src.config import DB_PATH

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS dataset_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_row_id INTEGER,
    source_text TEXT,
    target_text TEXT,
    is_valid BOOLEAN,
    gate_failed TEXT,
    error_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_gate_failed ON dataset_audit(gate_failed);
CREATE INDEX IF NOT EXISTS idx_is_valid ON dataset_audit(is_valid);
"""

class AuditDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Ensures the SQLite file and schema exist on boot."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA_SQL)

    def insert_record(self, record: Dict[str, Any]):
        """Inserts a single audited row into the database."""
        sql = """
        INSERT INTO dataset_audit
        (raw_row_id, source_text, target_text, is_valid, gate_failed, error_reason)
        VALUES (:raw_row_id, :source_text, :target_text, :is_valid, :gate_failed, :error_reason)
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(sql, record)

    def insert_batch(self, records: list):
        """Flushes a buffer of records to SQLite in a single hardware transaction."""
        sql = """
        INSERT INTO dataset_audit
        (raw_row_id, source_text, target_text, is_valid, gate_failed, error_reason)
        VALUES (:raw_row_id, :source_text, :target_text, :is_valid, :gate_failed, :error_reason)
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(sql, records)

    def get_summary_stats(self):
        """Quick helper to print our research paper metrics to the terminal."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT gate_failed, COUNT(*) FROM dataset_audit GROUP BY gate_failed")
            return cursor.fetchall()

    def reset_laboratory(self):
        """Drops the table and rebuilds it. Guarantees 100% pipeline idempotency."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DROP TABLE IF EXISTS dataset_audit")
        self._init_db()
