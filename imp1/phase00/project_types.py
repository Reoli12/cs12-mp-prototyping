from dataclasses import dataclass

@dataclass
class Point:
    y: float
    x: float

@dataclass
class Egg:
    height: int
    width: int
    total_hp: int
    current_hp: int
    center_position: Point

    @property
    def rightmost_point(self):
        return self.center_position.x + (self.width // 2)
    @property
    def leftmost_point(self):
        return self.center_position.x - (self.width // 2)
    @property
    def topmost_point(self):
        return  self.center_position.y - (self.height // 2)
    @property
    def bottom_point(self):
        return self.center_position.y + (self.height // 2)
    
