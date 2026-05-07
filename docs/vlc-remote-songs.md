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