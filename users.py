import sqlite3
from werkzeug.security import check_password_hash
import db

def create_user(username, password_hash, date):
    try:
        sql = """INSERT INTO
            Users (username, created_at, password_hash)
            VALUES (?, ?, ?)"""
        db.execute(sql, [username, date, password_hash])
    except sqlite3.IntegrityError:
        return None
    return db.last_insert_id()


def check_login(username, password):
    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    result = db.query(sql, [username])
    if result != []:
        result = result[0]
        user_id = result[0]
        password_hash = result[1]
        if check_password_hash(password_hash, password):
            return user_id
        return None
        

def get_user(username):
    sql = """SELECT *
    FROM Users
    WHERE username = ?"""

    user = db.query(sql, params=[username])[0]
    return user
