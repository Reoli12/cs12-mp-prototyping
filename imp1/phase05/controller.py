from model import Model
from view import View
from copy import deepcopy
from typing import Literal


class Controller:
    def __init__(self, model: Model, view: View):
        self._model: Model = model
        self._view: View = view

    def update(self):
        if self._model.is_game_over or self._model.is_game_won:
            if not self._model.is_time_get and self._model.is_game_won:
                min = deepcopy(self._model.min)
                sec = deepcopy(self._model.sec)
                self._model.update_leaderboards(min, sec)
            if self._view.is_restart_pressed():
                self._model.restart()
            return

        egghancement_chosen: Literal[1, 2, 3, None] = None
        if self._model.is_egghance and not egghancement_chosen:
            egghancement_pressed: list[bool] = [
                self._view.is_first_egghancement(),
                self._view.is_second_egghancement(),
                self._view.is_third_egghancement()
            ]
            egghancement_pressed_indices: list[int] = [
                i for (i, chosen) in enumerate(egghancement_pressed, 1) if chosen
            ]
            print(egghancement_pressed)
            print(egghancement_pressed_indices)
            print(egghancement_chosen)
            
            if len(egghancement_pressed_indices) == 1:
                [egghancement_checker] = egghancement_pressed_indices
                match egghancement_checker:
                    case 1:
                        egghancement_chosen = 1
                    case 2:
                        egghancement_chosen = 2
                    case 3:
                        egghancement_chosen = 3
                    case _:
                        pass
        
        self._model.update(
            self._view.is_forward_pressed(), 
            self._view.is_left_pressed(), 
            self._view.is_down_pressed(), 
            self._view.is_right_pressed(),
            self._view.is_attack_pressed(),
            egghancement_chosen
            )

    def draw(self):
        self._view.clear_screen()

        #screen dimensions
        screen_width = self._model.screen_width
        screen_height = self._model.screen_height

        #player and camera
        player_x_pos: int = int(self._model.player_egg.leftmost_point)
        player_y_pos: int = int(self._model.player_egg.topmost_point)
        player_width: int = self._model.player_egg.stats.width
        player_height: int = self._model.player_egg.stats.height
        
        camera_x_pos: int = player_x_pos - screen_width // 2
        camera_y_pos: int = player_y_pos - screen_height // 2 + 5

        player_cur_hp: int = self._model.player_egg.stats.current_hp
        player_max_hp: int = self._model.player_egg.stats.max_hp
        player_hp_x_pos: int = int((player_x_pos - player_width / 2))
        player_hp_y_pos: int = int(player_y_pos + int(player_height * 1.25))

        #player egg
        if not self._model.is_game_over:
            self._view.draw_egg(
                player_x_pos - camera_x_pos, 
                player_y_pos - camera_y_pos, 
                player_width, 
                player_height)
        
        #player hp
        self._view.text_player_health(
            player_hp_x_pos - camera_x_pos, 
            player_hp_y_pos - camera_y_pos, 
            player_cur_hp, 
            player_max_hp)

        #eggnemies
        eggnemies = self._model.eggnemies
        for eggnemy in eggnemies:
            eggnemy_x_pos: int = int(eggnemy.leftmost_point)
            eggnemy_y_pos: int = int(eggnemy.topmost_point)
            eggnemy_width: int = eggnemy.stats.width
            eggnemy_height: int = eggnemy.stats.height

            eggnemy_cur_hp: int = eggnemy.stats.current_hp
            eggnemy_max_hp: int = eggnemy.stats.max_hp
            eggnemy_hp_x: int = int((eggnemy_x_pos -( eggnemy_width / 2) ** 0.5))
            eggnemy_hp_y: int = int(eggnemy_y_pos + int(eggnemy_height * 1.5))

            #eggnemy
            self._view.draw_eggnemy(
                eggnemy_x_pos - camera_x_pos, 
                eggnemy_y_pos - camera_y_pos, 
                eggnemy_width, 
                eggnemy_height)
            
            #eggnemy hp
            self._view.text_eggnemy_health(
                eggnemy_hp_x - camera_x_pos, 
                eggnemy_hp_y - camera_y_pos, 
                eggnemy_cur_hp, 
                eggnemy_max_hp)
            
        #boss
        boss = self._model.boss_egg
        if boss:
            assert boss
            boss_x_pos: int = int(boss.leftmost_point)
            boss_y_pos: int = int(boss.topmost_point)
            boss_width: int = boss.stats.width
            boss_height: int = boss.stats.height

            boss_cur_hp: int = boss.stats.current_hp
            boss_max_hp: int = boss.stats.max_hp
            boss_hp_x: int = int((boss_x_pos - (boss_width / 2) ** 0.5))
            boss_hp_y: int = int(boss_y_pos + int(boss_height * 1.25))

            #boss
            self._view.draw_boss(
                boss_x_pos - camera_x_pos, 
                boss_y_pos - camera_y_pos, 
                boss_width, 
                boss_height)

            #boss hp
            self._view.text_boss_health(
                boss_hp_x - camera_x_pos, 
                boss_hp_y - camera_y_pos, 
                boss_cur_hp, 
                boss_max_hp)
            
        #world border
        self._view.draw_world(-camera_x_pos, -camera_y_pos)

        #stats
        num_defeated_eggnemies: int = self._model.num_defeated_eggnemies
        num_defeated_x_pos: int = 7
        num_defeated_y_pos: int = 7

        #num defeated
        self._view.text_num_defeated_eggnemy(
            num_defeated_x_pos, 
            num_defeated_y_pos, 
            num_defeated_eggnemies)
        
        time_x_pos: int = screen_width - 25
        time_y_pos: int = 7
        sec: int = self._model.sec
        sec_str: str = f'{sec}' if sec > 9 else f'0{sec}'
        min: int = self._model.min
        min_str: str = f'{min}' if min > 9 else f'0{min}'
        time: str = f'{min_str}:{sec_str}'

        #time
        self._view.text_time(
            time_x_pos, 
            time_y_pos,
            time)

        #leaderboards
        if self._model.is_game_over or self._model.is_game_won:
            runs_str: list[str] = self._model.leaderboards_str

            leaderboard_x_pos = 7
            leaderboard_spacing = 10
            leaderboard_y_pos = screen_height - (leaderboard_spacing * len(runs_str)) - 7
            
            for (i, top_runs_str) in enumerate(runs_str):
                self._view.text_leaderboards(
                    leaderboard_x_pos,
                    leaderboard_y_pos + (i * leaderboard_spacing),
                    top_runs_str)
        
        #end state messages
        if self._model.is_game_won:
            win_x_pos: int = int((player_x_pos - int((player_width / 2) * 2)))
            win_y_pos: int = int(player_y_pos - int(player_height))

            #win message
            self._view.text_win_message(
            win_x_pos - camera_x_pos, 
            win_y_pos - camera_y_pos)

        if self._model.is_game_over or self._model.is_game_won:
            restart_x_pos = player_hp_x_pos - 13
            restart_y_pos = int(player_y_pos + int(player_height * 2))

            #restart message
            self._view.text_restart_message(
                restart_x_pos - camera_x_pos,
                restart_y_pos - camera_y_pos
            )
        
        #egghance
        if self._model.is_egghance:
            egghance_x_pos = screen_width // 4
            egghance_y_pos = int(screen_height // 2.5)
            egghance_width = screen_width // 2
            egghance_height = screen_height // 8
            self._view.draw_egghance_ui(
                egghance_x_pos,
                egghance_y_pos,
                egghance_width,
                egghance_height
            )
            egghance_text_x_pos = egghance_x_pos + egghance_width // 7
            egghance_text_y_pos = egghance_y_pos + egghance_height // 6
            egghance_spacing = egghance_height // 4

            self._view.text_egghance(
                egghance_text_x_pos,
                egghance_text_y_pos,
                egghance_spacing)

        
    def start(self):
        self._view.start(self._model.fps, self, self)