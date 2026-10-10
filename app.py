import datetime, math
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
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    deck_count = decks.deck_count()
    page_count = math.ceil(deck_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    deck_list = decks.get_decks(page, page_size)
    category_list = decks.get_categories_for_decks()
    ratings_list = decks.get_ratings_for_decks()
    return render_template("index.html",
                        page=page,
                        page_count=page_count,
                        deck_list=deck_list,
                        ratings_list=ratings_list, 
                        category_list=category_list)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"].rstrip()
        password1 = request.form["password1"].rstrip()
        password2 = request.form["password2"].rstrip()
        if not username or not password1 or not password2 or len(username) > 30 or len(password1) > 100:
            flash("ERROR: Invalid username or password")
            return render_template("register.html", filled={})
        if len(username.strip(" ")) < 1 or len(password1.strip(" ")) < 1:
            flash("ERROR: Username and password must contain characters")
            return render_template("register.html", filled={})
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
    username = request.form["username"].rstrip()
    password = request.form["password"].rstrip()

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
    cards = []
    return render_template("new_deck.html", cards=cards)

@app.route("/add_card_field", methods=["POST"])
def add_card_field():
    deck_name = request.form["name"].rstrip()
    description = request.form["description"].rstrip()
    questions = request.form.getlist("questions[]")
    answers = request.form.getlist("answers[]")

    cards = []
    if questions and answers: 
        for q, a in zip(questions, answers):
            cards.append({"question": q, "answer": a})
        cards.append({"question": "", "answer": ""})
    else:
        cards.append({"question": "", "answer": ""})

    return render_template("new_deck.html", deck_name=deck_name, description=description, cards=cards)

@app.route("/create_deck", methods=["POST"])
def create_deck():
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = request.form["name"].rstrip()
    description = request.form["description"].rstrip()
    questions = request.form.getlist("questions[]")
    answers = request.form.getlist("answers[]")
    if not name or not description or len(name) > 30 or len(description) > 150:
        flash("Invalid name or description")
        return redirect("/new_deck")
    if len(name.strip(" ")) < 1 or len(description.strip(" ")) < 1:
        flash("Invalid name or description")
        return redirect("/new_deck")

    if questions and answers:
        cards = [] 
        for q, a in zip(questions, answers):
            if not q or not a or len(q) > 60 or len(a) > 60:
                flash("Invalid card parameters")
                return redirect("/new_deck")
            if len(q.strip(" ")) < 1 or len(a.strip(" ")) < 1:
                flash("Invalid card parameters")
                return redirect("/new_deck")
            cards.append({"question": q, "answer": a})

        date = datetime.datetime.now().date()
        deck_id = decks.create_deck(name, description, session["user_id"], date)
        for card in cards:
            decks.add_card(card["question"].rstrip(), card["answer"].rstrip(), deck_id)
        return redirect("/deck/" + str(deck_id))
    else:
        date = datetime.datetime.now().date()
        deck_id = decks.create_deck(name, description, session["user_id"], date)
        return redirect("/deck/" + str(deck_id))

@app.route("/deck/<int:deck_id>")
@app.route("/deck/<int:deck_id>/<int:page>")
def show_deck(deck_id, page=1):
    page_size = 5
    card_count = decks.card_count(deck_id)
    page_count = math.ceil(card_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/deck/" + str(deck_id) + "/1")
    if page > page_count:
        return redirect("/deck/" + str(deck_id) + "/" + str(page_count))

    deck = decks.get_deck(deck_id)
    cards = decks.get_cards(deck_id, page, page_size)
    categories = decks.get_categories_for_deck(deck_id)
    ratings = decks.get_rating_for_deck(deck_id)    
    if not deck:
        abort(404)
    return render_template("deck.html",
                           page=page,
                           page_count=page_count,
                           deck=deck,
                           cards=cards,
                           categories=categories,
                           ratings=ratings,
                           new_card=False)

@app.route("/new_card_form/<int:deck_id>")
@app.route("/new_card_form/<int:deck_id>/<int:page>")
def add_card_form(deck_id, page=0):
    require_login()
    page_size = 5
    card_count = decks.card_count(deck_id)
    page_count = math.ceil(card_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/new_card_form/" + str(deck_id) + "/1")
    if page > page_count:
        return redirect("/new_card_form/" + str(deck_id) + "/" + str(page_count))

    deck = decks.get_deck(deck_id)
    cards = decks.get_cards(deck_id, page, page_size)
    if not deck:
        abort(404)

    if deck[3] == session["user_id"]:
        return render_template("deck.html",
                               page=page,
                               page_count=page_count,
                               deck=deck, cards=cards,
                               new_card=True)
    abort(403)

@app.route("/add_card", methods=["POST"])
def add_card():
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    question = request.form["question"].rstrip()
    answer = request.form["answer"].rstrip()
    if not question or not answer or len(question) > 60 or len(answer) > 60:
        abort(403)
    if len(question.strip(" ")) < 1 or len(answer.strip(" ")) < 1:
        abort(403)
    deck_id = request.form["deck_id"]
    decks.add_card(question, answer, deck_id)
    return redirect("/deck/" + str(deck_id))


@app.route("/edit_deck/<int:deck_id>")
@app.route("/edit_deck/<int:deck_id>/<int:page>")
def edit_cards(deck_id, page=1):
    require_login()
    page_size = 5
    card_count = decks.card_count(deck_id)
    page_count = math.ceil(card_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/edit_deck/" + str(deck_id) + "/1")
    if page > page_count:
        return redirect("/edit_deck/" + str(deck_id) + "/" + str(page))
    

    cards = decks.get_cards(deck_id, page, page_size)
    deck = decks.get_deck(deck_id)
    if not deck:
        abort(404)

    if deck[3] == session["user_id"]:
        return render_template("edit_deck.html",
                               page=page,
                               page_count=page_count,
                               cards=cards,
                               deck=deck,
                               card_id=-1)
    abort(403)

@app.route("/edit_deck_name_and_description/<int:deck_id>", methods=["POST"])
def edit_deck_name(deck_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    name = request.form["deck_name"].rstrip()
    description = request.form["description"].rstrip()
    
    if not name or not description or len(name) > 30 or len(description) > 150:
        flash("Invalid name or description")
        return redirect("/edit_deck/" + str(deck_id))
    if len(name.strip(" ")) < 1 or len(description.strip(" ")) < 1:
        flash("Invalid name or description")
        return redirect("/edit_deck/" + str(deck_id))

    decks.update_deck(name, description, deck_id)
    flash("Changes applied")
    return redirect("/edit_deck/" + str(deck_id))

@app.route("/edit_card/delete/<int:card_id>", methods=["POST"])
def delete_card(card_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    deck_id = decks.delete_card(card_id)
    return redirect("/edit_deck/" + str(deck_id))

@app.route("/edit_card/edit/<int:deck_id>/<int:page>/<int:page_count>/<int:card_id>", methods=["POST"])
def edit_card(deck_id, page, page_count, card_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    cards = decks.get_cards(deck_id, page, 5)
    deck = decks.get_deck(deck_id)
    return render_template("edit_deck.html", page=page, page_conut=page_count, cards=cards, deck=deck, card_id=card_id)

@app.route("/edit_card/update/<int:deck_id>/<int:card_id>", methods=["POST"])
def update_card(deck_id, card_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    q = request.form["question"].rstrip()
    a = request.form["answer"].rstrip()
    if not q or not a or len(q) > 60 or len(a) > 60:
        flash("Invalid card parameters")
        return redirect("/edit_deck/" + str(deck_id))
    if len(q.strip(" ")) < 1 or len(a.strip(" ")) < 1:
        flash("Invalid card parameters")
        return redirect("/edit_deck/" + str(deck_id))
    deck_id = decks.update_card(card_id, q, a)
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
    query = request.args.get("query").rstrip()
    results = decks.search(query)
    return render_template("search.html", results=results, query=query)

@app.route("/user/<int:user_id>/<username>")
@app.route("/user/<int:user_id>/<username>/<int:page>")
def user_page(user_id, username, page=1):
    page_size = 5
    deck_count = decks.deck_count_for_user(user_id)
    page_count = math.ceil(deck_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/user/" + str(user_id) + "/" + str(username) + "/1")
    if page > page_count:
        return redirect("/user/" + str(user_id) + "/" + str(username) + "/" + str(page_count))
    
    user = users.get_user(username)
    deck_list = decks.get_users_decks(user_id, page, page_size)
    return render_template("user.html", page=page, page_count=page_count, user=user, decks=deck_list)

@app.route("/edit_categories/<int:deck_id>")
def category_edit_page(deck_id):
    require_login()
    deck = decks.get_deck(deck_id)
    if not deck or deck["user_id"] != session["user_id"]:
        abort(403)
    
    categories = decks.get_categories()
    decks_categories = decks.get_categories_for_deck(deck_id)
    return render_template("category_edit.html",
                           categories=categories,
                           deck_id=deck_id,
                           decks_categories = decks_categories)

@app.route("/add_categories/<int:deck_id>", methods=["POST"])
def add_categories(deck_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    category_id_list = request.form.getlist("categories")
    if category_id_list != []:
        for category_id in category_id_list:
            if decks.check_for_duplicate_category(category_id, deck_id):
                decks.add_category_to_deck(category_id, deck_id)
        return redirect("/deck/" + str(deck_id))
    flash("Please select atleast 1 category")
    return redirect("/edit_categories/" + str(deck_id))

@app.route("/delete_category_from_deck/<int:deck_id>/<int:category_id>", methods=["POST"])
def delete_category_from_deck(deck_id, category_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    decks.delete_category_from_deck(deck_id, category_id)
    return redirect("/edit_categories/" + str(deck_id))
    


@app.route("/create_category/<int:deck_id>", methods=["POST", "GET"])
def create_category_page(deck_id):
    require_login()
    return render_template("new_category.html", deck_id=deck_id)

@app.route("/create_new_category/<int:deck_id>", methods=["POST"])
def create_new_category(deck_id):
    require_login()
    category = request.form["category"].rstrip()
    if not category or len(category) > 50 or len(category.strip(" ")) < 1:
        flash("Invalid category")
    if decks.check_existing_category(category):
        decks.create_category(category)
        flash("Category added successfully")
        return redirect("/create_category/" + str(deck_id))
    flash("Category already exists!")
    return redirect("/create_category" + str(deck_id))

@app.route("/add_rating/<int:deck_id>", methods=["POST"])
def add_rating_to_deck(deck_id):
    require_login()
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    rating = request.form["rating"]
    if decks.check_existing_rating(session["user_id"], deck_id):
        decks.add_rating_to_deck(session["user_id"], rating, deck_id)
        flash("Rating submitted. Thank you for rating this deck!")
        return redirect("/deck/" + str(deck_id))
    decks.update_rating(session["user_id"], rating, deck_id)
    flash("Your rating for this deck has been updated")
    return redirect("/deck/" + str(deck_id))

@app.route("/category/<category>")
def category_page(category):
    deck_list = decks.get_decks_for_category(category)
    return render_template("category.html", category=category, deck_list=deck_list)