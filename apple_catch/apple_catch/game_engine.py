from pygame import init as pygame_init
from pygame import quit as pygame_quit
from pygame import display
from pygame import Surface
from pygame import QUIT
from pygame.time import Clock
from pygame.event import get as get_event
from pygame.image import load as load_image
from pygame.sprite import spritecollideany, Group

from .entities.text import Text
from .helpers.math import Math

from .logger import Logger
from .entities.catcher import Catcher
from .entities.dimension import Dimension
from .entities.apple_manager import AppleManager

class GameEngine:
    def __init__(self, screen_size: Dimension, catcher: Catcher, apple_manager: AppleManager, logger: Logger):
        self._screen: Surface | None = None
        self._game_clock: Clock | None = None
        self._game_is_running: bool = False
        self._catcher: Catcher = catcher
        self._apple_manager: AppleManager = apple_manager
        self._screen_size: Dimension = screen_size
        self._logger: Logger = logger
        self._image: Surface = load_image("./img/background.png")
        self._score: int = 0
        self._text: Group = Group()
    
    def init(self):
        pygame_init()
        self._screen = display.set_mode((self._screen_size.w, self._screen_size.h))
        self._game_clock = Clock()
        self._game_is_running = True
        
    
    def run(self):
        dt = 0
        while self._game_is_running:
            self._screen.blit(self._image, (self._screen_size.w - 3000, self._screen_size.h - 3000))
            self._logger.reset()
            self._logger.log(f"Score: {self._score}", self._screen)
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in get_event():
                if event.type == QUIT:
                    self._game_is_running = False

            self._apple_manager.try_add_apple()
            self._apple_manager.update(dt)
            self._apple_manager.display(self._screen)

            self._catcher.update(self._screen_size.w)
            self._catcher.display(self._screen)

            if (good_apple := spritecollideany(self._catcher, self._apple_manager._good_apples)) is not None:
                self._apple_manager._good_apples.remove(good_apple)
                points = Math.roundto(good_apple.width/10, 5)
                self._score += points
                self._text.add(
                    Text(
                        text = f"+{points}",
                        size = good_apple.width,
                        x=good_apple._dimension.x + good_apple._dimension.w + 10,
                        y=good_apple._dimension.y - 10,
                        colour=(185,255,50)
                    )
                )

            if (bad_apple := spritecollideany(self._catcher, self._apple_manager._bad_apples)) is not None:
                self._apple_manager._bad_apples.remove(bad_apple)
                points = Math.roundto(bad_apple.width/10, 5)
                self._score -= points
                self._text.add(
                    Text(
                        text = f"-{points}",
                        size = bad_apple.width,
                        x=bad_apple._dimension.x - 10,
                        y=bad_apple._dimension.y - 10,
                        colour=(255,105,185)
                    )
                )

            self._text.update()
            self._text.draw(self._screen)

            self._text.remove(
                [
                    t
                    for t in self._text
                    if t.size < 1
                ]
            )

            # flip() the display to put your work on screen
            display.flip()

            dt = self._game_clock.tick(144) / 1000
        
        pygame_quit()