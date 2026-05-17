CREATE TABLE remote_images (
    remote_image_id INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    url             TEXT NOT NULL UNIQUE,
    created_at      TEXT,
    updated_at      TEXT,
    deleted_at      TEXT,
    active          INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
