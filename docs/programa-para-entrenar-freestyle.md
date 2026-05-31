# Entrenar freestyle 
Entrena el Improvisar. Simplemente reproduce beet, y muestra palabras, cada "x" cantida de compases.

Básicamente es un metronomo, con prefix dependiendo el beet. Prefijo visual/sonoro que acompaña al beat o a un marcador de compás. El beet puede ser local, pero preferiblemente sera un audio de YT, o por streaming, lo que sea mejor. Así la app solo se enfoca en entrar en tempo. 

Dependiendo el beat, sea local o por streaming, se configura el metronomo.

Se mostraran palabras random. Configurables por la persona, o solo palabras locas, las default. Las palabras default seran 4 por cada cambio, y todas rimaran entre si, de forma fonetica claro.

Cada "x" cantidad de compases, se mostraran palabras.

Ya tengo el metronomo funcional. Funciona por FPS fijos, vere si es mejor hacerlo a tiempo real o no, ya que lo pienso hacer para Android, aunque primeramente lo hare para PC por motivos de facilidad y testeo.

Por defecto se pondran beats ya configurados, sacados de internet. Su configuración sera guardada en un JSON, o en un SQLite DB. 

El usuario podra añadir o borrar config de beats. 

Tambien podra configurar que palabras mostrar, etc.

Tambien habra un modo solo beat, o solo metronomo. En realidad esto seria solo desabilitar cosas, pero supongo que puede servir.

Las palabras; rimas fonéticas. Podrian estar en un JSON.

Ejemplo:
```json
{
  "sets": [
    {
      "ending": "ar",
      "words": ["cantar", "soñar", "volar", "jugar"]
    },
    {
      "ending": "ón",
      "words": ["canción", "pasión", "razón", "visión"]
    }
  ],
  "images": [
    {
      "id": 1,
      "path": "assets/img/gato.png",
      "category": "animal"
    },
    {
      "id": 2,
      "path": "https://miweb.com/img/microfono.png",
      "category": "music"
    }
  ],
  "emojis": [
    {
      "id": 1,
      "emoji": "🎤",
      "category": "music"
    },
    {
      "id": 2,
      "emoji": "🔥",
      "category": "energy"
    }
  ]
}
```

## Features
En vez de mostrar palabras, mostrar; figuras, emojis, dibujos. Uno o varios.

Grabar microfono. Y si esta usando audifonos, se conbinara el beat y la voz si es que se acepta así. Si se hace así, entonces se podra editar el volumen tanto de la pista de la voz como la del beat.

Opcional, si es video; mostrarlo o no.

### Tema anuncios

- YouTube exige que los anuncios se reproduzcan. No puedes saltártelos ni bloquearlos.

- Lo que sí puedes hacer es detectar cuándo termina el anuncio y recién ahí arrancar tu metronomo. Eso es totalmente válido y respeta las reglas.

- En práctica: tu app espera a que el “player state” cambie a playing en el API, y entonces sincronizas el metronomo.


---
## Arquitectura de módulos sugerida
- Beat Manager: Guarda y carga beats desde JSON o SQLite
- Metronome Engine: Envia señales.

- Stimulus Generator: Palabras, emojis, figuras, dibujos. Configurable por el usuario (listas personalizadas).
    - Las imagenes podran ser direcciones HTML.
    - JSON/Table de palabras foneticas entre si, otro JSON/Table de rutas de imagenes HTML o locales, o separao. y un JSON/Table final de Emojis.
    - Se guardan como caracteres Unicode.

- Recorder: Graba microfono
- Mixer: Si hay audifonos, mezcla voz y beat. Guarda audio, en donde diga el user, o en ruta por defecto.

- UI Layer: probablemente hecha en PyKivy, y PyQt6 para pc. Interfaz grande.

## Tips técnicos
Para Android, usa AudioTrack o OpenSL ES si necesitas baja latencia.

SQLite te da persistencia limpia para beats y configuraciones. JSON puede servir como export/import.

Para las rimas fonéticas, puedes empezar con un diccionario simple de terminaciones (ej. “-ar”, “-ón”, “-ente”) y luego expandir.

### Como hacer el metronomo en tiempo real
```python
from kivy.clock import Clock

bpm = 90
beat_interval = 60.0 / bpm  # segundos por beat

def tick(dt):
    print("Beat!")  # aquí disparas palabra/emoji/etc

Clock.schedule_interval(tick, beat_interval)
```

### Audio de baja latencia
Ok en pc, hago un `PySoundManager`, que hara que el bajo nivel, sea mas alto nivel. Y despues un `AudioTrackManager`, con el mismo concepto. Ambos seran hijos de la entidad de `SoundManager`, para mentener lógica, y no tener que cambiar tanto code.