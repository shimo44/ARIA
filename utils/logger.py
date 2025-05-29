import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "aria_memory.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, aria TEXT)"
    )
    conn.commit()
    conn.close()

def log_interaction(user, aria):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memory (user, aria) VALUES (?, ?)", (user, aria))
    conn.commit()
    conn.close()

def get_memory_entries(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user, aria FROM memory ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    return "\n".join([f"User: {u}\nAria: {a}" for u, a in rows])

def clear_memory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memory")
    conn.commit()
    conn.close()
