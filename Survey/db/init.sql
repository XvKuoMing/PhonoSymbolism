CREATE TABLE IF NOT EXISTS responses (
user_id INTEGER PRIMARY KEY,
firstly_chosen_group VARCHAR(100) NOT NULL,
associations VARCHAR(255) NOT NULL,
image TEXT NOT NULL,
is_interested VARCHAR(5) NOT NULL,
lastly_chosen_group VARCHAR(100) NOT NULL
);
