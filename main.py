from core.dt_metronome import DTMetronome
from core.stimulus_generator import StimulusGenerator

metronome = DTMetronome( bpm=90, beats_per_bar=4, bpm_limit=200, beats_limit_per_bar=16 )
stimulus_generator = StimulusGenerator()

# Loop
import time

prev_time = time.perf_counter()
current_stimulus = None

while True:
    # Calcular delta time
    now = time.perf_counter()
    dt = now - prev_time
    prev_time = now

    # Eventos
    signals = metronome.update(dt)

    stimulus = stimulus_generator.update(signals)
    if isinstance(stimulus, str):
        current_stimulus = stimulus

    if signals['first_step_of_beat']:
        info = (
            f'current beat: {signals["current_beat"]}\n'
            f'reset bar: {signals["reset_bar"]}\n'
            f'first_step_of_beat: {signals["first_step_of_beat"]}\n'
            f'step_before_the_bar: {signals["step_before_the_bar"]}\n'
            "\n-------------\n"
        )
        print(info)
        stimulus_info = (
            f"StimulusGenerator\n"
            f"bar count: {stimulus_generator.bar_count}\n"
            f"{current_stimulus}\n"
            "\n-------------\n"
        )
        print(stimulus_info)

