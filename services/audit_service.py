
import sqlite3
from pathlib import Path
from datetime import datetime


# ==========================================
# AUDIT DATABASE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

DATABASE_PATH = LOG_DIR / "audit.db"


# ==========================================
# INITIALIZE AUDIT DATABASE
# ==========================================

def initialize_audit_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            event_type TEXT NOT NULL,

            category TEXT,

            user_message TEXT,

            response_status TEXT NOT NULL,

            error_message TEXT

        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# RECORD AUDIT EVENT
# ==========================================

def log_event(
    event_type,
    category="GENERAL",
    user_message="",
    response_status="SUCCESS",
    error_message=None
):

    initialize_audit_database()

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    timestamp = datetime.now().astimezone().isoformat()

    cursor.execute("""
        INSERT INTO audit_logs (
            timestamp,
            event_type,
            category,
            user_message,
            response_status,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        event_type,
        category,
        user_message,
        response_status,
        error_message
    ))

    connection.commit()
    connection.close()


# ==========================================
# FETCH AUDIT LOGS
# ==========================================

def get_audit_logs(limit=100):

    initialize_audit_database()

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    logs = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return logs
