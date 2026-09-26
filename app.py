import sqlite3, datetime
from flask import Flask
from flask import redirect, render_template, request, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db, decks
from flask import session
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    deck_list = decks.get_decks()
    return render_template("index.html", deck_list=deck_list)


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

    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    session_query = db.query(sql, [username])[0]
    password_hash = session_query[1]
    user_id = session_query[0]
    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/")
    else:
        return "Wrong username or password"

@app.route("/logout", methods=["POST"])
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")


@app.route("/new_deck")
def new_deck():
    try:
        if session["user_id"]:
            return render_template("new_deck.html")
    except KeyError:
        abort(403)

@app.route("/create_deck", methods=["POST"])
def create_deck():
    name = request.form["name"]
    description = request.form["description"]
    if name != "" and description != "":
        thread_id = decks.create_deck(name, description, session["user_id"], datetime.datetime.now().date())
        return redirect("/deck/" + str(thread_id))

@app.route("/deck/<int:deck_id>")
def show_deck(deck_id):
    deck = decks.get_deck(deck_id)
    cards = decks.get_cards(deck_id)
    if not deck:
        abort(404)
    return render_template("deck.html", deck=deck, cards=cards, new_card=False)

@app.route("/new_card_form/<int:deck_id>")
def add_card_form(deck_id):
    deck = decks.get_deck(deck_id)
    cards = decks.get_cards(deck_id)
    if not deck:
        abort(404)
    try:
        if deck[3] == session["user_id"]:
            return render_template("deck.html", deck=deck, cards=cards, new_card=True)
        else:
            abort(403)
    except KeyError:
        abort(403)

@app.route("/add_card", methods=["POST"])
def add_card():
    question = request.form["question"]
    answer = request.form["answer"]
    deck_id = request.form["deck_id"]
    decks.add_card(question, answer, deck_id)
    return redirect("/deck/" + str(deck_id))


@app.route("/edit_deck/<int:deck_id>")
def edit_cards(deck_id):
    cards = decks.get_cards(deck_id)
    deck = decks.get_deck(deck_id)
    if not deck:
        abort(404)
    try:
        if deck[3] == session["user_id"]:
            return render_template("edit_deck.html", cards=cards, deck_id=deck_id, card_id=-1)
        else:
            abort(403)
    except KeyError:
        abort(403)

@app.route("/edit_card/delete/<int:card_id>", methods=["POST"])
def delete_card(card_id):
    #Only accessible by post method so users cant type the route in the address bar and delete cards
    deck_id = decks.delete_card(card_id)
    return redirect("/edit_deck/" + str(deck_id))

@app.route("/edit_card/edit/<int:deck_id>/<int:card_id>", methods=["POST"])
def edit_card(deck_id, card_id):    
    cards = decks.get_cards(deck_id)
    return render_template("edit_deck.html", cards=cards, deck_id=deck_id, card_id=card_id)

@app.route("/edit_card/update/<int:card_id>", methods=["POST"])
def update_card(card_id):
    updated_question = request.form["question"]
    updated_answer = request.form["answer"]
    deck_id = decks.update_card(card_id, updated_question, updated_answer)
    return redirect("/edit_deck/" + str(deck_id))

@app.route("/search")
def search():
    query = request.args.get("query")
    results = decks.search(query)
    return render_template("search.html", results=results, query=query)

