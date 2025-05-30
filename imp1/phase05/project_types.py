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

@dataclass
class EgghancementSettings:
    xp_needed: int
    inc_max_hp: int
    inc_atk: int
    inc_spd: int

@dataclass
class EggInfo:
    width: int
    height: int
    max_hp: int
    current_hp: int
    atk: int
    speed: int

@dataclass
class Point:
    x: float
    y: float


class Egg(ABC):
    stats: EggInfo
    center_position: Point
    

    def __init__(self, egginfo: EggInfo, center: Point):
        self.stats: EggInfo = egginfo
        self.center_position: Point = center


    @property
    def rightmost_point(self):
        return self.center_position.x + (self.stats.width // 2)
    @property
    def leftmost_point(self):
        return self.center_position.x - (self.stats.width // 2)
    @property
    def topmost_point(self):
        return  self.center_position.y - (self.stats.height // 2)
    @property
    def bottom_point(self):
        return self.center_position.y + (self.stats.height // 2)
    

class PlayerEgg(Egg):
    def __init__(self, egginfo: EggInfo, center: Point, damage: int, attack_radius: int):
        super().__init__(egginfo, center)
        self.player_attack_radius = attack_radius

class Eggnemy(Egg):
    def __init__(self, egginfo: EggInfo, center: Point):
        super().__init__(egginfo, center)

class Boss(Eggnemy):
    def __init__(self, egginfo: EggInfo, center: Point):
        super().__init__(egginfo, center)