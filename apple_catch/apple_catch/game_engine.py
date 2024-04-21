from pygame import init as pygame_init
from pygame import quit as pygame_quit
from pygame import display
from pygame import Surface
from pygame import QUIT
from pygame.time import Clock
from pygame.event import get as get_event
from pygame.image import load as load_image

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

            # flip() the display to put your work on screen
            display.flip()

            dt = self._game_clock.tick(144) / 1000
        
        pygame_quit()