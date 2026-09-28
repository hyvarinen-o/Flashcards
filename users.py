import sqlite3
import db

def create_user(username, password_hash):
    try:
        sql = """INSERT INTO
            Users (username, created_at, password_hash)
            VALUES (?, datetime('now'), ?)"""
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return None
    return db.last_insert_id()
