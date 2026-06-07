# Change log Android
## `2026-06-06`
Para el reproducir sonidos del internet, poner el en buildozer:
```
android.permissions = android.permission.INTERNET, (name=android.permission.WRITE_EXTERNAL_STORAGE;maxSdkVersion=18)
```

En el minimizado de la ventana, parar songs. Aun no lo hago, pero facil, solo un stop al `current song` sonando.

El `AndroidMediaPlayerAsync` jala, pero hay que esperarse para darle play. La AI ChatGPT + Copilit + Gemini, crearon la base. Teoricamente jala como debe, pero pos tienes que esperar a que cargue para que recien el play suceda. Bueno pos async moment. Si es vastante descriptivo, pero pos pa mi esto es nuevo.

Entonces Android `SoundPool` para pool de archivos solitarios. Effects. Android `MediaPlayer`, para play de urls, es lo mas sencillo. `SoundPool` es lo mas rapidote que hay en Android base.

Resumen, se crearon con AI (no quiero estar mucho rato haciendo cosas low level y debug en Android, que hueva) de `AndroidMediaPlayerAsync`, `AndroidMediaPlayer`, `AndroidSoundPoolAlone`. Todos listos para usarse en el `ISoundManager`. Al final solo se uso `AndroidMediaPlayer`. Porque carga de una los urls, y jala bien.
