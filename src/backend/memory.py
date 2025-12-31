import sqlite3
import datetime
import json
import os

class MemoryManager:
    def __init__(self, db_path="app_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(conversation_id) REFERENCES conversations(id)
            )
        ''')

        # Long-term memory (for "remember important data")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Reminders
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                reminder_time TIMESTAMP,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def create_conversation(self, title="New Chat"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversations (title) VALUES (?)", (title,))
        conv_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return conv_id

    def get_conversations(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, created_at FROM conversations ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete_conversation(self, conversation_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        conn.commit()
        conn.close()

    def add_message(self, conversation_id, role, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                       (conversation_id, role, content))
        conn.commit()
        conn.close()

    def get_messages(self, conversation_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at ASC", (conversation_id,))
        rows = cursor.fetchall()
        conn.close()
        # Convert to list of dicts
        return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in rows]

    def add_memory(self, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO long_term_memory (content) VALUES (?)", (content,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_memories(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM long_term_memory ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]

    def add_reminder(self, message, reminder_time_str):
        """reminder_time_str should be ISO format or acceptable by sqlite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reminders (message, reminder_time) VALUES (?, ?)", (message, reminder_time_str))
        conn.commit()
        conn.close()

    def get_pending_reminders(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute("SELECT id, message, reminder_time FROM reminders WHERE completed = 0 AND reminder_time <= ?", (now,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def mark_reminder_complete(self, reminder_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE reminders SET completed = 1 WHERE id = ?", (reminder_id,))
        conn.commit()
        conn.close()
