from pygame.image import load as load_image
from pygame.font import get_fonts

from .logger import Logger
from .entities.apple_manager import AppleManager
from .game_engine import GameEngine
from .entities.dimension import Dimension
from .entities.apple import AppleConfig
from .entities.catcher import Catcher, CatcherConfig

def main():
    # print(get_fonts())
    logger = Logger(x=10, y=10, font_size=10)
    apple_config = AppleConfig(
        min_width=32,
        max_width=128,
        min_speed=20,
        max_speed=100,
        terminal_velocity=50,
        spawn_chance=0.998,
        good_chance=0.2,
        img_path="./img/apple.png"
    )

    catcher_config = CatcherConfig(
        width=200,
        speed=5,
        img_path="./img/catcher.png"
    )

    screen_size = Dimension(
        x=0,
        y=0,
        w=1920,
        h=1000)
    
    image = load_image(catcher_config.img_path)
    catcher = Catcher(
        image=image,
        dimension=Dimension(
            x = screen_size.w / 2,
            y = screen_size.h - catcher_config.width - 20,
            w = catcher_config.width,
            h = catcher_config.width
        ),
        speed = 10,
        logger=logger
        )
    
    apple_manager = AppleManager(config=apple_config, screen_size=screen_size, logger=logger)

    engine = GameEngine(screen_size=screen_size, catcher=catcher, apple_manager=apple_manager, logger=logger)

    engine.init()
    engine.run()




if __name__ == "__main__":
    main()