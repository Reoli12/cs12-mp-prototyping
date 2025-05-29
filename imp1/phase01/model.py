from __future__ import annotations
from project_types import Eggnemy, PlayerEgg, Point, GameSettings
import random


class Model:
    def __init__(self, player_egg: PlayerEgg, settings: GameSettings, eggnemy_count: int, eggnemy_width: int, eggnemy_height: int, eggnemy_speed: int, eggnemy_initial_hp: int):
        self._screen_width = settings.screen_width
        self._screen_height = settings.screen_height
        self._world_width = settings.world_width
        self._world_height = settings.world_height
        self._fps = settings.fps
        self._frame_count = 0

        self._player_egg = player_egg

        self._eggnemies: list[Eggnemy] = []
        self._overlapping_player_eggnemy: list[Eggnemy] = []
        self._num_defeated_eggnemies = 0
        self._eggnemy_count = eggnemy_count
        self._eggnemy_width = eggnemy_width
        self._eggnemy_height = eggnemy_height
        self._eggnemy_speed = eggnemy_speed
        self._eggnemy_max_hp = eggnemy_initial_hp

        self._is_game_over = False

    def update(self, is_forward_pressed: bool, is_left_pressed: bool, is_down_pressed: bool, is_right_pressed: bool, is_attack_pressed: bool):
        player_egg = self._player_egg

        #game over state
        if player_egg.current_hp <= 0:
            self._is_game_over = True

        if self._is_game_over:
            return
        
        #player movement, position and attack
        self.player_movement(is_forward_pressed, is_down_pressed, is_left_pressed, is_right_pressed)

        self.player_attack(is_attack_pressed)
            
        if self.is_out_of_bounds():
            self.return_to_bounds()

        #eggnemies
        self.eggnemy_movement()
        self.eggnemy_spawn()

        #damage
        if self._frame_count % self._fps == 0 and len(self._overlapping_player_eggnemy) > 0:
            self._player_egg.current_hp -= 1 

        self._frame_count += 1
        print(player_egg.center_position, player_egg.topmost_point, self._fps)


    def is_overlapping_player(self, eggnemy: Eggnemy):
        left_bounds = self._player_egg.leftmost_point
        right_bounds = self._player_egg.rightmost_point
        top_bounds = self._player_egg.topmost_point
        bottom_bounds = self._player_egg.bottom_point

        eggnemy_right = eggnemy.rightmost_point
        eggnemy_left = eggnemy.leftmost_point
        eggnemy_bottom = eggnemy.bottom_point
        eggnemy_top = eggnemy.topmost_point

        return not (left_bounds > eggnemy_right or 
                right_bounds < eggnemy_left or
                top_bounds > eggnemy_bottom or
                bottom_bounds < eggnemy_top)

    def is_out_of_bounds(self) -> bool:
        return (   
            self._player_egg.leftmost_point < 0 
            or self._player_egg.rightmost_point > self._world_width
            or self._player_egg.topmost_point < 0
            or self._player_egg.bottom_point > self._world_height 
        )

    def return_to_bounds(self):
        player_egg = self._player_egg
        assert self.is_out_of_bounds()
        
        if player_egg.leftmost_point < 0:
            player_egg.center_position.x = player_egg.width / 2

        if player_egg.rightmost_point > self._world_width:
            player_egg.center_position.x = self._world_width - (player_egg.width / 2)

        if player_egg.bottom_point > self._world_height:
            player_egg.center_position.y = self._world_height - (player_egg.height / 2)

        if player_egg.topmost_point < 0:
            player_egg.center_position.y = player_egg.height / 2
    
    def player_movement(self, forward_btn: bool, down_btn: bool, left_btn: bool, right_btn: bool):
        if forward_btn:
            self._player_egg.center_position.y -= self._player_egg.speed
        if left_btn:
            self._player_egg.center_position.x -= self._player_egg.speed
        if down_btn:
            self._player_egg.center_position.y += self._player_egg.speed
        if right_btn:
            self._player_egg.center_position.x += self._player_egg.speed

    def player_attack(self, is_attack_pressed: bool):
        if is_attack_pressed:
            radius = self._player_egg.player_attack_radius
            damage = self._player_egg.player_attack_damage
            for eggnemy in self._eggnemies:
                eggnemy_center = eggnemy.center_position
                
                #defeats eggnemy
                distance_to_player = ((self._player_egg.center_position.x - eggnemy_center.x) ** 2 + (self._player_egg.center_position.y - eggnemy_center.y) ** 2) ** 0.5
                if distance_to_player <= radius:
                    eggnemy.current_hp -= damage

                    if eggnemy.current_hp <= 0:
                        self._eggnemies.remove(eggnemy)
                        self._num_defeated_eggnemies += 1
                        if eggnemy in self._overlapping_player_eggnemy:
                            self._overlapping_player_eggnemy.remove(eggnemy)

    def eggnemy_movement(self):
        for eggnemy in self._eggnemies:
            self.eggnemy_overlap_check(eggnemy)
            
            x_distance_to_player = self._player_egg.center_position.x - eggnemy.center_position.x
            y_distance_to_player = self._player_egg.center_position.y - eggnemy.center_position.y
            
            #follows player
            if not self._is_game_over:
                if x_distance_to_player < 0: #right of player
                    eggnemy.center_position.x -= eggnemy.speed
                elif x_distance_to_player > 0: #left
                    eggnemy.center_position.x += eggnemy.speed

                if y_distance_to_player < 0: #down
                    eggnemy.center_position.y -= eggnemy.speed
                elif y_distance_to_player > 0: #up
                    eggnemy.center_position.y += eggnemy.speed
                    
    def eggnemy_overlap_check(self, eggnemy: Eggnemy):
        is_overlap: bool = self.is_overlapping_player(eggnemy) 

        if is_overlap and eggnemy not in self._overlapping_player_eggnemy:
            self._overlapping_player_eggnemy.append(eggnemy)

        if not is_overlap and eggnemy in self._overlapping_player_eggnemy:
            self._overlapping_player_eggnemy.remove(eggnemy)

    def eggnemy_spawn(self):
        if len(self._eggnemies) <= self._eggnemy_count - 1:
            eggnemy_width = self._eggnemy_width
            eggnemy_height = self._eggnemy_height
            eggnemy_center = None
            while True:
                test_eggnemy_x = random.randint(eggnemy_width, self._world_width - eggnemy_width)
                test_eggnemy_y = random.randint(eggnemy_height, self._world_height - eggnemy_height)
                
                eggnemy_center = Point(test_eggnemy_x, test_eggnemy_y)
                eggnemy = Eggnemy(
                    self._eggnemy_height, 
                    self._eggnemy_width,
                    self._eggnemy_max_hp,
                    eggnemy_center,
                    self.eggnemy_speed
                    )
                
                if not self.is_overlapping_player(eggnemy):
                    break
            self._eggnemies.append(eggnemy)

    @property
    def screen_width(self):
        return self._screen_width
    
    @property
    def screen_height(self):
        return self._screen_height

    @property
    def world_width(self):
        return self._world_width
    
    @property
    def world_height(self):
        return self._world_height

    @property
    def fps(self):
        return self._fps

    @property
    def player_egg(self):
        return self._player_egg
    
    @property
    def is_game_over(self):
        return self._is_game_over
    
    @property
    def eggnemies(self):
        return self._eggnemies
    
    @property
    def eggnemy_count(self):
        return self._eggnemy_count
    
    @property
    def eggnemy_width(self):
        return self._eggnemy_width
    
    @property
    def eggnemy_height(self):
        return self._eggnemy_height
    
    @property
    def eggnemy_speed(self):
        return self._eggnemy_speed

    @property
    def eggnemy_max_hp(self):
        return self._eggnemy_max_hp
    
    @property
    def num_defeated_eggnemies(self):
        return self._num_defeated_eggnemies

    @property
    def overlapping_player_eggnemy(self):
        return self._overlapping_player_eggnemy