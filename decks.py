import db


def get_decks():
    sql = """
    SELECT 
        d.id,
        d.name,
        d.description,
        u.username,
        COUNT(c.id) AS total,
        d.created_at,
        d.user_id
    FROM Decks d
    LEFT JOIN Cards c ON c.deck_id = d.id
    LEFT JOIN Users u ON u.id = d.user_id
    GROUP BY d.id, d.name, d.description, u.username, d.created_at
    ORDER BY d.id DESC
    """
    result = db.query(sql)
    return result

def get_deck(deck_id):
    sql = """SELECT d.id, d.name, d.description, d.user_id, d.created_at, u.username
            FROM Decks d JOIN Users u
            WHERE d.id = ? AND d.user_id = u.id"""
    result = db.query(sql, params=[deck_id])
    return result[0] if result else None

def get_users_decks(user_id):
    sql = """
    SELECT 
        d.id,
        d.name,
        d.description,
        COUNT(c.id) AS total,
        d.created_at
    FROM Decks d
    LEFT JOIN Cards c ON c.deck_id = d.id
    WHERE d.user_id = ?
    GROUP BY d.id, d.name, d.description, d.created_at
    ORDER BY d.id DESC
    """
    result = db.query(sql, params=[user_id])
    return result

def get_cards(deck_id):
    sql = "SELECT id, question, answer, deck_id FROM Cards WHERE deck_id = ?"
    result = db.query(sql, params=[deck_id])
    return result

def create_deck(name, description, user_id, created_at):
    sql = """INSERT INTO
            Decks (name, description, user_id, created_at)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, params=[name, description, user_id, created_at])
    deck_id = db.last_insert_id()
    return deck_id

def update_deck(deck_name, description, deck_id):
    sql = """UPDATE Decks
            SET name = ?, description = ?
            WHERE id = ?"""
    result = db.execute(sql, params=[deck_name, description, deck_id])
    return deck_id
    

def add_card(question, answer, deck_id):
    sql = """INSERT INTO
            Cards (question, answer, deck_id)
            VALUES (?, ?, ?)"""
    db.execute(sql, params=[question, answer, deck_id])
    return True

def delete_card(card_id):
    sql = """DELETE FROM
            Cards WHERE id = ?
            RETURNING deck_id"""
    deck_id = db.execute(sql, [card_id])
    return deck_id[0][0]

def update_card(card_id, updated_question, updated_answer):
    sql = """UPDATE Cards 
            SET question = ?, answer = ? WHERE id = ?
            RETURNING deck_id"""
    deck_id = db.execute(sql, [updated_question, updated_answer, card_id])
    return deck_id[0][0]

def delete_deck(deck_id):
    sql1 = "DELETE FROM Decks WHERE id = ?"
    sql2 = "DELETE FROM Cards WHERE deck_id = ?"
    result = db.execute(sql2, params=[deck_id])
    result = db.execute(sql1, params=[deck_id])
    return True

def search(query):
    sql = """SELECT d.id AS deck_id,
                    d.name,
                    d.created_at,
                    u.username
             FROM Decks d
             JOIN Users u ON u.id = d.user_id
             LEFT JOIN Decks_categories dc ON dc.deck_id = d.id
             JOIN Categories c on dc.category_id = c.id 
             WHERE (d.name LIKE ?
             OR u.username LIKE ?
             OR d.description LIKE ?
             OR c.category LIKE ?)
             ORDER BY d.created_at DESC"""
    
    query_sql = "%" + query + "%"
    return db.query(sql, [query_sql, query_sql, query_sql, query_sql])

def get_categories():
    sql = "SELECT id, category FROM Categories"
    result = db.query(sql)
    return result

def check_existing_category(category):
    sql = "SELECT id, category From Categories WHERE category = ?"
    result = db.query(sql, params=[category])
    if result == []:
        return True
    return False

def create_category(category):
    sql = """INSERT INTO
            Categories (category)
            VALUES (?)"""
    result = db.execute(sql, params=[category])
    return result

def add_category_to_deck(category_id, deck_id):
    sql = """INSERT INTO
            Decks_categories (deck_id, category_id)
            VALUES (?, ?)"""
    result = db.execute(sql, params=[deck_id, category_id])
    return result

def check_for_duplicate_category(category_id, deck_id):
    sql = """SELECT id, deck_id, category_id FROM Decks_categories
            WHERE category_id = ? AND deck_id = ?"""
    result = db.query(sql, params=[category_id, deck_id])
    if result == []:
        return True
    return False

def get_categories_for_decks():
    sql = """SELECT d.deck_id, c.category
        FROM Decks_categories d
        JOIN Categories c
        ON c.id = d.category_id"""
    result = db.query(sql)
    return result

def get_categories_for_deck(deck_id):
    sql = """ SELECT c.category
        FROM Decks_categories d
        JOIN Categories c
        ON c.id = d.category_id AND d.deck_id = ?"""
    result = db.query(sql, params=[deck_id])
    return result

def get_decks_for_category(category):
    sql = """SELECT c.category, d.name, d.description,
            d.created_at, u.username, d.id
            FROM Decks d JOIN Users u ON d.user_id = u.id
            LEFT JOIN Decks_categories dc ON dc.deck_id = d.id 
            JOIN Categories c ON dc.category_id = c.id
            WHERE c.category = ?
            GROUP BY d.id, d.name, d.description, d.created_at, u.username, c.category"""
    result = db.query(sql, params=[category])
    return result

def get_ratings_for_decks():
    sql = """SELECT deck_id, ROUND(AVG(rating), 1) as average
            FROM Rating
            GROUP BY deck_id"""
    result = db.query(sql)
    return result
    

def get_rating_for_deck(deck_id):
    sql = """SELECT ROUND(AVG(rating), 1) as average, COUNT(rating) as count 
            FROM Rating 
            WHERE deck_id = ?
            GROUP BY deck_id"""
    result = db.query(sql, params=[deck_id])
    if len(result) == 0:
        return result
    return result[0]

def add_rating_to_deck(user_id, rating, deck_id):
    sql = """INSERT INTO
        Rating (user_id, rating, deck_id)
        VALUES (?, ? ,?)"""
    result = db.execute(sql, params=[user_id, rating, deck_id])
    return result

def check_existing_rating(user_id, deck_id):
    sql = "SELECT id, user_id, rating, deck_id FROM Rating WHERE user_id = ? AND deck_id = ?"
    result = db.query(sql, params=[user_id, deck_id])
    if result == []:
        return True
    return False

def update_rating(user_id, rating, deck_id):
    sql = """UPDATE Rating
        SET rating = ?
        WHERE user_id = ? AND deck_id = ?"""
    result = db.execute(sql, params=[rating, user_id, deck_id])
    return result