from .logger import Logger
from .entities.apple_manager import AppleManager
from .game_engine import GameEngine
from .entities.dimension import Dimension
from .entities.apple import Apple, AppleConfig
from .entities.catcher import Catcher

def main():
    apple_config = AppleConfig(
        min_width=16,
        max_width=64,
        min_speed=20,
        max_speed=100,
        terminal_velocity=50,
        spawn_chance=0.9,
        good_chance=0.2,
        img_path="./img/apple.png"
    )

    screen_size = Dimension(
        x=0,
        y=0,
        w=1500,
        h=900)
    
    logger = Logger(x=10, y=10, font_size=10)

    apple_manager = AppleManager(config=apple_config, screen_size=screen_size, logger=logger)

    engine = GameEngine(screen_size=screen_size, apple_manager=apple_manager, logger=logger)

    engine.init()

    engine.run()




if __name__ == "__main__":
    main()