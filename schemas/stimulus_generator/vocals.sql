CREATE TABLE vocals (
    vocal_id    INTEGER PRIMARY KEY,
    vocal_text  TEXT NOT NULL UNIQUE,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
