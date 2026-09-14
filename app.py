import sqlite3
from flask import Flask
from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import db
from flask import session
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "Error, passwords don't match"

    password_hash = generate_password_hash(password1)
    try:
        sql = "INSERT INTO Users (username, created_at, password_hash) VALUES (?, datetime('now'), ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "username already taken"
    return redirect("/")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM Users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "Wrong username or password"

@app.route("/logout", methods=["POST"])
def logout():
    del session["username"]
    return redirect("/")