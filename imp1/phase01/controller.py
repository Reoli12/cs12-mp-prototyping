from model import Model
from view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view

    def update(self):
        self._model.update(
            self._view.is_w_pressed(), 
            self._view.is_a_pressed(), 
            self._view.is_s_pressed(), 
            self._view.is_d_pressed(),
            self._view.is_l_pressed()
            )

    def draw(self):
        self._view.clear_screen()

        if not self._model.is_game_over:
            self._view.draw_egg()
        
        self._view.text_player_health()

        eggnemies = self._model.eggnemies
        for eggnemy in eggnemies:
            self._view.draw_eggnemy(eggnemy)
        
    def start(self):
        self._view.start(self._model.fps, self, self)