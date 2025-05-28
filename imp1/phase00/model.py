from __future__ import annotations
from project_types import PlayerEgg


EGG_HEIGHT = 20
EGG_WID = 10
EGG_HP = 10

class Model:
    def __init__(self, player_egg: PlayerEgg, window_width: int, window_height: int):
        self._window_width = window_width
        self._window_height = window_height

        self._player_egg = player_egg
        
        self._is_game_over = False

    def update(self, is_w_pressed: bool, is_a_pressed: bool, is_s_pressed: bool, is_d_pressed: bool):
        player_egg = self._player_egg

        #game over state
        if player_egg.current_hp <= 0:
            self._is_game_over = True

        if self._is_game_over:
            return
        
        #player movement
        if is_w_pressed:
            player_egg.center_position.y -= 2

        if is_a_pressed:
            player_egg.center_position.x -= 2

        if is_s_pressed:
            player_egg.center_position.y += 2  

        if is_d_pressed:
            player_egg.center_position.x += 2

        if self.is_out_of_bounds():
            self.return_to_bounds()

        print(player_egg.center_position, player_egg.topmost_point)


#if not working change egg to self._player_egg
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
    def player_egg(self):
        return self._player_egg
    
    @property
    def is_game_over(self):
        return self._is_game_over