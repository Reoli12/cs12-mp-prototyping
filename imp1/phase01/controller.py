from model import Model
from view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view

    def update(self):
        self._model.update(
            self._view.is_forward_pressed(), 
            self._view.is_left_pressed(), 
            self._view.is_down_pressed(), 
            self._view.is_right_pressed(),
            self._view.is_attack_pressed()
            )

    def draw(self):
        self._view.clear_screen()

        player_x_pos = int(self._model.player_egg.leftmost_point)
        player_y_pos = int(self._model.player_egg.topmost_point)
        player_width = self._model.player_egg.width
        player_height = self._model.player_egg.height
        player_cur_hp = self._model.player_egg.current_hp
        player_total_hp = self._model.player_egg.total_hp

        player_hp_x = int(player_x_pos - player_width / 2)
        player_hp_y = player_y_pos + int(player_height * 1.5) 

        if not self._model.is_game_over:
            self._view.draw_egg(player_x_pos, player_y_pos, player_width, player_height)
        
        self._view.text_player_health(player_hp_x, player_hp_y, player_cur_hp, player_total_hp)

        eggnemies = self._model.eggnemies
        for eggnemy in eggnemies:
            x_pos = int(eggnemy.leftmost_point)
            y_pos = int(eggnemy.topmost_point)
            width = eggnemy.width
            height = eggnemy.height
            self._view.draw_eggnemy(x_pos, y_pos, width, height)
        
    def start(self):
        self._view.start(self._model.fps, self, self)