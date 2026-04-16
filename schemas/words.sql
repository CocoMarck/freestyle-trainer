CREATE TABLE words (
    word_id     INTEGER PRIMARY KEY,
    word_text   TEXT NOT NULL UNIQUE,
    ending_id   INTEGER NOT NULL,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
    FOREIGN KEY(ending_id) REFERENCES endings(ending_id)
);
