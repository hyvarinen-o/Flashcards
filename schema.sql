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

CREATE TABLE Category_options(
    id INTEGER PRIMARY KEY,
    category_option TEXT UNIQUE NOT NULL,
    category_id INTEGER NOT NULL REFERENCES Categories,
    UNIQUE (category_id, category_option)
);

CREATE TABLE Decks_category_options(
    deck_id INTEGER NOT NULL REFERENCES Decks,
    option_id INTEGER NOT NULL REFERENCES Category_options,
    PRIMARY KEY (deck_id, option_id)
);

CREATE TABLE Comments(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES Users,
    content TEXT NOT NULL,
    deck_id INTEGER NOT NULL REFERENCES Decks,
    created_at TEXT
);