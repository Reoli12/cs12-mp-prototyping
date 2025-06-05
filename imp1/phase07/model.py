from __future__ import annotations
from project_types import Eggnemy, PlayerEgg, Boss, Point, GameSettings, EggInfo, EgghancementSettings
from typing import Literal
from copy import deepcopy
import random
import math


class Model:
    def __init__(self, player_egg: PlayerEgg, settings: GameSettings, eggnemy_count: int, eggnemy_info: EggInfo, boss_info: EggInfo, boss_spawn_rate: int, egghancement: EgghancementSettings):
        #Stored parameters
        self._param_player_egg: PlayerEgg = player_egg
        self._param_settings: GameSettings = settings
        self._param_eggnemy_count: int = eggnemy_count
        self._param_eggnemy_info: EggInfo = eggnemy_info
        self._param_boss_info: EggInfo = boss_info
        self._param_boss_spawn_rate: int = boss_spawn_rate
        self._param_egghancement: EgghancementSettings = egghancement
        self._leaderboards: list[tuple[int, int]] = []
        self._leaderboards_str: list[str] = []
        self._is_time_get: bool = False

        '''
        Note: The isinstance code below is for testing purposes only. We are aware the code below does not improve the code's functionality.
        During testing, it was found that even though an Eggnemy or Boss was passed onto the player_egg parameter, the model would work perfectly fine.
        Pyright does flag it, but it should not work. Therefore, the code below was added for testing.
        '''
        if not isinstance(self._param_player_egg, PlayerEgg):
           raise TypeError("This is not a PlayerEgg type.")

        self.restart()

    def update(self, is_forward_pressed: bool, is_left_pressed: bool, is_down_pressed: bool, is_right_pressed: bool, is_attack_pressed: bool, egghancement_pressed: Literal[1, 2, 3, None]):

        if not self.is_to_be_egghanced:
            player_egg: PlayerEgg = self._player_egg

            #game over state
            if player_egg.stats.current_hp <= 0:
                self._is_game_over: bool = True
                self._sfx_player_dead: bool = True

            if self._is_game_over:
                return
            
            #player movement, position and attack
            self.player_movement(is_forward_pressed, is_down_pressed, is_left_pressed, is_right_pressed)

            self.player_attack(is_attack_pressed)
                
            if self.is_out_of_world_bounds(player_egg):
                self.return_to_world_bounds(player_egg)

            #eggnemies/boss movement and spawn
            self.eggnemy_movement()
            self.eggnemy_spawn()

            self.boss_movement()
            self.boss_spawn()
                
            #damage
            self.player_takes_damage()

            #time and frame
            if self._frame_count % self._fps == 0 and not self._is_game_over:
                self._sec += 1
                if self._sec % 60 == 0:
                    self._min += 1
                    self._sec = 0

            self._frame_count += 1
        
        else:
            self.egghancement_stats(egghancement_pressed)


    def is_overlapping_entities(self, entity_a: PlayerEgg | Eggnemy | Boss, entity_b: PlayerEgg | Eggnemy | Boss) -> bool:
        left_bounds: float = entity_a.leftmost_point
        right_bounds: float = entity_a.rightmost_point
        top_bounds: float = entity_a.topmost_point
        bottom_bounds: float = entity_a.bottom_point

        eggnemy_right: float = entity_b.rightmost_point
        eggnemy_left: float = entity_b.leftmost_point
        eggnemy_bottom: float = entity_b.bottom_point
        eggnemy_top: float = entity_b.topmost_point

        return not (left_bounds > eggnemy_right or 
                right_bounds < eggnemy_left or
                top_bounds > eggnemy_bottom or
                bottom_bounds < eggnemy_top)

    def is_out_of_world_bounds(self, entity: PlayerEgg | Eggnemy | Boss) -> bool:
        return (   
            entity.leftmost_point < 0 
            or entity.rightmost_point > self._world_width
            or entity.topmost_point < 0
            or entity.bottom_point > self._world_height 
        )

    def return_to_world_bounds(self, entity: PlayerEgg | Eggnemy | Boss):
        assert self.is_out_of_world_bounds(entity)
        
        if entity.leftmost_point < 0:
            entity.center_position.x = entity.stats.width / 2

        if entity.rightmost_point > self._world_width:
            entity.center_position.x = self._world_width - (entity.stats.width / 2)

        if entity.bottom_point > self._world_height:
            entity.center_position.y = self._world_height - (entity.stats.height / 2)

        if entity.topmost_point < 0:
            entity.center_position.y = entity.stats.height / 2
    
    def player_movement(self, forward_btn: bool, down_btn: bool, left_btn: bool, right_btn: bool):
        if forward_btn:
            self._player_egg.center_position.y -= self._player_egg.stats.speed
        if left_btn:
            self._player_egg.center_position.x -= self._player_egg.stats.speed
        if down_btn:
            self._player_egg.center_position.y += self._player_egg.stats.speed
        if right_btn:
            self._player_egg.center_position.x += self._player_egg.stats.speed

    def player_attack(self, is_attack_pressed: bool):
        if is_attack_pressed:
            radius: int = self._player_egg.player_attack_radius
            damage: int = self._player_egg.stats.atk

            for eggnemy in self._eggnemies:
                eggnemy_center = eggnemy.center_position
                
                #defeats eggnemy
                distance_to_player: float = ((self._player_egg.center_position.x - eggnemy_center.x) ** 2 + (self._player_egg.center_position.y - eggnemy_center.y) ** 2) ** 0.5
                if distance_to_player <= radius:
                    eggnemy.stats.current_hp -= damage

                    if eggnemy.stats.current_hp <= 0:
                        self._cur_xp += 1
                        self._num_defeated_eggnemies += 1
                        self._got_egghanced: bool = False
                        self._eggnemies.remove(eggnemy)
                        self.egghance_check()
                        if self._is_to_be_egghanced:
                            break
                        if eggnemy in self._overlapping_player_eggnemy:
                            self._overlapping_player_eggnemy.remove(eggnemy)

                    self._prev_wave_done = True if self._num_defeated_eggnemies % self._boss_spawn_rate and not self._boss_egg else False
            
            boss: None | Boss = self._boss_egg
            if boss:
                boss_distance_to_player: float = ((self._player_egg.center_position.x - boss.center_position.x) ** 2 + (self._player_egg.center_position.y - boss.center_position.y) ** 2) ** 0.5
                if boss_distance_to_player <= radius:
                    boss.stats.current_hp -= damage

                    if boss.stats.current_hp <= 0:
                        self._wave_count += 1
                        self._is_boss_dead = True
                        self._sfx_boss = True
                        self._boss_egg: None | Boss = None
                        if boss in self._overlapping_player_eggnemy:
                            self._overlapping_player_eggnemy.remove(boss)
   
    def eggnemy_overlap_check(self, eggnemy: Eggnemy):
        is_overlap: bool = self.is_overlapping_entities(self._player_egg, eggnemy) 

        if is_overlap and eggnemy not in self._overlapping_player_eggnemy:
            self._overlapping_player_eggnemy.append(eggnemy)

        if not is_overlap and eggnemy in self._overlapping_player_eggnemy:
            self._overlapping_player_eggnemy.remove(eggnemy)

    def eggnemy_spawn(self):
        if len(self._eggnemies) <= self._eggnemy_count - 1:
            eggnemy_width: int = self._eggnemy_width
            eggnemy_height: int = self._eggnemy_height
            eggnemy_center: None | Point = None
            self._eggnemy_max_hp: int = int(self._base_eggnemy_max_hp * (4) ** (self._wave_count))
            self._eggnemy_atk: int = int(self._base_eggnemy_atk * (1.05) ** self._wave_count)
            self._eggnemy_speed: int = int(self._base_eggnemy_speed + (2 * (math.log10(self._wave_count + 1))))

            while True:
                test_eggnemy_x: int = random.randint(eggnemy_width, self._world_width - eggnemy_width)
                test_eggnemy_y: int = random.randint(eggnemy_height, self._world_height - eggnemy_height)

                eggnemy_center = Point(test_eggnemy_x, test_eggnemy_y)
                new_eggnemy: Eggnemy = Eggnemy(
                    EggInfo(
                        eggnemy_width,
                        eggnemy_height,
                        self._eggnemy_max_hp,
                        self._eggnemy_max_hp,
                        self._eggnemy_atk,
                        self._eggnemy_speed
                    ),
                    eggnemy_center,
                    )
                
                #check overlap for player, other eggnemies, and boss
                if (not self.is_overlapping_entities(self.player_egg, new_eggnemy) and
                    not any(self.is_overlapping_entities(new_eggnemy, eggnemy) for eggnemy in self._eggnemies) and
                    (self._boss_egg is None or not self.is_overlapping_entities(new_eggnemy, self._boss_egg))):
                    break
            self._eggnemies.append(new_eggnemy)               

    def eggnemy_movement(self):
        for eggnemy in self._eggnemies:
            self.eggnemy_overlap_check(eggnemy)
            
            x_distance_to_player: float = self._player_egg.center_position.x - eggnemy.center_position.x
            y_distance_to_player: float = self._player_egg.center_position.y - eggnemy.center_position.y
            distance_to_player: float = ((x_distance_to_player) ** 2 + (y_distance_to_player) ** 2) ** 0.5
            original_center: Point = deepcopy(eggnemy.center_position)

            #follows player
            if not self._is_game_over and distance_to_player > 0:
                x_pos: float = (x_distance_to_player / distance_to_player) * eggnemy.stats.speed
                y_pos: float = (y_distance_to_player / distance_to_player) * eggnemy.stats.speed

                eggnemy.center_position.x += x_pos
                eggnemy.center_position.y += y_pos

            #if overlap with other eggnemy or boss, go back to original center
            if (any(self.is_overlapping_entities(eggnemy, other_eggnemy) for other_eggnemy in self._eggnemies if other_eggnemy != eggnemy) or
                (self._boss_egg and self.is_overlapping_entities(eggnemy, self._boss_egg))):
                eggnemy.center_position = original_center
            
            if self.is_out_of_world_bounds(eggnemy):
                self.return_to_world_bounds(eggnemy)

    def boss_spawn(self):
        if (not self._is_game_over and 
            self._prev_wave_done and
            not self._boss_egg and 
            self.num_defeated_eggnemies != 0 and 
            self._num_defeated_eggnemies % self._boss_spawn_rate == 0):
            
            self._prev_wave_done: bool = False
            self._is_boss_dead: bool = False
            boss_width: int = self._boss_width
            boss_height: int = self._boss_height
            boss_center: None | Point = None
            self._boss_max_hp: int = int(self._base_boss_max_hp * (4) ** self._wave_count)
            self._boss_atk: int = int(self._base_boss_atk * (1.5) ** self._wave_count)
            self._boss_speed: int = int(self._base_boss_speed + (4 * (math.log10(self._wave_count + 1))))

            while True:
                test_eggnemy_x: int = random.randint(boss_width, self._world_width - boss_width)
                test_eggnemy_y: int = random.randint(boss_height, self._world_height - boss_height)
                
                boss_center = Point(test_eggnemy_x, test_eggnemy_y)
                self._boss_egg = Boss(
                    EggInfo(
                        boss_width,
                        boss_height,
                        self._boss_max_hp,
                        self._boss_max_hp,
                        self._boss_atk,
                        self._boss_speed
                        ),
                    boss_center,
                    )
                if (not self.is_overlapping_entities(self.player_egg, self._boss_egg) and
                    not any(self.is_overlapping_entities(self._boss_egg, eggnemy) for eggnemy in self._eggnemies)):
                    break
    
    def boss_movement(self):
        if self._boss_egg:
            x_distance_to_player: float = self._player_egg.center_position.x - self._boss_egg.center_position.x
            y_distance_to_player: float = self._player_egg.center_position.y - self._boss_egg.center_position.y
            
            distance_to_player: float = ((x_distance_to_player) ** 2 + (y_distance_to_player) ** 2) ** 0.5
            
            #follows player
            if not self._is_game_over and distance_to_player > 0:
                x_pos: float = (x_distance_to_player / distance_to_player) * self._boss_egg.stats.speed
                y_pos: float = (y_distance_to_player / distance_to_player) * self._boss_egg.stats.speed
                original_center: Point = deepcopy(self._boss_egg.center_position)

                self._boss_egg.center_position.x += x_pos
                self._boss_egg.center_position.y += y_pos
            
                #if overlap with other eggnemy, go back to original pos
                if (any(self.is_overlapping_entities(self._boss_egg, other_eggnemy) for other_eggnemy in self._eggnemies)):
                    self._boss_egg.center_position = original_center

            if self.is_out_of_world_bounds(self._boss_egg):
                self.return_to_world_bounds(self._boss_egg)

    def restart(self):
        self._is_time_get = False
        
        self._screen_width: int = self._param_settings.screen_width
        self._screen_height: int = self._param_settings.screen_height
        self._world_width: int = self._param_settings.world_width
        self._world_height: int = self._param_settings.world_height
        self._fps: int = self._param_settings.fps
        self._frame_count: int = 0
        self._sec: int = 0
        self._min: int = 0

        self._player_egg: PlayerEgg = deepcopy(self._param_player_egg)
        self._egghancement: EgghancementSettings = deepcopy(self._param_egghancement)
        self._is_to_be_egghanced: bool = False
        self._got_egghanced = False
        self._cur_xp: int = 0

        self._eggnemies: list[Eggnemy] = []
        self._overlapping_player_eggnemy: list[Eggnemy] = []
        self._num_defeated_eggnemies: int = 0
        self._eggnemy_count: int = self._param_eggnemy_count
        self._eggnemy_info: EggInfo = deepcopy(self._param_eggnemy_info)
        self._eggnemy_width: int = self._eggnemy_info.width
        self._eggnemy_height: int = self._eggnemy_info.height

        self._base_eggnemy_speed: int = self._eggnemy_info.speed
        self._eggnemy_speed = self._base_eggnemy_speed
        self._base_eggnemy_max_hp: int = self._eggnemy_info.max_hp
        self._eggnemy_max_hp = self._base_eggnemy_max_hp
        self._base_eggnemy_atk: int = self._eggnemy_info.atk
        self._eggnemy_atk = self._base_eggnemy_atk
        
        self._boss_egg = None
        self._boss_info: EggInfo = deepcopy(self._param_boss_info)
        self._boss_spawn_rate: int = self._param_boss_spawn_rate
        self._boss_width: int = self._boss_info.width
        self._boss_height: int = self._boss_info.height

        self._base_boss_speed: int = self._boss_info.speed
        self._boss_speed = self._base_boss_speed
        self._base_boss_max_hp: int = self._boss_info.max_hp
        self._boss_max_hp = self._base_boss_max_hp
        self._base_boss_atk: int = self._boss_info.atk
        self._boss_atk = self._base_boss_atk
        self._is_boss_dead: bool = False

        self._prev_wave_done = False
        self._wave_count: int = 0
        self._is_game_over = False

        self._sfx_boss: bool = False
        self._sfx_egghancement: bool = False
        self._sfx_player_dead: bool = False

    def update_leaderboards(self, min: int, sec: int):
        self._is_time_get = True
        self._leaderboards.append((min, sec))

        #in terms of seconds
        self._leaderboards.sort(key=lambda time: time[0] * 60 + time[1], reverse=True)
        self._leaderboards = self._leaderboards [:3]
        self.leaderboards_stringify()
    
    def leaderboards_stringify(self):
        runs: list[tuple[int, int]] = self.leaderboards
        self._leaderboards_str = []
        runs_str: list[str] = self._leaderboards_str
            
        for i, (min, sec) in enumerate(runs, 1):
            #stringify time
            run_sec_str: str = f'{sec}' if sec > 9 else f'0{sec}'
            run_min_str: str = f'{min}' if min > 9 else f'0{min}'
            time_str: str = f"{run_min_str}:{run_sec_str}"
            
            #place handler
            if i == 1:
                run_str: str = f'Top 1   {time_str}'
                runs_str.append(run_str)
            else:
                run_str = f'    {i}   {time_str}'
                runs_str.append(run_str)

        if len(runs_str) < 3:
            # 2 missing, len(runs_str) = 1, [2, 3]
            # 1 missing, len(runs_str) = 2, [3,]
            for i in range(len(runs_str) + 1, 4):
                run_str = f'    {i}   --:--'
                runs_str.append(run_str)

    def egghancement_stats(self, egghancement_pressed: Literal[1, 2, 3, None]):
        match egghancement_pressed:
            case 1:
                self._player_egg.stats.current_hp += self._egghancement.inc_max_hp
                self._player_egg.stats.max_hp += self._egghancement.inc_max_hp
            case 2:
                self._player_egg.stats.atk += self._egghancement.inc_atk
            case 3:
                self._player_egg.stats.speed += self._egghancement.inc_spd
            case _:
                return
        
        self._is_to_be_egghanced: bool = False
        self._got_egghanced: bool = True
        self._sfx_egghancement: bool = True

    def player_takes_damage(self):
        if self._frame_count % self._fps == 0 and len(self._overlapping_player_eggnemy) > 0:
            self._player_egg.stats.current_hp -= self._eggnemy_info.atk

        if self._frame_count % self._fps == 0  and self._boss_egg and self.is_overlapping_entities(self._player_egg, self._boss_egg):
            self._player_egg.stats.current_hp -= self._boss_egg.stats.atk 

    def egghance_check(self):
        if not self._got_egghanced and self._cur_xp != 0 and self._cur_xp % self._egghancement.xp_needed == 0:
            self._is_to_be_egghanced = True

    def sfx_player_dead_played(self):
        self._sfx_player_dead = False

    def sfx_boss_played(self):
        self._sfx_boss = False

    def sfx_egghancement_played(self):
        self._sfx_egghancement = False

    @property
    def param_player_egg(self) -> PlayerEgg:
        return self._param_player_egg
    
    @property
    def param_settings(self) -> GameSettings:
        return self._param_settings
    
    @property
    def param_eggnemy_count(self) -> int:
        return self._param_eggnemy_count
    
    @property
    def param_eggnemy_info(self) -> EggInfo:
        return self._param_eggnemy_info

    @property
    def param_boss_info(self) -> EggInfo:
        return self._param_boss_info
    
    @property
    def param_boss_spawn_rate(self) -> int:
        return self._param_boss_spawn_rate
    
    @property
    def param_egghancement(self) -> EgghancementSettings:
        return self._param_egghancement

    @property
    def leaderboards(self) -> list[tuple[int, int]]:
        return self._leaderboards

    @property
    def leaderboards_str(self) -> list[str]:
        return self._leaderboards_str

    @property
    def is_time_get(self) -> bool:
        return self._is_time_get

    @property
    def screen_width(self) -> int:
        return self._screen_width
    
    @property
    def screen_height(self) -> int:
        return self._screen_height

    @property
    def world_width(self) -> int:
        return self._world_width
    
    @property
    def world_height(self) -> int:
        return self._world_height

    @property
    def fps(self) -> int:
        return self._fps

    @property
    def frame_count(self) -> int:
        return self._frame_count
    
    @property
    def sec(self) -> int:
        return self._sec
    
    @property
    def min(self) -> int:
        return self._min

    @property
    def player_egg(self) -> PlayerEgg:
        return self._player_egg
    
    @property
    def egghancement(self) -> EgghancementSettings:
        return self._egghancement
    
    @property
    def is_to_be_egghanced(self) -> bool:
        return self._is_to_be_egghanced
    
    @property
    def got_egghanced(self) -> bool:
        return self._got_egghanced

    @property
    def cur_xp(self) -> int:
        return self._cur_xp

    @property
    def eggnemies(self) -> list[Eggnemy]:
        return self._eggnemies
    
    @property
    def overlapping_player_eggnemy(self) -> list[Eggnemy]:
        return self._overlapping_player_eggnemy
    
    @property
    def num_defeated_eggnemies(self) -> int:
        return self._num_defeated_eggnemies
    
    @property
    def eggnemy_count(self) -> int:
        return self._eggnemy_count
    
    @property
    def eggnemy_info(self) -> EggInfo:
        return self._eggnemy_info

    @property
    def eggnemy_width(self) -> int:
        return self._eggnemy_width
    
    @property
    def eggnemy_height(self) -> int:
        return self._eggnemy_height
    
    @property
    def base_eggnemy_speed(self) -> int:
        return self._base_eggnemy_speed
    
    @property
    def eggnemy_speed(self) -> int:
        return self._eggnemy_speed

    @property
    def base_eggnemy_max_hp(self) -> int:
        return self._base_eggnemy_max_hp
    
    @property
    def eggnemy_max_hp(self) -> int:
        return self._eggnemy_max_hp
    
    @property
    def base_eggnemy_atk(self) -> int:
        return self._base_eggnemy_atk
    
    @property
    def eggnemy_atk(self) -> int:
        return self._eggnemy_atk
    
    @property
    def boss_egg(self) -> None | Boss:
        return self._boss_egg
    
    @property
    def boss_info(self) -> EggInfo:
        return self._boss_info

    @property
    def boss_spawn_rate(self) -> int:
        return self._boss_spawn_rate
    
    @property
    def boss_width(self) -> int:
        return self._boss_width
    
    @property
    def boss_height(self) -> int:
        return self._boss_height
    
    @property
    def base_boss_speed(self) -> int:
        return self._base_boss_speed
    
    @property
    def boss_speed(self) -> int:
        return self._boss_speed
    
    @property
    def base_boss_max_hp(self) -> int:
        return self._base_boss_max_hp
    
    @property
    def boss_max_hp(self) -> int:
        return self._boss_max_hp
    
    @property
    def base_boss_atk(self) -> int:
        return self._base_boss_atk
    
    @property
    def boss_atk(self) -> int:
        return self._boss_atk

    @property
    def prev_wave_done(self) -> bool:
        return self._prev_wave_done

    @property
    def wave_count(self) -> int:
        return self._wave_count

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over
    
    @property
    def is_boss_dead(self) -> bool:
        return self._is_boss_dead

    @property
    def sfx_boss(self) -> bool:
        return self._sfx_boss
    
    @property
    def sfx_egghancement(self) -> bool:
        return self._sfx_egghancement
    
    @property
    def sfx_player_dead(self) -> bool:
        return self._sfx_player_dead