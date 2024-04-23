from dataclasses import dataclass
import random
import pygame as pg
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

from .instrument import Instrument
from .oscillator import TriangleWaveOscillator, SquareWaveOscillator, OrganWaveOscillator
from .synth import Synth
from .music_theory import MusicTheory




def main():
    pg.init()
    pg.mixer.init()

    music_theory = MusicTheory()
    bass_notes = music_theory.get_major_key(
        root_note="C",
        start_octave=2,
        octave_count=1
        )

    mid_notes = music_theory.get_major_key(
        root_note="C",
        start_octave=3,
        octave_count=1
        )
    
    high_notes = music_theory.get_major_key(
        root_note="C",
        start_octave=4,
        octave_count=2
        )
    
    mid_durations = [0.125, 0.25]
    bass_durations = [1,2]
    
    square_synth = Synth(oscillator=SquareWaveOscillator())
    organ_synth = Synth(oscillator=OrganWaveOscillator())
    triangle_synth = Synth(oscillator=TriangleWaveOscillator())

    bass_organ = Instrument(synth=square_synth, available_durations=bass_durations, available_notes=bass_notes)
    mid_organ = Instrument(synth=organ_synth, available_durations=mid_durations, available_notes=mid_notes)
    high_organ = Instrument(synth=triangle_synth, available_durations=mid_durations, available_notes=high_notes)

    #bass_thread = Thread(bass_organ.play_random_song)
    #mid_thread = Thread(mid_organ.play_random_song)
    
    pool = ThreadPoolExecutor(max_workers=3)
    for i in range(100):
        try:
            pool.submit(high_organ.walk, 0.5, 0.1)
        except:
            pass
        
        try:
            pool.submit(mid_organ.walk, 0.25, 0.5)
        except:
            pass
        
        try:
            pool.submit(bass_organ.walk, 0.5, 0.75)
        except:
            pass
        
    pool.shutdown(wait=True)
    
    pg.mixer.quit()
    pg.quit()

if __name__ == "__main__":
    main()


# def dead_code():
#     a_file = open("noteslist.txt")
#     file_contents = a_file.read(); a_file.close()
#     noteslist = file_contents.splitlines()
#     freq = 16.3516 #starting frequency
#     freqs = {}

#     for i in range(len(noteslist)):
#         freqs[noteslist[i]]= freq
#         freq = freq * 2 ** (1/12)

#     with open("SuperMario.txt", "r") as file:
#         notes = [eval(line.rstrip()) for line in file]
#     file.close()

#     track = []
#     for i in range(int(len(notes)/2)):
#         track = track + list(np.zeros(max(0, int(44.1*(notes[i*2][2]-100)))))
#         track = track + synth(freqs[notes[i*2][1]], 1e-3*(notes[i*2+1][2]+100))
    
#     arr = 32767*np.asarray(track)*0.5
#     sound = np.asarray([arr,arr]).T.astype(np.int16)
#     sound = pg.sndarray.make_sound(sound.copy())

#     sound.play()
#     pg.time.wait(int(len(arr)/44.1))

#     import wave

#     sfile = wave.open('mario.wav', 'w')
#     sfile.setframerate(44100)
#     sfile.setnchannels(2)
#     sfile.setsampwidth(2)
#     sfile.writeframesraw(sound)
#     sfile.close()
