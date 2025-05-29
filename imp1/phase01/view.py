import pyxel
from project_types import UpdateHandler, DrawHandler, GameSettings

class View:
    def __init__(self, settings: GameSettings):
        self._player_color = 7
        self._eggnemy_color = 13
        self._world_border_color = 7

        self._screen_width = settings.screen_width
        self._screen_height = settings.screen_height
        self._world_width = settings.world_width
        self._world_height = settings.world_height

    #Outputs
    def clear_screen(self):
        pyxel.cls(0)

    def draw_world(self, x_pos: int, y_pos: int):
        pyxel.rectb(
            x_pos,
            y_pos,
            self._world_width,
            self._world_height,
            self._world_border_color
        )

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
        
    def text_eggnemy_health(self, x_pos: int, y_pos: int, cur_hp: int, total_hp: int):
        pyxel.text( 
            x_pos,
            y_pos,
            f'{cur_hp}/{total_hp}',
            self._eggnemy_color
            )
        
    def text_num_defeated_eggnemy(self, x_pos: int, y_pos: int, num: int):
        pyxel.text(
            x_pos,
            y_pos,
            f'{num}',
            self._player_color
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
        pyxel.init(self._screen_width, self._screen_height, fps=fps)
        pyxel.run(update_handler.update, draw_handler.draw)