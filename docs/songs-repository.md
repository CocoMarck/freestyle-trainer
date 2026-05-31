# Song Repository
Guardamos en la tabla songs, la canción. Se indicara si es local, o no. Si no lo es se asume que es remota.

Se establece su velocidad en BPM. No almacena nada relacionado con `StimulusGenerator`. O otra cosa, es independiente. Si se mete en DB, tendra campos de control.

### Local song
```json
{
  "name": "Mi Track",
  "bpm": 90,
  "beats_per_bar": 4,
  "path": "data/music/mi_track.mp3"
}
```

### Remote song
```json
{
  "name": "Mi Track",
  "bpm": 90,
  "beats_per_bar": 4,
  "url": "data/music/mi_track.mp3"
}
```

### Remote or local song
```json
{
  "name": "Mi Track",
  "bpm": 90,
  "beats_per_bar": 4,
  "path": null,
  "url": null
}
```
> Se hay path es local, si no hay se asume que es remote. Si path y url, tienen datos, se asume que es local. Pioridad a ser local.

---

## Tablas
Una para canciones locales, y otra para canciones remotas.
```sql
CREATE TABLE local_songs (
    local_song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    bpm INTEGER NOT NULL,
    beats_per_bar INTEGER NOT NULL,
    path TEXT NOT NULL,
    created_at  TEXT,
    updated_at  TEXT,
    deleted_at  TEXT,
    active      INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1))
);
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
```
