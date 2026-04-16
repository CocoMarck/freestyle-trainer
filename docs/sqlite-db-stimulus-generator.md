# SQLite3 DB Stimulus Generator

Base de datos de stimulos para ideas improvisadas.

Campos de control: `created_at`, `updated_at`, `deleted_at`, `active`.

## Tablas base de todo
```sql
CREATE TABLE endings (
    ending_id   INTEGER PRIMARY KEY,
    ending_text TEXT NOT NULL UNIQUE,
    vocal       TEXT NOT NULL,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
```
Tabla de terminaciónes de palabras.

```sql
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
```
Tabla de palabras, con terminación indicada.


## Tabla para sets personalizados
```sql
CREATE TABLE sets (
    set_id      INTEGER PRIMARY KEY,
    set_name    TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
```
Tabla de sets, preconfigurados. Palabras eleguidas por el user.

```sql
CREATE TABLE set_words (
    set_id          INTEGER NOT NULL,
    word_id         INTEGER NOT NULL,
    PRIMARY KEY (set_id, word_id),
    FOREIGN KEY(set_id) REFERENCES sets(set_id),
    FOREIGN KEY(word_id) REFERENCES words(word_id)
);
```
Tabla indicativa de palabras almacenadas en cada set. Sin campos de control, para mantener simplicidad. Responsabilizar tabla `sets` de la complejidad.
