from random import random

from numpy import interp
from pygame import Surface
from pygame.sprite import Group
from pygame.image import load as load_image

from ..helpers import Logger
from .dimension import Dimension
from .apple import Apple, AppleConfig
from .entity import Entity

class AppleManager:
    def __init__(self, config: AppleConfig, screen_size: Dimension, logger: Logger) -> None:
        self._good_apples: Group = Group()
        self._bad_apples: Group = Group()
        self._logger: Logger = logger
        self._config: AppleConfig = config
        self._screen_size: Dimension = screen_size
        self._apple_image: Surface = load_image(config.img_path)
        self._bad_apple_image: Surface = load_image(config.img_path.replace("apple", "bad_apple"))
    
    def new_apple(self, is_good_apple: bool = False) -> Entity:
        x = random() * self._screen_size.w
        y = 0 - ((random() * 100) + self._config.max_width)
        w = (random() * self._config.max_width) + self._config.min_width

        speed = interp(w, [self._config.min_width, self._config.max_width], [self._config.min_speed, self._config.max_speed])

        dimension = Dimension(x=x, y=y, w=w, h=w)
        img = self._apple_image if is_good_apple else self._bad_apple_image
        apple = Apple(dimension=dimension, image=img, is_good=is_good_apple, speed=speed)
        if apple._is_good:
            self._good_apples.add(apple)
        else:
            self._bad_apples.add(apple)
    
    def try_add_apple(self) -> Entity | None:
        spawn_chance = random()
        if spawn_chance > self._config.spawn_chance:
            good_chance = random()
            return self.new_apple(is_good_apple=good_chance > self._config.good_chance)
        return None
    
   

    def update(self, time_delta: float):
        self._bad_apples.update(time_delta, self._config.terminal_velocity)
        self._good_apples.update(time_delta, self._config.terminal_velocity)

        self._good_apples.remove(self._offscreen_apples(apple_group=self._good_apples))
        self._bad_apples.remove(self._offscreen_apples(apple_group=self._bad_apples))


    def _offscreen_apples(self, apple_group: Group) -> list[Apple]:
        return [
            apple
            for apple in apple_group
            if apple.is_off_screen(self._screen_size.h)
        ]


    def display(self, screen: Surface):
        for apple in self._good_apples:
            self._logger.log(
                message=str(apple),
                screen=screen
            )
            screen.blit(apple.image, apple.rect)

        for apple in self._bad_apples:
            self._logger.log(
                message=str(apple),
                screen=screen
            )
            screen.blit(apple.image, apple.rect)