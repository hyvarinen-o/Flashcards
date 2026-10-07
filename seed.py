import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM Users")
db.execute("DELETE FROM Decks")
db.execute("DELETE FROM Cards")
db.execute("DELETE FROM Categories")
db.execute("DELETE FROM Decks_categories")
db.execute("DELETE FROM Rating")

user_count = 1000
deck_count = 10**5
card_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO Users (username, created_at, password_hash) VALUES (?, datetime('now'), ?)",
               ["user" + str(i), "ABC" + str(i)])

for i in range(1, deck_count + 1):
    db.execute("INSERT INTO Decks (name, description, user_id, created_at) VALUES (?, ?, ?, datetime('now'))",
               ["deck" + str(i), "desc" + str(i), random.randint(1, 1000)])

for i in range(1, card_count + 1):
    user_id = random.randint(1, user_count)
    deck_id = random.randint(1, deck_count)
    db.execute("""INSERT INTO Cards (question, answer, deck_id)
                  VALUES (?, ?, ?)""",
               ["question" + str(i), "answer" + str(i), deck_id])

db.commit()
db.close()