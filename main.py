from core.dt_metronome import DTMetronome

metronome = DTMetronome( bpm=120, beats_per_bar=4, bpm_limit=200, beats_limit_per_bar=16 )

# Loop
import time

prev_time = time.perf_counter()

while True:
    # Calculate delta time
    now = time.perf_counter()
    dt = now - prev_time
    prev_time = now

    # Use dt for framerate-independent logic
    # Example: Move 100 pixels per second
    # position += speed * dt

    signals = metronome.update(dt)
    if signals['change_beat']:
        text = (
            f'current beat: {signals["current_beat"]}\n'
            f'reset bar: {signals["reset_bar"]}\n'
            f'first_step_of_beat: {signals["first_step_of_beat"]}\n'
            f'step_before_the_bar: {signals["step_before_the_bar"]}\n'
            "\n-------------\n"
        )
        print(text)

