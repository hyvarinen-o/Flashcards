import db

def get_decks():
    sql = """SELECT d.id, d.name, d.description, COUNT(c.id) total, d.created_at
            FROM Decks d, Cards c
            WHERE c.deck_id = d.id
            GROUP BY d.id
            ORDER BY d.id DESC"""

    return db.query(sql)

def get_deck(deck_id):
    sql = """SELECT d.id, d.name, d.description, d.created_at, u.username
            FROM Decks d JOIN Users u
            WHERE d.id = ? AND d.user_id = u.id"""
    return db.query(sql, params=[deck_id])[0]


def get_cards(deck_id):
    sql = "SELECT * FROM Cards WHERE deck_id = ?"
    return db.query(sql, params=[deck_id])


def create_deck(name, description, user_id):
    sql = "INSERT INTO Decks (name, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, params=[name, description, user_id])
    deck_id = db.last_insert_id()
    return deck_id

def add_card(question, answer, deck_id):
    sql = "INSERT INTO Cards (question, answer, deck_id) VALUES (?, ?, ?)"
    db.execute(sql, params=[question, answer, deck_id])
    return True
