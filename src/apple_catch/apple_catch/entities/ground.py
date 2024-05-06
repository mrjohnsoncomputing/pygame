from logging import Logger
from pygame import Rect, Surface
from pygame.transform import scale

from .dimension import Dimension
from .entity import Entity

class Ground(Entity):
    def __init__(self, image: Surface, dimension: Dimension, logger: Logger):
        super().__init__()
        self._dimension = dimension
        self.rect: Rect = self.get_rekt()
        self.image: Surface = self._scale_image(image)
        self._logger = logger

    def get_rekt(self) -> Rect:
        return Rect(self._dimension.x, self._dimension.y, self._dimension.w, self._dimension.h)
    
    def _scale_image(self, image: Surface) -> Surface:
        return scale(image, (self._dimension.w, self._dimension.h))