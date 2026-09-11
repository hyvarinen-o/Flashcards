CREATE TABLE Users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE Decks(
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    user_id INTEGER REFERENCES Users,
    categories TEXT
);

CREATE TABLE Cards(
    id INTEGER PRIMARY KEY,
    question TEXT,
    answer TEXT,
    deck_id INTEGER REFERENCES Decks,
    image BLOB
);

CREATE TABLE Categories(
    id INTEGER PRIMARY KEY,
    category TEXT;
);

CREATE TABLE Sub_categories(
    id INTEGER PRIMARY KEY,
    sub_category TEXT,
    category_id INTEGER REFERENCES Categories
);