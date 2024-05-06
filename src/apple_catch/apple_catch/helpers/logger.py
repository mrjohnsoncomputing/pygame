from pygame import Surface
from pygame.font import SysFont

class Logger:
    def __init__(self, x: float, y: float, font_size: float):
        self._initial_y = y
        self.y = y
        self.x = x
        self._font_size = font_size

    def reset(self):
        self.y = self._initial_y
    
    def log(self, message: str, screen: Surface):
        font = SysFont('timesnewroman',  self._font_size)
        rendered_font = font.render(message, False, (255,255,255), (0,0,0))
        screen.blit(rendered_font, (self.x, self.y))
        self.y += self._font_size

