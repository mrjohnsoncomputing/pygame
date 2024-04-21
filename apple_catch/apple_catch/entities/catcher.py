from dataclasses import dataclass
from random import randint, random
from typing import Any

from pygame import Surface, Rect
from pygame.transform import scale
from pygame.key import get_pressed
from pygame import K_LEFT, K_RIGHT, K_a, K_d

from ..logger import Logger

from .dimension import Dimension
from .entity import Entity


@dataclass
class CatcherConfig:
    width: float
    speed: float
    img_path: str

class Catcher(Entity):
    def __init__(self, image: Surface, dimension: Dimension, speed: float, logger: Logger):
        super().__init__()
        self._dimension = dimension
        self.rect: Rect = self.get_rekt()
        self.image: Surface = self._scale_image(image=image)
        self.speed: float = speed
        self._logger = logger
    
    def get_rekt(self) -> Rect:
        return Rect(self._dimension.x, self._dimension.y, self._dimension.w, self._dimension.h)
    
    def _scale_image(self, image: Surface) -> Surface:
        return scale(image, (self._dimension.w, self._dimension.h))

    def update(self, screen_width: float) -> None:
        keys = get_pressed()
        x = -1

        if keys[K_LEFT] or keys[K_a]:
            x = self._dimension.x - self.speed
        if keys[K_RIGHT] or keys[K_d]:
            x = self._dimension.x + self.speed
        
        if x < 0 or x > screen_width - self._dimension.w:
            return
        
        self._dimension = self._dimension.new_x(x=x)
        self.rect = self.get_rekt()
    
    def display(self, screen: Surface):
        self._logger.log(
            message=str(self),
            screen=screen
        )
        screen.blit(self.image, self.rect)

    def __str__(self):
        return f"CATCHER || x:{self._dimension.x}, y:{self._dimension.y}, width:{self._dimension.w}, speed:{self.speed} "