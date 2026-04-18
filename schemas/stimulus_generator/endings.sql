CREATE TABLE endings (
    ending_id   INTEGER PRIMARY KEY,
    ending_text TEXT NOT NULL UNIQUE,
    vocal_id    INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
    FOREIGN KEY(vocal_id) REFERENCES vocals(vocal_id),
    FOREIGN KEY(language_id) REFERENCES languages(vocal_id)
);
