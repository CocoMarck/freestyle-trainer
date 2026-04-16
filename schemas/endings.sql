CREATE TABLE endings (
    ending_id   INTEGER PRIMARY KEY,
    ending_text TEXT NOT NULL UNIQUE,
    vocal       TEXT NOT NULL,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
