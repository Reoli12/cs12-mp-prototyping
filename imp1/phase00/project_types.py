from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Protocol


class UpdateHandler(Protocol):
    def update(self):
        ...

class DrawHandler(Protocol):
    def draw(self):
        ...

@dataclass
class Point:
    x: float
    y: float


class Egg(ABC):
    height: int
    width: int
    total_hp: int
    current_hp: int
    center_position: Point
    

    def __init__(self, height: int, width: int, hp: int, center: Point):
        self.height: int = height
        self.width: int = width
        self.total_hp: int = hp
        self.current_hp = hp
        self.center_position: Point = center

    @abstractmethod
    def move(self): # generalize how eggs should move, then add args
        ...
        

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
    

class PlayerEgg(Egg):
    def move(self):
        ...