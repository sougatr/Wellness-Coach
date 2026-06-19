"""
Lightweight Usage Tracking for MetaWell
=========================================
Tracks page visits, form starts, and form submissions using a simple
SQLite file. No personal data is logged - only event counts and timestamps.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usage_tracking.db")


def _get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def log_event(event_name):
    try:
        conn = _get_connection()
        conn.execute(
            "INSERT INTO events (event_name, timestamp) VALUES (?, ?)",
            (event_name, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def get_summary():
    try:
        conn = _get_connection()
        cursor = conn.execute(
            "SELECT event_name, COUNT(*) FROM events GROUP BY event_name"
        )
        rows = cursor.fetchall()
        conn.close()
        return {name: count for name, count in rows}
    except Exception:
        return {}

