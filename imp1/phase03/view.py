import pyxel
from project_types import UpdateHandler, DrawHandler, GameSettings

class View:
    def __init__(self, settings: GameSettings):
        self._player_color: int = 1
        self._eggnemy_color: int = 13
        self._boss_color: int = 10
        self._world_border_color: int = 7
        self._text_stats_color: int = 7
        self._screen_width: int = settings.screen_width
        self._screen_height: int = settings.screen_height
        self._world_width: int = settings.world_width
        self._world_height: int = settings.world_height

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
        
    def text_player_health(self, x_pos: int, y_pos: int, cur_hp: int, max_hp: int):
        pyxel.text( 
            x_pos,
            y_pos,
            f'{cur_hp}/{max_hp}',
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
        
    def text_eggnemy_health(self, x_pos: int, y_pos: int, cur_hp: int, max_hp: int):
        pyxel.text( 
            x_pos,
            y_pos,
            f'{cur_hp}/{max_hp}',
            self._eggnemy_color
            )
            
    def draw_boss(self, x_pos: int, y_pos: int, width: int, height: int):
        pyxel.rect(
        x_pos,
        y_pos,
        width,
        height,
        self._boss_color
    )        
        
    def text_boss_health(self, x_pos: int, y_pos: int, cur_hp: int, max_hp: int):
        pyxel.text( 
            x_pos,
            y_pos,
            f'{cur_hp}/{max_hp}',
            self._boss_color
            )
        
    def text_num_defeated_eggnemy(self, x_pos: int, y_pos: int, num: int):
        pyxel.text(
            x_pos,
            y_pos,
            f'{num}',
            self._text_stats_color
        ) 

    def text_time(self, x_pos: int, y_pos: int, time: str):
        pyxel.text(
            x_pos,
            y_pos,
            time,
            self._text_stats_color
        )

    def text_win_message(self, x_pos: int, y_pos: int):
        pyxel.text(
            x_pos,
            y_pos,
            f'You Win!',
            self._text_stats_color
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