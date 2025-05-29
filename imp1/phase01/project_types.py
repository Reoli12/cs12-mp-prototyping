from dataclasses import dataclass
from abc import ABC
from typing import Protocol


class UpdateHandler(Protocol):
    def update(self):
        ...

class DrawHandler(Protocol):
    def draw(self):
        ...

@dataclass
class GameSettings:
    fps: int
    world_width: int
    world_height: int
    screen_width: int
    screen_height: int

    def __init__(self, fps: int, world_width: int, world_height: int, screen_width: int, screen_height: int):
        self.fps: int = fps
        self.world_width: int = world_width
        self.world_height: int = world_height
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height

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
    speed: int
    

    def __init__(self, height: int, width: int, hp: int, center: Point, speed: int):
        self.height: int = height
        self.width: int = width
        self.total_hp: int = hp
        self.current_hp = hp
        self.center_position: Point = center
        self.speed: int = speed


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
    def __init__(self, height: int, width: int, hp: int, center: Point, speed: int, damage: int, attack_radius: int):
        super().__init__(height, width, hp, center, speed)
        
        self.player_attack_damage = damage
        self.player_attack_radius = attack_radius


class Eggnemy(Egg):
    def __init__(self, height: int, width: int, hp: int, center: Point, speed: int):
        super().__init__(height, width, hp, center, speed)

class Boss(Egg):
    def __init__(self, height: int, width: int, hp: int, center: Point, speed: int):
        super().__init__(height, width, hp, center, speed)