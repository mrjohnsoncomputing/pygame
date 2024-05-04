from __future__ import annotations

from pygame import Surface, Rect
from pygame.font import SysFont
from pygame.sprite import Group

from .dimension import Dimension
from .entity import Entity


class DisplayNumberGroup(Group):

    def get_item_from_label(self, label: str) -> DisplayNumber | None:
        matches = [
            x
            for x in self.sprites()
            if isinstance(x, DisplayNumber) and x.label.startswith(label)
        ]
        return None if len(matches) == 0 else matches[0]

class DisplayNumberFactory:
    def __init__(self, screen_size: Dimension):
        self._screen_size = screen_size

    def get_current_score(self) -> DisplayNumber:
        position = Dimension(
            x = 10,
            y = 10,
            w = 50,
            h = 30
        )
        return DisplayNumber(
            position=position,
            label = "Current Score",
            value=0,
            colour=(100, 200, 50)
        )

class DisplayNumber(Entity):
    def __init__(self, position: Dimension, label: str, value: int, colour: tuple[int,int,int]):
        super().__init__()
        self._position = position
        self.label = label
        self.value = value
        self.text = f"{label}: {value}"
        self._colour = colour
        self.image: Surface = self.get_image()
        self.rect: Rect = Rect(position.x,position.y,position.w,position.h)
    
    def get_image(self) -> Surface:
        font = SysFont('couriernew',  self._position.w)
        return font.render(self.text, False, self._colour)

    def update_value(self, value: int):
        self.value = value
        self.text = f"{self.label}: {value}"
        self.image = self.get_image()