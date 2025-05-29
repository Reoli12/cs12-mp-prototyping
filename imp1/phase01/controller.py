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

        #player and camera
        player_x_pos = int(self._model.player_egg.leftmost_point)
        player_y_pos = int(self._model.player_egg.topmost_point)
        player_width = self._model.player_egg.width
        player_height = self._model.player_egg.height
        
        camera_x = player_x_pos - self._model.screen_width // 2
        camera_y = player_y_pos - self._model.screen_height // 2

        player_cur_hp = self._model.player_egg.current_hp
        player_total_hp = self._model.player_egg.total_hp
        player_hp_x = int((player_x_pos - player_width / 2))
        player_hp_y = int(player_y_pos + int(player_height * 1.5))

        self._view.draw_world(-camera_x, -camera_y)

        if not self._model.is_game_over:
            self._view.draw_egg(
                player_x_pos - camera_x, 
                player_y_pos - camera_y, 
                player_width, 
                player_height)
        
        self._view.text_player_health(
            player_hp_x - camera_x, 
            player_hp_y - camera_y, 
            player_cur_hp, 
            player_total_hp)

        #eggnemies
        eggnemies = self._model.eggnemies
        for eggnemy in eggnemies:
            eggnemy_x_pos = int(eggnemy.leftmost_point)
            eggnemy_y_pos = int(eggnemy.topmost_point)
            eggnemy_width = eggnemy.width
            eggnemy_height = eggnemy.height

            eggnemy_cur_hp = eggnemy.current_hp
            eggnemy_total_hp = eggnemy.total_hp
            eggnemy_hp_x = int((eggnemy_x_pos - eggnemy_width / 2))
            eggnemy_hp_y = int(eggnemy_y_pos + int(eggnemy_height * 1.5))

            self._view.draw_eggnemy(
                eggnemy_x_pos - camera_x, 
                eggnemy_y_pos - camera_y, 
                eggnemy_width, 
                eggnemy_height)
            self._view.text_eggnemy_health(
                eggnemy_hp_x - camera_x, 
                eggnemy_hp_y - camera_y, 
                eggnemy_cur_hp, 
                eggnemy_total_hp)
            
        #boss
            
        #stats
        num_defeated_eggnemies = self._model.num_defeated_eggnemies
        num_defeated_x_pos = 7
        num_defeated_y_pos = 7
        self._view.text_num_defeated_eggnemy(
            num_defeated_x_pos, 
            num_defeated_y_pos, 
            num_defeated_eggnemies)
        
    def start(self):
        self._view.start(self._model.fps, self, self)