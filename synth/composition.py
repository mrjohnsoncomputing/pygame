from concurrent.futures import ThreadPoolExecutor

from .instrument import Instrument

class Composition:
    def __init__(self, instruments: list[Instrument]):
        self._instruments = instruments

    def compose(self, length: int):
        pool = ThreadPoolExecutor(max_workers=len(self._instruments))
        for i in range(length):
            for instrument in self._instruments:
                try:
                    pool.submit(instrument.walk)
                except:
                    print("Error!")
            
        pool.shutdown(wait=True)