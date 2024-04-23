from pygame.mixer import Sound
from pygame.sndarray import make_sound
from .oscillator import Oscillator
from numpy import asarray, int16

class Synth:
    def __init__(self, oscillator: Oscillator):
        self._oscillator = oscillator

    def play_note(self, frequency: int, duration: float = 1.5, sampling_rate: int = 44100):
        note = self.create_note(frequency=frequency, duration=duration, sampling_rate=sampling_rate)
        note.set_volume(0.6)
        note.play()

    def create_note(self, frequency: int, duration: float = 1.5, sampling_rate: int = 44100) -> Sound:
        frames = int(duration*sampling_rate)
        wave = self._oscillator.generate_wave(frequency=frequency, duration=duration, frames=frames, fade=False)
        arr = 32767 * asarray(wave) * 0.5
        sound = asarray([arr,arr]).T.astype(int16)
        return make_sound(sound.copy())