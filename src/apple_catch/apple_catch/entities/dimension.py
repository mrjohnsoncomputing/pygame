from dataclasses import dataclass, replace


@dataclass
class Dimension:
    x: float
    y: float
    w: float
    h: float

    def new_position(self, x: float, y: float):
        return replace(self, x=x, y=y)

    def new_y(self, y:float):
        return replace(self, y=y)

    def new_x(self, x:float):
        return replace(self, x=x)