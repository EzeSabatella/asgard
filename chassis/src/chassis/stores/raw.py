import aiosqlite
from pathlib import Path
from typing import List, Optional
from chassis.stores.base import BaseStore
from chassis.models.events import BaseEvent


class RawStore(BaseStore):
    """
    SQLite implementation of BaseStore.
    In production, SQLite file is encrypted with SQLCipher.
    In development/tests, runs without encryption.
    """

    def __init__(self, db_path: Path, encryption_key: Optional[str] = None):
        self.db_path = db_path
        self.encryption_key = encryption_key  # None = no encryption (dev/test)
        self._db: Optional[aiosqlite.Connection] = None

    async def initialize(self) -> None:
        """Creates tables if they don't exist. Idempotent — safe to call multiple times."""
        if self._db is not None:
            return

        if self.encryption_key:
            from sqlcipher3 import dbapi2 as sqlite3_cipher
            self._db = await aiosqlite.connect(self.db_path, module=sqlite3_cipher)
            await self._db.execute(f"PRAGMA key='{self.encryption_key}'")
        else:
            self._db = await aiosqlite.connect(self.db_path)

        self._db.row_factory = aiosqlite.Row

        await self._db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id    TEXT PRIMARY KEY,
                event_type  TEXT NOT NULL,
                source      TEXT NOT NULL,
                content     TEXT NOT NULL,
                created_at  TEXT NOT NULL,
                consolidated INTEGER NOT NULL DEFAULT 0
            )
        """)
        await self._db.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_consolidated
            ON events (consolidated, created_at)
        """)
        await self._db.commit()

    async def save_event(self, event: BaseEvent) -> str:
        """Stores event with consolidated=False regardless of input."""
        event_copy = event.model_copy()
        event_copy.consolidated = False

        await self._db.execute(
            "INSERT INTO events (event_id, event_type, source, content, created_at, consolidated) VALUES (?, ?, ?, ?, ?, ?)",
            (
                event_copy.id,
                type(event_copy).__name__,
                event_copy.source,
                event_copy.model_dump_json(),
                event_copy.ts.isoformat(),
                0,
            ),
        )
        await self._db.commit()
        return event_copy.id

    async def save_events(self, events: List[BaseEvent]) -> List[str]:
        """Atomic batch insert, all with consolidated=False."""
        if not events:
            return []

        event_ids = []
        rows = []
        for event in events:
            event_copy = event.model_copy()
            event_copy.consolidated = False
            event_ids.append(event_copy.id)
            rows.append((
                event_copy.id,
                type(event_copy).__name__,
                event_copy.source,
                event_copy.model_dump_json(),
                event_copy.ts.isoformat(),
                0,
            ))

        await self._db.executemany(
            "INSERT INTO events (event_id, event_type, source, content, created_at, consolidated) VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )
        await self._db.commit()
        return event_ids

    async def get_unconsolidated(self, limit: int = 100) -> List[BaseEvent]:
        cursor = await self._db.execute(
            "SELECT content FROM events WHERE consolidated = 0 ORDER BY created_at ASC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [BaseEvent.model_validate_json(row["content"]) for row in rows]

    async def mark_consolidated(self, event_ids: List[str]) -> int:
        if not event_ids:
            return 0

        placeholders = ",".join(["?"] * len(event_ids))
        cursor = await self._db.execute(
            f"UPDATE events SET consolidated = 1 WHERE event_id IN ({placeholders})",
            event_ids,
        )
        await self._db.commit()
        return cursor.rowcount

    async def get_by_id(self, event_id: str) -> Optional[BaseEvent]:
        cursor = await self._db.execute(
            "SELECT content FROM events WHERE event_id = ?",
            (event_id,),
        )
        row = await cursor.fetchone()
        if row:
            return BaseEvent.model_validate_json(row["content"])
        return None