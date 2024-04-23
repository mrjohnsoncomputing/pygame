from random import choice, random
from pygame.time import wait
from .music_theory import Note
from .synth import Synth

class Instrument:
    def __init__(self, synth: Synth, available_notes: list[Note], available_durations: list[float]):
        self._synth = synth
        self._available_notes = available_notes
        self._available_durations = available_durations
        self._current_note_position: int = 0

    def play_random_note(self):
        note = choice(self._available_notes)
        duration = choice(self._available_durations)
        self._synth.play_note(note.frequency, duration=duration)
        wait(int(duration * 1000))

    def play_random_song(self):
        while True:
            self.play_random_note()

    def walk(self, duration: float = 0.5, chance: float = 0.5):
        self._walk_change_note(chance = chance)
        self._synth.play_note(self._available_notes[self._current_note_position].frequency, duration)
        wait(int(duration * 1000))

    def _walk_change_note(self, chance: float = 0.5):
        change_note_chance = random()
        if change_note_chance > chance:
            if self._current_note_position == 0:
                self._current_note_position += 1
            elif self._current_note_position == len(self._available_notes) - 1:
                self._current_note_position -= 1
            else:
                direction = random()
                if direction > 0.5:
                    self._current_note_position += 1
                else:
                    self._current_note_position -= 1
        jump_chance = random()
        if jump_chance > 0.75:
            print("Jumping!")
            self._walk_change_note(0.1)

        
