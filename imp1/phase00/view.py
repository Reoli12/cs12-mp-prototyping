import pyxel
from project_types import UpdateHandler, DrawHandler, PlayerEgg

class View:
    def __init__(self, player_egg: PlayerEgg, window_width: int, window_height: int):
        self._player_egg = player_egg
        self._player_color = 1

        self._window_width = window_width
        self._window_height = window_height

    #Outputs
    def clear_screen(self):
        pyxel.cls(0)

    def draw_egg(self):
        x_pos = self._player_egg.center_position.x
        y_pos = self._player_egg.center_position.y
        player_width = self._player_egg.width
        player_height = self._player_egg.height

        pyxel.rect(
        x_pos - player_width / 2,
        y_pos - player_height / 2,
        player_width,
        player_height,
        self._player_color
    )
        
    def text_player_health(self):
        x_pos = self._player_egg.center_position.x
        y_pos = self._player_egg.center_position.y
        player_width = self._player_egg.width
        player_height = self._player_egg.height
        cur_hp = self._player_egg.current_hp
        max_hp = self._player_egg.total_hp

        pyxel.text( 
            x_pos - player_width / 2,
            y_pos + player_height,
            f'{cur_hp}/{max_hp}',
            self._player_color
            )
    
    #Inputs
    def is_w_pressed(self):
        return pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP)
    
    def is_a_pressed(self):
        return pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT)
    
    def is_s_pressed(self):
        return pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN)
    
    def is_d_pressed(self):
        return pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT)
    
    def start(self, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(self._window_width, self._window_height)
        pyxel.run(update_handler.update, draw_handler.draw)