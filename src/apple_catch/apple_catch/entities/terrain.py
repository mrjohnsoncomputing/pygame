from random import choice
from typing import Generator

from pygame import Surface
from pygame.sprite import Group
from pygame.image import load as load_image

from ..helpers import Logger
from .dimension import Dimension
from .ground import Ground


class GroundFactory:
    _images: list[Surface]

    def __init__(
            self, 
            screen_size: Dimension, 
            image_paths: list[str], 
            tile_size: Dimension, 
            logger: Logger, 
            levels: int = 1):
        self._tile_size: Dimension = tile_size
        self._screen_size = screen_size
        self._image_paths = image_paths
        self._logger = logger
        self._levels = levels
        self.load_images()

    def load_images(self):
        self._images = [
            load_image(x)
            for x in self._image_paths
        ]
    
    def random_surface_tiles(self) -> Generator[Ground, None, None]:
        tiles = round(self._screen_size.w / self._tile_size.w) + 1
        y_position = self._screen_size.h - (self._tile_size.h * self._levels)
        for i in range(tiles):
            yield Ground(
                image=choice(self._images),
                dimension=Dimension(
                    x=i * self._tile_size.w,
                    y=y_position,
                    w=self._tile_size.w,
                    h=self._tile_size.h
                ),
                logger = self._logger
            )

class Terrain:
    def __init__(self, screen_size: Dimension, ground_factory: GroundFactory, logger: Logger) -> None:
        self._ground: Group = Group()
        self._screen_size = screen_size
        self._sky_image = load_image("./img/background.png")
        self._logger = logger
        self._ground_factory = ground_factory

        self.create_ground()

    
    def create_ground(self):
        for ground in self._ground_factory.random_surface_tiles():
            self._ground.add(ground)
        self._ground.update()
    
    def draw(self, screen: Surface):
        screen.blit(self._sky_image, (0,0))
        self._ground.draw(screen)