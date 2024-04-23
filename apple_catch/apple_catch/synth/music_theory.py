from dataclasses import dataclass


@dataclass
class Note:
    octave: int
    note: str
    frequency: float

    @property
    def id(self):
        return f"{self.note}{self.octave}"
    
    def __str__(self):
        return f"{self.note}{self.octave}"

class MusicTheory:
    low_c: float = 32.7
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self) -> None:
        self._note_table = self.get_notes_table()
    
    @property
    def note_list(self):
        return [
            *self.notes,
            *self.notes
        ]

    def get_notes_table(self, octaves: int = 8, start_octave: int = 1):
        notes_table = {}
        current_frequency = self.low_c
        for i in range(start_octave, octaves + 1):
            for note in self.notes:
                note_data = Note(octave=i, note=note, frequency=current_frequency)
                notes_table[note_data.id] = note_data
                current_frequency = self.next_frequency(current_frequency=current_frequency)
        return notes_table

    def next_frequency(self, current_frequency: float) -> float:
        return current_frequency * 2 ** (1/12)
    
    def note_sequence(self, root_note: str):
        notes = []
        sequence_started = False
        print(f"Note list: {self.note_list}")
        for note in self.note_list:
            if note == root_note and sequence_started == False:
                print(f"First note: {note}")
                notes.append(note)
                sequence_started = True
            
            elif sequence_started == True:
                print(f"Appending note: {note}")
                notes.append(note)

                if note == root_note:
                    print(f"Final note: {note}")
                    return notes
        return notes

    def get_key(self, interval_mask: list[int], note_sequence: list[str], start_octave: int, octave_count: int) -> list[Note]:
        notes = []
        for i in range(start_octave, start_octave + octave_count + 1):
            note_counter = 0
            for note in note_sequence:
                if interval_mask[note_counter] == 0:
                    print(f"Not in key: {note}")
                else:
                    note_id = f"{note}{i}"
                    notes.append(self._note_table[note_id])
                    print(f"In key: {note}")
                note_counter += 1
        return notes

    def get_major_key(self, root_note: str, start_octave: int = 4, octave_count: int = 2) -> list[Note]:
        major_interval_mask = [1,0,1,0,1,1,0,1,0,1,0,1,1]
        note_sequence = self.note_sequence(root_note=root_note)
        print(f"Note Sequence: {note_sequence}")
        return self.get_key(interval_mask=major_interval_mask, note_sequence=note_sequence, start_octave=start_octave, octave_count=octave_count)
        


    def get_frequencies(starting_frequency: float, frequency_count: int):
        frequencies = [starting_frequency]
        frequency = starting_frequency
        for i in range(frequency_count):
            frequency = frequency * 2 ** (1/12)
            frequencies.append(frequency)
        return frequencies