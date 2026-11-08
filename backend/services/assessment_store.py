"""SQLite persistence for assessment session state; no external service required."""
import json
import os
import sqlite3
from pathlib import Path
from threading import RLock
from config import SARTA_ASSESSMENT_DB

LOCK = RLock()

def _connect():
    path = Path(os.environ.get("SARTA_ASSESSMENT_DB", SARTA_ASSESSMENT_DB))
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=10)
    db.execute("CREATE TABLE IF NOT EXISTS assessment_sessions (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
    return db

def save_session(session):
    with LOCK, _connect() as db:
        db.execute("INSERT OR REPLACE INTO assessment_sessions(id,payload) VALUES (?,?)", (session["session_id"], json.dumps(session)))
        db.commit()

def load_session(session_id):
    with LOCK, _connect() as db:
        row = db.execute("SELECT payload FROM assessment_sessions WHERE id=?", (session_id,)).fetchone()
    return json.loads(row[0]) if row else None
