from __future__ import annotations

from pygame import Rect, Surface
from pygame.font import SysFont
from pygame.sprite import Group

from .apple import Apple
from .entity import Entity
from .dimension import Dimension


class FadingTextFactory:
    def __init__(self):
        pass
    
    def get_positive_text(self, points: float, apple: Apple):
        dimensions = Dimension(
            x=apple._dimension.x + apple._dimension.w + 10,
            y=apple._dimension.y - 10,
            w=apple.width,
            h=apple.width
        )
        
        return FadingText(
            text = f"+{points}",
            dimensions=dimensions,
            colour=(185,255,50)
        )
    
    def get_negative_text(self, points: float, apple: Apple):
        dimensions = Dimension(
            x=apple._dimension.x - 10,
            y=apple._dimension.y - 10,
            w=apple.width,
            h=apple.width
        )
        
        return FadingText(
            text = f"{points}",
            dimensions=dimensions,
            colour=(255,105,185)
        )

    def get_text(self, points: int, apple: Apple) -> FadingText:
        if points >= 0:
            return self.get_positive_text(points=points, apple=apple)
        
        return self.get_negative_text(points=points, apple=apple)

class FadingTextGroup(Group):
    def __init__(self):
        super().__init__()

    def remove_smaller_than(self, limit: int = 1):
        self.remove(
            [
                t
                for t in self.sprites()
                if isinstance(t, FadingText) and t.size < limit
            ])
    
    def tick(self, screen: Surface):
        self.update()
        self.draw(surface=screen)
        self.remove_smaller_than()

class FadingText(Entity):
    def __init__(self, text: str, dimensions: Dimension, colour: tuple[int,int,int]):
        super().__init__()
        self._dimensions: Dimension = dimensions
        self.colour = colour
        self._text: str = text
        self.image: Surface = self.get_image()
        self.rect: Rect = Rect(dimensions.x,dimensions.y,10,10)
    
    @property
    def size(self):
        return self._dimensions.w
    
    @size.setter
    def size(self, value):
        self._dimensions.w = value

    def update(self):
        self.size-=1
        self.image = self.get_image()

    def get_image(self):
        font = SysFont('couriernew',  int(self._dimensions.w))
        return font.render(self._text, False, self.colour)
        