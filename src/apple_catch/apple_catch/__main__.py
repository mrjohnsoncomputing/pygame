from pygame.image import load as load_image

from .entities import Terrain, Dimension, AppleConfig, Catcher, CatcherConfig, AppleManager
from .entities import GroundFactory, DisplayNumberFactory, FadingTextFactory
from .helpers import Logger
from .game_engine import GameEngine


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
    
    ground_tile_size = Dimension(
        x = 0, 
        y = 0,
        w = 64,
        h = 64
    )

    ground_factory = GroundFactory(
        screen_size=screen_size,
        image_paths=[".\img\ground.png", ".\img\ground-2.png", ".\img\ground-3.png"],
        tile_size=ground_tile_size,
        logger=logger
    )

    terrain = Terrain(
        screen_size=screen_size,
        ground_factory=ground_factory,
        logger=logger)
    
    display_number_factory = DisplayNumberFactory(screen_size=screen_size)
    fading_text_factory = FadingTextFactory()
    engine = GameEngine(
        screen_size=screen_size,
        terrain=terrain,
        catcher=catcher,
        apple_manager=apple_manager,
        display_number_factory=display_number_factory,
        fading_text_factory=fading_text_factory,
        logger=logger)

    engine.init()
    engine.run()




if __name__ == "__main__":
    main()