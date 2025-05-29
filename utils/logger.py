import os
import sqlite3

def log_interaction(prompt, response, log_file="logs/chatlog.txt"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"User: {prompt}\n")
        f.write(f"Aria: {response}\n\n")
    log_to_db(prompt, response)

def get_recent_context(log_file="logs/chatlog.txt", lines=10):
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            return "".join(f.readlines()[-lines:])
    except FileNotFoundError:
        return ""

def clear_memory(log_file="logs/chatlog.txt", db_file="logs/memory.db"):
    if os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("")
    if os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memory")
        conn.commit()
        conn.close()

def init_db(db_file="logs/memory.db"):
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_to_db(prompt, response, db_file="logs/memory.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memory (prompt, response) VALUES (?, ?)", (prompt, response))
    conn.commit()
    conn.close()

def get_memory_entries(limit=10, db_file="logs/memory.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT prompt, response FROM memory ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return "\n".join([f"User: {p}\nAria: {r}" for p, r in reversed(rows)])
