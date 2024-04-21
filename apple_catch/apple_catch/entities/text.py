from pygame import Rect, Surface
from pygame.font import SysFont

from .entity import Entity

from .dimension import Dimension

class Text(Entity):
    def __init__(self, text: str, size: float, x: float, y: float, colour: tuple[int,int,int]):
        super().__init__()
        self.size: int = int(size)
        self.colour = colour
        self._text: str = text
        self.image: Surface = self.get_image()
        self.rect: Rect = Rect(x,y,10,10)
        
        
    def update(self):
        self.size-=1
        self.image = self.get_image()

    def get_image(self):
        font = SysFont('couriernew',  self.size)
        return font.render(self._text, False, self.colour)
        