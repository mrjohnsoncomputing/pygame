from abc import ABC, abstractmethod
import numpy as np

class Oscillator(ABC):
    
    def generate_wave(self, frequency: int, duration: float, frames: int, fade: bool = True) -> list[float]:
        wave = self._generate_wave(frequency=frequency, duration=duration, frames=frames)    
        if fade:
            return self.fade_wave(wave=wave, frames=frames)
        return wave
    
    @abstractmethod
    def _generate_wave(self, frequency: int, duration: float, frames: int) -> list[float]:
        raise NotImplementedError

    def fade_wave(self, wave: list[float], frames: int) -> list[float]:
        fade = list(np.ones(frames-4410))+list(np.linspace(1, 0, 4410))
        new_wave = np.multiply(wave, np.asarray(fade))
        return list(new_wave)


class SinWaveOscillator(Oscillator):
    def _generate_wave(self, frequency: int, duration: float, frames: int) -> list[float]:
        return np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))


class SquareWaveOscillator(Oscillator):
    def _generate_wave(self, frequency: int, duration: float, frames: int) -> list[float]:
        wave = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
        return np.clip(wave*10, -1, 1) # squarish waves


class TriangleWaveOscillator(Oscillator):
    def _generate_wave(self, frequency: int, duration: float, frames: int) -> list[float]:
        wave = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
        wave = np.cumsum(np.clip(wave*10, -1, 1)) # triangularish waves pt1
        wave = wave+np.sin(2*np.pi*frequency*np.linspace(0,duration, frames)) # triangularish waves pt1
        return wave/max(np.abs(wave)) # adjust to -1, 1 range


class OrganWaveOscillator(Oscillator):
    def _generate_wave(self, frequency: int, duration: float, frames: int) -> list[float]:
        wave = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
        wave = wave + np.cos(4*np.pi*frequency*np.linspace(0,duration, frames)) # organ like
        wave = wave + np.cos(6*np.pi*frequency*np.linspace(0,duration, frames)) # organ like
        return wave/max(np.abs(wave)) # adjust to -1, 1 range