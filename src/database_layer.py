import sqlite3
from datetime import datetime
conn=sqlite3.connect('chat.db',check_same_thread=False)
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_messages(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               session_id TEXT,
               role TEXT,
               content TEXT,
               created_at text
               )
""")

conn.commit()

def save_message(session_id:str,role:str,content:str):
    cursor.execute(
        "INSERT INTO chat_messages VALUES (NULL, ?, ?, ?, ?)",
        (session_id, role, content, datetime.utcnow().isoformat())
    )
    conn.commit()

def get_messages(session_id:str):
    cursor.execute(
        "SELECT role, content FROM chat_messages WHERE session_id=? ORDER BY id",
        (session_id,)
    )
    rows=cursor.fetchall()
    messages=[{"role":r,"content":c} for r,c in rows]
    return messages