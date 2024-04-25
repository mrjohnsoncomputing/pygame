import pygame as pg

from .instrument import Instrument, InstrumentConfig
from .oscillator import TriangleWaveOscillator, SquareWaveOscillator, OrganWaveOscillator
from .synth import Synth
from .music_theory import MusicTheory
from .composition import Composition

def main():
    pg.init()
    pg.mixer.init()

    music_theory = MusicTheory()
    bass_config = InstrumentConfig(
        available_notes=music_theory.get_major_key(
            root_note="C",
            start_octave=2,
            octave_count=1),
        available_durations=[1,2],
        walk_duration=0.5,
        walk_note_change_chance=0.85,
        walk_note_jump_chance=0.95)

    mid_config = InstrumentConfig(
        available_notes=music_theory.get_major_key(
            root_note="C",
            start_octave=3,
            octave_count=1),
        available_durations=[0.125, 0.25],
        walk_duration=0.25,
        walk_note_change_chance=0.7,
        walk_note_jump_chance=0.75)

    high_config = InstrumentConfig(
        available_notes=music_theory.get_major_key(
            root_note="C",
            start_octave=3,
            octave_count=2),
        available_durations=[0.125, 0.25],
        walk_duration=0.25,
        walk_note_change_chance=0.25,
        walk_note_jump_chance=0.50)
    
    square_synth = Synth(oscillator=SquareWaveOscillator())
    organ_synth = Synth(oscillator=OrganWaveOscillator())
    triangle_synth = Synth(oscillator=TriangleWaveOscillator())

    composition = Composition(
        instruments=[
            Instrument(synth=square_synth, instrument_config=bass_config),
            Instrument(synth=organ_synth, instrument_config=mid_config),
            Instrument(synth=organ_synth, instrument_config=mid_config),
            Instrument(synth=triangle_synth, instrument_config=high_config),
            Instrument(synth=square_synth, instrument_config=high_config),
        ])

    composition.compose(length=1000)
    
    pg.mixer.quit()
    pg.quit()

if __name__ == "__main__":
    main()
