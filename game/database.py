import sqlite3
import os
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self):
        self.db_path = Path("game_data.db")
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create scores table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    time INTEGER NOT NULL,
                    mines INTEGER NOT NULL,
                    board_size TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def add_user(self, username, password):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)',
                    (username, password)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id FROM users WHERE username = ? AND password = ?',
                (username, password)
            )
            result = cursor.fetchone()
            return result[0] if result else None
    
    def add_score(self, user_id, time, mines, board_size):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO scores (user_id, time, mines, board_size) VALUES (?, ?, ?, ?)',
                (user_id, time, mines, board_size)
            )
            conn.commit()
    
    def get_top_scores(self, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    users.username,
                    scores.time,
                    scores.mines,
                    scores.board_size,
                    scores.created_at
                FROM scores
                JOIN users ON users.id = scores.user_id
                ORDER BY scores.time ASC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()