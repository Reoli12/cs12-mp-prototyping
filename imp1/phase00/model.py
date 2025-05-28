from __future__ import annotations
from project_types import Eggnemy, PlayerEgg, Point
import random


class Model:
    def __init__(self, player_egg: PlayerEgg, fps: int, window_width: int, window_height: int, eggnemy_count: int, eggnemy_width: int, eggnemy_height: int):
        self._window_width = window_width
        self._window_height = window_height
        self._fps = fps

        self._player_egg = player_egg

        self._eggnemies: list[Eggnemy] = []
        self._overlapping_player_eggnemy: list[Eggnemy] = []
        self._eggnemy_count = eggnemy_count
        self._eggnemy_width = eggnemy_width
        self._eggnemy_height = eggnemy_height

        self._is_game_over = False

    def update(self, is_w_pressed: bool, is_a_pressed: bool, is_s_pressed: bool, is_d_pressed: bool, is_l_pressed: bool):
        player_egg = self._player_egg

        #game over state
        if player_egg.current_hp <= 0:
            self._is_game_over = True

        if self._is_game_over:
            return
        
        #player movement and state
        if is_w_pressed:
            player_egg.center_position.y -= 2

        if is_a_pressed:
            player_egg.center_position.x -= 2

        if is_s_pressed:
            player_egg.center_position.y += 2  

        if is_d_pressed:
            player_egg.center_position.x += 2

        if is_l_pressed:
            radius = 50
            for eggnemy in self._eggnemies:
                eggnemy_center = eggnemy.center_position
                
                #defeats eggnemy
                distance_to_player = ((self._player_egg.center_position.x - eggnemy_center.x) ** 2 + (self._player_egg.center_position.y - eggnemy_center.y) ** 2) ** 0.5
                if distance_to_player <= radius:
                    self._eggnemies.remove(eggnemy)
            

        if self.is_out_of_bounds():
            self.return_to_bounds()

        #eggnemies
        for eggnemy in self._eggnemies:
            if self.is_overlapping_player(eggnemy.center_position, eggnemy.width, eggnemy.height):
                self._overlapping_player_eggnemy.append(eggnemy)

                if self._fps % 30 == 0:
                    self._player_egg.current_hp -= 1 
            
            x_distance_to_player = self._player_egg.center_position.x - eggnemy.center_position.x
            y_distance_to_player = self._player_egg.center_position.y - eggnemy.center_position.y
            
            '''#follows player
            if x_distance_to_player < 0: #right of player
                eggnemy.center_position.x -= 1 
            elif x_distance_to_player > 0: #left
                eggnemy.center_position.x += 1

            if y_distance_to_player < 0: #down
                eggnemy.center_position.y -= 1 
            elif y_distance_to_player > 0: #up
                eggnemy.center_position.y += 1'''


        if len(self._eggnemies) <= self._eggnemy_count - 1:
            eggnemy_width = self._eggnemy_width
            eggnemy_height = self._eggnemy_height
            eggnemy_center = None
            while True:
                test_eggnemy_x = random.randint(eggnemy_width, self._window_width - eggnemy_width)
                test_eggnemy_y = random.randint(eggnemy_height, self._window_height - eggnemy_height)
                
                eggnemy_center = Point(test_eggnemy_x, test_eggnemy_y)
                
                if not self.is_overlapping_player(eggnemy_center, eggnemy_width, eggnemy_height):
                    eggenemy = Eggnemy(
                        self._eggnemy_height, 
                        self._eggnemy_width,
                        1,
                        eggnemy_center
                        )
                    break
            self._eggnemies.append(eggenemy)

        print(player_egg.center_position, player_egg.topmost_point)
    
    def is_overlapping_player(self, eggnemy_center: Point, eggnemy_width: int, eggnemy_height: int):
        player_x = self._player_egg.center_position.x
        player_y = self._player_egg.center_position.y
        eggnemy_x = eggnemy_center.x
        eggnemy_y = eggnemy_center.y

        left_bounds = player_x - self._player_egg.width / 2
        right_bounds = player_x + self._player_egg.width / 2
        top_bounds = player_y - self._player_egg.height / 2
        bottom_bounds = player_y + self._player_egg.height / 2

        eggnemy_right = eggnemy_x + eggnemy_width / 2
        eggnemy_left = eggnemy_x - eggnemy_width / 2
        eggnemy_bottom = eggnemy_y + eggnemy_height / 2
        eggnemy_top = eggnemy_y - eggnemy_height / 2

        return (left_bounds < eggnemy_right or 
                right_bounds > eggnemy_left or
                top_bounds < eggnemy_bottom or
                bottom_bounds > eggnemy_top)

    def is_out_of_bounds(self) -> bool:
        return (   
            self._player_egg.leftmost_point < 0 
            or self._player_egg.rightmost_point > self._window_width
            or self._player_egg.topmost_point < 0
            or self._player_egg.bottom_point > self._window_height 
        )

    def return_to_bounds(self):
        player_egg = self._player_egg
        assert self.is_out_of_bounds()
        
        if player_egg.leftmost_point < 0:
            player_egg.center_position.x = player_egg.width / 2

        if player_egg.rightmost_point > self._window_width:
            player_egg.center_position.x = self._window_width - (player_egg.width / 2)

        if player_egg.bottom_point > self._window_height:
            player_egg.center_position.y = self._window_height - (player_egg.height / 2)

        if player_egg.topmost_point < 0:
            player_egg.center_position.y = player_egg.height / 2



    @property
    def window_width(self):
        return self._window_width
    
    @property
    def window_height(self):
        return self._window_height

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
    def overlapping_player_eggnemy(self):
        return self._overlapping_player_eggnemy