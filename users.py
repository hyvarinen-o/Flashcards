import sqlite3
from werkzeug.security import check_password_hash
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


def check_login(username, password):
    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    result = db.query(sql, [username])[0]
    user_id = result[0]
    password_hash = result[1]
    if check_password_hash(password_hash, password):
        return user_id
    return None

