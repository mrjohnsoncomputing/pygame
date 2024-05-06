from dataclasses import dataclass
from random import choice, random
from pygame.time import wait
from .music_theory import Note
from .synth import Synth


@dataclass 
class InstrumentConfig:
    available_notes: list[Note]
    available_durations: list[float]
    walk_duration: float
    walk_note_change_chance: float
    walk_note_jump_chance: float


class Instrument:
    def __init__(self, synth: Synth, instrument_config: InstrumentConfig):
        self._synth = synth
        self._config = instrument_config
        self._current_note_position: int = 0

    def play_random_note(self):
        note = choice(self._config.available_notes)
        duration = choice(self._config.available_durations)
        self._synth.play_note(note.frequency, duration=duration)
        wait(int(duration * 1000))

    def play_random_song(self):
        while True:
            self.play_random_note()

    def walk(self):
        self._walk_change_note()
        self._synth.play_note(self._config.available_notes[self._current_note_position].frequency, self._config.walk_duration)
        wait(int(self._config.walk_duration * 1000))

    def _walk_change_note(self):
        change_note_chance = random()
        if change_note_chance > self._config.walk_note_change_chance:
            if self._current_note_position == 0:
                self._current_note_position += 1
            elif self._current_note_position == len(self._config.available_notes) - 1:
                self._current_note_position -= 1
            else:
                direction = random()
                if direction > 0.5:
                    self._current_note_position += 1
                else:
                    self._current_note_position -= 1
        jump_chance = random()
        if jump_chance > self._config.walk_note_jump_chance:
            self._walk_change_note()

        
