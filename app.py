import sqlite3
from flask import Flask
from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password = request.form["password"]
    password_hash =generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username, created_at, password_hash) VALUES (?, datetime('now'), ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "username already taken"
    return "Tunnus luotu"