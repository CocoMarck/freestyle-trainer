CREATE TABLE remote_songs (
    remote_song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    bpm INTEGER NOT NULL,
    beats_per_bar INTEGER NOT NULL,
    url TEXT NOT NULL,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
