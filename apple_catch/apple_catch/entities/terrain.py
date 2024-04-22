from pygame import Surface
from pygame.sprite import Group
from pygame.image import load as load_image

from ..helpers import Logger
from .dimension import Dimension
from .ground import Ground

class Terrain:
    def __init__(self, screen_size: Dimension, ground_size: int, logger: Logger) -> None:
        self._ground: Group = Group()
        self._screen_size = screen_size
        self._ground_image = load_image("./img/ground.png")
        self._sky_image = load_image("./img/background.png")
        self._ground_tile_size = ground_size
        self._logger = logger

        self.create_ground()

    
    def create_ground(self):
        tiles = round(self._screen_size.w / self._ground_tile_size) + 1
        for i in range(tiles):
            self._ground.add(
                Ground(
                    image=self._ground_image,
                    dimension=Dimension(
                        x=i * self._ground_tile_size,
                        y=self._screen_size.h - self._ground_tile_size,
                        w=self._ground_tile_size,
                        h=self._ground_tile_size
                    ),
                    logger = self._logger
                )
            )
        self._ground.update()
    
    def draw(self, screen: Surface):
        screen.blit(self._sky_image, (0,0))
        self._ground.draw(screen)