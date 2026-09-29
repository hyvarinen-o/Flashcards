CREATE TABLE Users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    created_at TEXT,
    password_hash TEXT NOT NULL,
    image BLOB
);

CREATE TABLE Decks(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    user_id INTEGER NOT NULL REFERENCES Users,
    created_at TEXT NOT NULL 
);

CREATE TABLE Cards(
    id INTEGER PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    deck_id INTEGER NOT NULL REFERENCES Decks,
    image BLOB
);

CREATE TABLE Categories(
    id INTEGER PRIMARY KEY,
    category TEXT UNIQUE NOT NULL
);

CREATE TABLE Decks_categories(
    id INTEGER PRIMARY KEY,
    deck_id INTEGER NOT NULL REFERENCES Decks,
    category_id INTEGER NOT NULL REFERENCES Categories
);

CREATE TABLE Comments(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES Users,
    content TEXT NOT NULL,
    deck_id INTEGER NOT NULL REFERENCES Decks,
    created_at TEXT
);