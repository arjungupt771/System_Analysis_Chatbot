

import sqlite3
from datetime import datetime

DB_NAME = "chatmate_ai.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Ensure the table is created with the correct schema
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- auto-increment message_id
            chat_id TEXT NOT NULL,                         -- chat_id for identifying a chat
            role TEXT NOT NULL,                            -- Role (e.g., user, assistant)
            message TEXT NOT NULL,                         -- The chat message
            timestamp TEXT NOT NULL                        -- Timestamp of the message
        )
    ''')
    conn.commit()
    conn.close()
    

def delete_chat(chat_id):
    conn = sqlite3.connect("DB_NAME")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()


def save_message(chat_id, role, message):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    # Insert a new message into the 'chats' table
    c.execute("INSERT INTO chats (chat_id, role, message, timestamp) VALUES (?, ?, ?, ?)", 
              (chat_id, role, message, timestamp))
    conn.commit()
    conn.close()

def load_chat_history(chat_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Fetch chat history for the given chat_id, sorted by timestamp
    c.execute("SELECT role, message FROM chats WHERE chat_id=? ORDER BY timestamp", (chat_id,))
    rows = c.fetchall()
    conn.close()
    # Return the history in the expected format
    return [{"role": role, "parts": [msg]} for role, msg in rows]

def get_all_chat_ids():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Fetch all unique chat_id values
    c.execute("SELECT DISTINCT chat_id FROM chats")
    ids = [row[0] for row in c.fetchall()]
    conn.close()
    return ids
