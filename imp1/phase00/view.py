import pyxel
from project_types import UpdateHandler, DrawHandler

class View:
    def __init__(self, window_width: int, window_height: int):
        self._player_color = 7
        self._eggnemy_color = 15

        self._window_width = window_width
        self._window_height = window_height

    #Outputs
    def clear_screen(self):
        pyxel.cls(0)

    def draw_egg(self, x_pos: int, y_pos: int, width: int, height: int):
        pyxel.rect(
        x_pos,
        y_pos,
        width,
        height,
        self._player_color
    )
        
    def text_player_health(self, x_pos: int, y_pos: int, cur_hp: int, total_hp: int):
        pyxel.text( 
            x_pos,
            y_pos,
            f'{cur_hp}/{total_hp}',
            self._player_color
            )
    
    def draw_eggnemy(self, x_pos: int, y_pos: int, width: int, height: int):
        pyxel.rect(
        x_pos,
        y_pos,
        width,
        height,
        self._eggnemy_color
    )


    #Inputs
    def is_forward_pressed(self):
        return pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP)
    
    def is_left_pressed(self):
        return pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT)
    
    def is_down_pressed(self):
        return pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN)
    
    def is_right_pressed(self):
        return pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT)
    
    def is_attack_pressed(self):
        return pyxel.btn(pyxel.KEY_L)
    
    def start(self, fps: int, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(self._window_width, self._window_height, fps=fps)
        pyxel.run(update_handler.update, draw_handler.draw)