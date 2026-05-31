# Image table
Tabla de imagenes. De preferencia que el nombre de las imagenes sea en ingles. Aunque en realidad no importa mucho para el funcionamiento, pero si para la consistencia del code.

Seran locales y remotas, las locales tienen path, y las remotas tienen url a image.

### schema
```sql
CREATE TABLE local_images (
    local_image_id  INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    path            TEXT NOT NULL UNIQUE,
    created_at      TEXT,
    updated_at      TEXT,
    deleted_at      TEXT,
    active          INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
CREATE TABLE remote_images (
    remote_image_id INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    url             TEXT NOT NULL UNIQUE,
    created_at      TEXT,
    updated_at      TEXT,
    deleted_at      TEXT,
    active          INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
```
