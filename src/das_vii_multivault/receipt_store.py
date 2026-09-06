from __future__ import annotations

import sqlite3
import threading

from .canonical import sha256_hex
from .models import ProtectedOutputValidationReceipt


class ReceiptStoreError(RuntimeError):
    pass


class ProtectedReceiptStore:
    """Local reference store.

    SQLite transactionality demonstrates commit-before-capability and consume-once state.
    It does NOT provide hardware rollback resistance or distributed atomicity.
    """

    def __init__(self, path: str = ":memory:"):
        self._db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self._lock = threading.Lock()
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS receipts (receipt_id TEXT PRIMARY KEY, digest TEXT NOT NULL, body TEXT NOT NULL)"
        )
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS consumed_capabilities (capability_id TEXT PRIMARY KEY, consumed_at REAL NOT NULL)"
        )

    def commit(self, receipt: ProtectedOutputValidationReceipt) -> str:
        digest = sha256_hex(receipt)
        body = repr(receipt)
        with self._lock:
            try:
                self._db.execute("BEGIN IMMEDIATE")
                self._db.execute(
                    "INSERT INTO receipts(receipt_id,digest,body) VALUES(?,?,?)",
                    (receipt.receipt_id, digest, body),
                )
                self._db.execute("COMMIT")
            except Exception:
                self._db.execute("ROLLBACK")
                raise
        return digest

    def contains_digest(self, receipt_id: str, digest: str) -> bool:
        row = self._db.execute("SELECT digest FROM receipts WHERE receipt_id=?", (receipt_id,)).fetchone()
        return bool(row and row[0] == digest)

    def consume_once(self, capability_id: str, consumed_at: float) -> bool:
        with self._lock:
            try:
                self._db.execute("BEGIN IMMEDIATE")
                self._db.execute(
                    "INSERT INTO consumed_capabilities(capability_id,consumed_at) VALUES(?,?)",
                    (capability_id, consumed_at),
                )
                self._db.execute("COMMIT")
                return True
            except sqlite3.IntegrityError:
                self._db.execute("ROLLBACK")
                return False
            except Exception:
                self._db.execute("ROLLBACK")
                raise
