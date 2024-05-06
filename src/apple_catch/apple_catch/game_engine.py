from pygame import init as pygame_init
from pygame import quit as pygame_quit
from pygame import display
from pygame import Surface
from pygame import QUIT
from pygame.time import Clock
from pygame.event import get as get_event
from pygame.image import load as load_image

from .entities import Terrain, Catcher, Dimension, AppleManager, Apple
from .entities import DisplayNumberFactory, DisplayNumberGroup, FadingTextGroup, FadingTextFactory
from .helpers import Math, Logger

class GameEngine:
    def __init__(
            self, 
            screen_size: Dimension, 
            catcher: Catcher, 
            apple_manager: AppleManager, 
            terrain: Terrain,
            display_number_factory: DisplayNumberFactory,
            fading_text_factory: FadingTextFactory,
            logger: Logger):
        self._display_text_factory = display_number_factory
        self._fading_text_factory = fading_text_factory
        self._screen: Surface | None = None
        self._game_clock: Clock | None = None
        self._game_is_running: bool = False
        self._catcher: Catcher = catcher
        self._apple_manager: AppleManager = apple_manager
        self._screen_size: Dimension = screen_size
        self._logger: Logger = logger
        self._image: Surface = load_image("./img/background.png")
        self._current_score: int = 0
        self._fading_text_group: FadingTextGroup = FadingTextGroup()
        self._display_text_group: DisplayNumberGroup = DisplayNumberGroup()
        self._terrain: Terrain = terrain
    
    @property
    def current_score(self):
        return self._current_score
    
    @current_score.setter
    def current_score(self, value: int):
        self._current_score = value
        if (item := self._display_text_group.get_item_from_label("Current Score")) is not None:
            item.update_value(self._current_score)

    def init(self):
        pygame_init()
        self._screen = display.set_mode((self._screen_size.w, self._screen_size.h))
        self._game_clock = Clock()
        self._game_is_running = True
        self.create_display_text()

    def create_display_text(self):
        current_score = self._display_text_factory.get_current_score()
        self._display_text_group.add(current_score)
    
    def check_events(self):
        for event in get_event():
            if event.type == QUIT:
                self._game_is_running = False

    def calculate_points(self, apple: Apple):
        points = Math.roundto(apple.width/10, 5)
        if not apple._is_good:
            return -points
        return points
    
    def get_ticks(self, frame_rate: int = 144) -> float:
        return self._game_clock.tick(frame_rate) / 1000
    
    def check_for_collisions(self):
        while True:
            if (apple := self._apple_manager._good_apples.get_colliding_apple(self._catcher)) is None:
                if (apple := self._apple_manager._bad_apples.get_colliding_apple(self._catcher)) is None:
                    break
        
            points = self.calculate_points(apple=apple)
            self.current_score += points
            self._fading_text_group.add(
                self._fading_text_factory.get_text(points=points, apple=apple))

    def run(self):
        ticks = 0
        while self._game_is_running:
            self._terrain.draw(self._screen)
            self._logger.reset()
            self._logger.log(f"Score: {self._current_score}", self._screen)
            
            self.check_events()
            self._apple_manager.tick(ticks=ticks, screen=self._screen)
            self._catcher.tick(screen=self._screen, screen_size=self._screen_size)
            self.check_for_collisions()
            self._fading_text_group.tick(self._screen)
            self._display_text_group.tick(self._screen)

            # flip() the display to put your work on screen
            display.flip()

            ticks = self.get_ticks(144)
        
        pygame_quit()