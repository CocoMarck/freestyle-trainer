# Tabla de Tematicas `sets_table`
`set_id, set_name, description, campos de control`.

### schema:
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

A sets le vale queso que palabras y en que idioma los elijas.

## Tabla palabras de tematicas `set_words`
Se almacenaran así: `set_id, word_id, sin campos de control`.

## Tabla imagenes de tematicas `set_local_songs` `set_remote_songs`
- Se almacenaran así: `set_id, local_song_id, sin campos de control`
- Se almacenaran así: `set_id, remote_song_id, sin campos de control`

## Tabla imagenes de tematicas `set_local_images` `set_remote_images`
- Se almacenaran así: `set_id, local_image_id, sin campos de control`
- Se almacenaran así: `set_id, remote_image_id, sin campos de control`

## Como funcionara
Así solo se obtienen palabras con tematica custom. Sea por ejemplo: hogar, calle, crimen, etc.
