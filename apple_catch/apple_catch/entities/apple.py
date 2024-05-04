from dataclasses import dataclass
from random import randint, random
from typing import Any

from pygame import Surface, Rect
from pygame.transform import scale
from pygame.transform import rotate as rotate_surface

from .dimension import Dimension
from .entity import Entity


@dataclass
class AppleConfig:
    min_width: float
    max_width: float
    min_speed: float
    max_speed: float
    terminal_velocity: float
    spawn_chance: float
    good_chance: float
    img_path: str

class Apple(Entity):
    def __init__(self, image: Surface, dimension: Dimension, speed: float, is_good: bool = True):
        super().__init__()
        self._is_good = is_good
        self._dimension = dimension
        self.rect: Rect = self.get_rekt()
        self.image: Surface = self._scale_image(image=image)
        self.speed: float = speed
        self._fall_time: float = 0
        self.rotation: float = 0
    
    @property
    def width(self) -> float:
        return self._dimension.w

    def get_rekt(self) -> Rect:
        return Rect(self._dimension.x, self._dimension.y, self._dimension.w, self._dimension.h)
    
    def _scale_image(self, image: Surface) -> Surface:
        return scale(image, (self._dimension.w, self._dimension.h))

    def update(self, time_delta: float) -> None:
        self._fall_time += time_delta
        self._dimension = self._dimension.new_y(y= self._dimension.y + (self.speed * self._fall_time * 0.05))
        self.rect = self.get_rekt()
    
    def is_off_screen(self, boundary: float) -> bool:
        return self._dimension.y > boundary

    def __str__(self):
        return f"x:{self._dimension.x}, y:{self._dimension.y}, width:{self._dimension.w}, speed:{self.speed} "