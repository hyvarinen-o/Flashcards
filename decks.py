import db

def get_decks():
    sql = """SELECT d.id, d.name, d.description, COUNT(c.id) AS total, d.created_at
            FROM Decks d LEFT JOIN Cards c ON c.deck_id = d.id
            GROUP BY d.id
            ORDER BY d.id DESC"""
    return db.query(sql)

def get_deck(deck_id):
    sql = """SELECT d.id, d.name, d.description, d.user_id, d.created_at, u.username
            FROM Decks d JOIN Users u
            WHERE d.id = ? AND d.user_id = u.id"""
    return db.query(sql, params=[deck_id])[0]


def get_cards(deck_id):
    sql = "SELECT * FROM Cards WHERE deck_id = ?"
    return db.query(sql, params=[deck_id])


def create_deck(name, description, user_id, created_at):
    sql = "INSERT INTO Decks (name, description, user_id, created_at) VALUES (?, ?, ?, ?)"
    db.execute(sql, params=[name, description, user_id, created_at])
    deck_id = db.last_insert_id()
    return deck_id

def add_card(question, answer, deck_id):
    sql = "INSERT INTO Cards (question, answer, deck_id) VALUES (?, ?, ?)"
    db.execute(sql, params=[question, answer, deck_id])
    return True

def delete_card(card_id):
    sql = "DELETE FROM Cards WHERE id = ? RETURNING deck_id"
    deck_id = db.execute(sql, [card_id])
    return deck_id[0][0]

def update_card(card_id, updated_question, updated_answer):
    sql = "UPDATE Cards SET question = ?, answer = ? WHERE id = ? RETURNING deck_id"
    deck_id = db.execute(sql, [updated_question, updated_answer, card_id])
    return deck_id[0][0]

def search(query):
    sql = """SELECT d.id AS deck_id,
                    d.name,
                    d.created_at,
                    u.username
             FROM Decks d
             JOIN Users u ON u.id = d.user_id
             WHERE d.name LIKE ?
             ORDER BY d.created_at DESC"""

    return db.query(sql, ["%" + query + "%"])