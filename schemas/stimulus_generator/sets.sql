CREATE TABLE sets (
    set_id      INTEGER PRIMARY KEY,
    set_name    TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
