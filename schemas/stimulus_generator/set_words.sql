CREATE TABLE set_words (
    set_id          INTEGER NOT NULL,
    word_id         INTEGER NOT NULL,
    PRIMARY KEY (set_id, word_id),
    FOREIGN KEY(set_id) REFERENCES sets(set_id),
    FOREIGN KEY(word_id) REFERENCES words(word_id)
);
