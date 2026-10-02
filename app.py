import datetime
from flask import Flask
from flask import redirect, render_template, request, abort
from flask import session, flash
from werkzeug.security import generate_password_hash
import decks, users
import config

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    deck_list = decks.get_decks()
    category_list = decks.get_categories_for_decks()
    ratings_list = decks.get_ratings_for_decks()
    return render_template("index.html", deck_list=deck_list, ratings_list=ratings_list, category_list=category_list)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash("ERROR: passwords must match")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        password_hash = generate_password_hash(password1)
        date = datetime.datetime.now().date()
        result = users.create_user(username, password_hash, date)
        if not result:
            flash("ERROR: Username taken")
            return render_template("register.html", filled={})

        session["username"] = username
        session["user_id"] = result
        session["csrf_token"] = config.generate_csrf_token()
        return redirect("/")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)
    if user_id == None:
        flash("ERROR: Incorrect username or password")
        return redirect("/login_page")
    session["username"] = username
    session["user_id"] = user_id
    session["csrf_token"] = config.generate_csrf_token()
    return redirect("/")

@app.route("/logout", methods=["POST"])
def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/new_deck")
def new_deck():
    require_login()
    return render_template("new_deck.html")

@app.route("/create_deck", methods=["POST"])
def create_deck():
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = request.form["name"]
    description = request.form["description"]
    date = datetime.datetime.now().date()
    thread_id = decks.create_deck(name, description, session["user_id"], date)
    return redirect("/deck/" + str(thread_id))

@app.route("/deck/<int:deck_id>")
def show_deck(deck_id):
    deck = decks.get_deck(deck_id)
    cards = decks.get_cards(deck_id)
    categories = decks.get_categories_for_deck(deck_id)
    ratings = decks.get_rating_for_deck(deck_id)    
    if not deck:
        abort(404)
    return render_template("deck.html", deck=deck, cards=cards, categories=categories, ratings=ratings, new_card=False)

@app.route("/new_card_form/<int:deck_id>")
def add_card_form(deck_id):
    require_login()
    deck = decks.get_deck(deck_id)
    cards = decks.get_cards(deck_id)
    if not deck:
        abort(404)

    if deck[3] == session["user_id"]:
        return render_template("deck.html", deck=deck, cards=cards, new_card=True)
    abort(403)

@app.route("/add_card", methods=["POST"])
def add_card():
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    question = request.form["question"]
    answer = request.form["answer"]
    deck_id = request.form["deck_id"]
    decks.add_card(question, answer, deck_id)
    return redirect("/deck/" + str(deck_id))


@app.route("/edit_deck/<int:deck_id>")
def edit_cards(deck_id):
    require_login()
    cards = decks.get_cards(deck_id)
    deck = decks.get_deck(deck_id)
    if not deck:
        abort(404)

    if deck[3] == session["user_id"]:
        return render_template("edit_deck.html", cards=cards, deck_id=deck_id, card_id=-1)
    abort(403)

@app.route("/edit_card/delete/<int:card_id>", methods=["POST"])
def delete_card(card_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    deck_id = decks.delete_card(card_id)
    return redirect("/edit_deck/" + str(deck_id))

@app.route("/edit_card/edit/<int:deck_id>/<int:card_id>", methods=["POST"])
def edit_card(deck_id, card_id):
    require_login()
    cards = decks.get_cards(deck_id)
    return render_template("edit_deck.html", cards=cards, deck_id=deck_id, card_id=card_id)

@app.route("/edit_card/update/<int:card_id>", methods=["POST"])
def update_card(card_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    updated_question = request.form["question"]
    updated_answer = request.form["answer"]
    deck_id = decks.update_card(card_id, updated_question, updated_answer)
    return redirect("/edit_deck/" + str(deck_id))

@app.route("/delete_deck/<int:deck_id>/verification")
def verify_deletion(deck_id):
    require_login()
    if decks.get_deck(deck_id)[3] != session["user_id"]:
            abort(403)
    return render_template("delete.html", deck_id = deck_id)

@app.route("/delete_deck/<int:deck_id>", methods=["POST"])
def delete_deck(deck_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if decks.get_deck(deck_id)[3] != session["user_id"]:
        abort(403)
    else:
        decks.delete_deck(deck_id)
    return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("query")
    results = decks.search(query)
    return render_template("search.html", results=results, query=query)

@app.route("/user/<int:user_id>/<username>")
def user_page(user_id, username):
    user = users.get_user(username)
    deck = decks.get_users_decks(user_id)
    return render_template("user.html", user=user, decks=deck)

@app.route("/categories/<int:deck_id>")
def category_page(deck_id):
    categories = decks.get_categories()
    return render_template("categories.html", categories=categories, deck_id=deck_id, new_category=False)

@app.route("/add_categories/<int:deck_id>", methods=["POST"])
def add_categories(deck_id):
    category_id_list = request.form.getlist("categories")
    for category_id in category_id_list:
        if decks.check_for_duplicate_category(category_id, deck_id):
            decks.add_category_to_deck(category_id, deck_id)
    return redirect("/deck/" + str(deck_id))

@app.route("/create_category")
def create_category_page():
    return render_template("new_category.html")

@app.route("/create_new_category", methods=["POST"])
def create_new_category():
    require_login()
    category = request.form["category"]
    if decks.check_existing_category(category):
        decks.create_category(category)
        flash("Category added successfully")
        return redirect("/create_category")
    flash("Category already exists!")
    return redirect("/create_category")

@app.route("/add_rating/<int:deck_id>", methods=["POST"])
def add_rating_to_deck(deck_id):
    require_login()
    rating = request.form["rating"]
    if decks.check_existing_rating(session["user_id"], deck_id):
        decks.add_rating_to_deck(session["user_id"], rating, deck_id)
        flash("Rating submitted. Thank you for rating this deck!")
        return redirect("/deck/" + str(deck_id))
    decks.update_rating(session["user_id"], rating, deck_id)
    flash("Your rating for this deck has been updated")
    return redirect("/deck/" + str(deck_id))
    