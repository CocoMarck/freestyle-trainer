# VLC Remote songs
Asi se reproducen mp3 del internet, en vlc.
```python
# URL SOUND
import random
import vlc

audio_urls = [
    "https://cdn.pixabay.com/download/audio/2025/06/13/audio_0308f9186a.mp3?filename=onesevenbeatxs-slow-westcoast-boombap-type-beat-359448.mp3",
    "https://cdn.pixabay.com/download/audio/2025/11/07/audio_ab111ab299.mp3?filename=mohamed_hassan-nostalgic-trails-432767.mp3",
    "https://cdn.pixabay.com/download/audio/2025/09/28/audio_ded164a340.mp3?filename=psychronic-pixel-menace-411365.mp3",
    "https://cdn.pixabay.com/download/audio/2025/05/10/audio_14aff3f684.mp3?filename=onesevenbeatxs-funny-boombap-reggae-old-school-rap-beat-prod-by-onesevenbeatxs-339287.mp3"
]
#player =  vlc.MediaPlayer( random.choice(audio_urls) )
player =  vlc.MediaPlayer( audio_urls[3] )
player.audio_set_volume(50)
player.play()
```

---

### Flujo correcto para obtener songs de Pixabay
1. **Descarga controlada**  
   - Usa `requests` o `urllib` para bajar el archivo MP3.  
   - Así evitas bloqueos por `User-Agent` o expiración de URL.  
   - Ejemplo:
     ```python
     import requests

     url = "https://cdn.pixabay.com/download/audio/2025/05/10/audio_14aff3f684.mp3"
     headers = {"User-Agent": "Mozilla/5.0"}
     r = requests.get(url, headers=headers)
     with open("song.mp3", "wb") as f:
         f.write(r.content)
     ```

2. **Almacenamiento temporal**  
   - Guarda en `/tmp` o en tu carpeta `songs/`.  
   - Usa `tempfile.NamedTemporaryFile` si no quieres persistir.  

3. **Reproducción local**  
   - Una vez descargado, tu `RemoteSongController` lo trata como **local song**.  
   - Así evitas que VLC o PyAudio peleen con el servidor.  

4. **Metadatos**  
   - Guarda en tu DB: `name`, `bpm`, `beats_per_bar`, `url_original`, `path_local`.  
   - Así mantienes trazabilidad: sabes de dónde vino y cómo lo usas.  

---

### Ejemplo de integración en tu `RemoteSongController`
```python
import requests, tempfile

class RemoteSongController:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.current_song = None

    def set_random_song(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.write(r.content)
        tmp.close()
        self.current_song = {
            "path": tmp.name,
            "url": url
        }

    def play_song(self):
        if self.current_song:
            sound = self.sound_manager.get_sound(self.current_song["path"])
            return self.sound_manager.play_sound(sound)
```

👉 Aquí ya no dependes de que VLC abra el stream remoto. Descargas con headers válidos, guardas temporalmente y reproduces como si fuera local.

---

### ⚖️ Ventajas de este enfoque
- **Evitas 403**: el servidor cree que eres navegador legítimo.  
- **Consistencia**: tu app siempre reproduce archivos locales, sin importar si vienen de remoto.  
- **Escalabilidad**: puedes cachear canciones y no volver a pedirlas.  
- **Trazabilidad**: DB guarda tanto el `url` original como el `path` local.  
