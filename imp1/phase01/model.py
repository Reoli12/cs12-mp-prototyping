from __future__ import annotations
from project_types import Eggnemy, PlayerEgg, Boss, Point, GameSettings, EggInfo
import random


class Model:
    def __init__(self, player_egg: PlayerEgg, settings: GameSettings, eggnemy_count: int, eggnemy_info: EggInfo, boss_info: EggInfo, boss_spawn_rate: int):
        self._screen_width = settings.screen_width
        self._screen_height = settings.screen_height
        self._world_width = settings.world_width
        self._world_height = settings.world_height
        self._fps = settings.fps
        self._frame_count = 0
        self._sec = 0
        self._min = 0

        self._player_egg = player_egg

        self._eggnemies: list[Eggnemy] = []
        self._overlapping_player_eggnemy: list[Eggnemy] = []
        self._num_defeated_eggnemies = 0
        self._eggnemy_count = eggnemy_count
        self._eggnemy_width = eggnemy_info.width
        self._eggnemy_height = eggnemy_info.height
        self._eggnemy_speed = eggnemy_info.speed
        self._eggnemy_max_hp = eggnemy_info.max_hp
        
        self._boss_egg: None | Boss = None
        self._boss_spawn_rate = boss_spawn_rate
        self._boss_width = boss_info.width
        self._boss_height = boss_info.height
        self._boss_speed = boss_info.speed
        self._boss_max_hp = boss_info.max_hp

        self._is_game_over = False
        self._is_game_won = False

    def update(self, is_forward_pressed: bool, is_left_pressed: bool, is_down_pressed: bool, is_right_pressed: bool, is_attack_pressed: bool):
        player_egg = self._player_egg

        #game over state
        if player_egg.stats.current_hp <= 0:
            self._is_game_over = True

        if self._is_game_over or self._is_game_won:
            return
        
        #player movement, position and attack
        self.player_movement(is_forward_pressed, is_down_pressed, is_left_pressed, is_right_pressed)

        self.player_attack(is_attack_pressed)
            
        if self.is_out_of_bounds():
            self.return_to_bounds()

        #eggnemies/boss movement and spawn
        self.eggnemy_movement()
        self.eggnemy_spawn()

        self.boss_movement()
        
        if self._boss_spawn_rate - self._num_defeated_eggnemies == 0 and not self._boss_egg:
            print("spawning boss")
            self.boss_spawn()
            print("spawned boss")

        #damage
        if self._frame_count % self._fps == 0 and len(self._overlapping_player_eggnemy) > 0:
            self._player_egg.stats.current_hp -= 1 
        if self._frame_count % self._fps == 0  and self._boss_egg and self.is_overlapping_player(self._boss_egg):
            self._player_egg.stats.current_hp -= 3 


        #time and frame
        if self._frame_count % self._fps == 0:
            self._sec += 1
            if self._sec % 60 == 0:
                self._min += 1
                self._sec = 0

        self._frame_count += 1


        print(player_egg.center_position, player_egg.topmost_point, self._fps)


    def is_overlapping_player(self, eggnemy: Eggnemy | Boss):
        left_bounds = self._player_egg.leftmost_point
        right_bounds = self._player_egg.rightmost_point
        top_bounds = self._player_egg.topmost_point
        bottom_bounds = self._player_egg.bottom_point

        eggnemy_right = eggnemy.rightmost_point
        eggnemy_left = eggnemy.leftmost_point
        eggnemy_bottom = eggnemy.bottom_point
        eggnemy_top = eggnemy.topmost_point

        return not (left_bounds > eggnemy_right or 
                right_bounds < eggnemy_left or
                top_bounds > eggnemy_bottom or
                bottom_bounds < eggnemy_top)

    def is_out_of_bounds(self) -> bool:
        return (   
            self._player_egg.leftmost_point < 0 
            or self._player_egg.rightmost_point > self._world_width
            or self._player_egg.topmost_point < 0
            or self._player_egg.bottom_point > self._world_height 
        )

    def return_to_bounds(self):
        player_egg = self._player_egg
        assert self.is_out_of_bounds()
        
        if player_egg.leftmost_point < 0:
            player_egg.center_position.x = player_egg.stats.width / 2

        if player_egg.rightmost_point > self._world_width:
            player_egg.center_position.x = self._world_width - (player_egg.stats.width / 2)

        if player_egg.bottom_point > self._world_height:
            player_egg.center_position.y = self._world_height - (player_egg.stats.height / 2)

        if player_egg.topmost_point < 0:
            player_egg.center_position.y = player_egg.stats.height / 2
    
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
            radius = self._player_egg.player_attack_radius
            damage = self._player_egg.player_attack_damage

            for eggnemy in self._eggnemies:
                eggnemy_center = eggnemy.center_position
                
                #defeats eggnemy
                distance_to_player = ((self._player_egg.center_position.x - eggnemy_center.x) ** 2 + (self._player_egg.center_position.y - eggnemy_center.y) ** 2) ** 0.5
                if distance_to_player <= radius:
                    eggnemy.stats.current_hp -= damage

                    if eggnemy.stats.current_hp <= 0:
                        self._eggnemies.remove(eggnemy)
                        self._num_defeated_eggnemies += 1
                        if eggnemy in self._overlapping_player_eggnemy:
                            self._overlapping_player_eggnemy.remove(eggnemy)
            
            boss = self._boss_egg
            if boss:
                boss_distance_to_player = ((self._player_egg.center_position.x - boss.center_position.x) ** 2 + (self._player_egg.center_position.y - boss.center_position.y) ** 2) ** 0.5
                if boss_distance_to_player <= radius:
                    boss.stats.current_hp -= damage

                    if boss.stats.current_hp <= 0:
                        self._num_defeated_eggnemies += 1
                        self._boss_egg = None
                        self._is_game_won = True 
                        if boss in self._overlapping_player_eggnemy:
                            self._overlapping_player_eggnemy.remove(boss)
                

    def eggnemy_movement(self):
        for eggnemy in self._eggnemies:
            self.eggnemy_overlap_check(eggnemy)
            
            x_distance_to_player = self._player_egg.center_position.x - eggnemy.center_position.x
            y_distance_to_player = self._player_egg.center_position.y - eggnemy.center_position.y
            
            #follows player
            if not self._is_game_over:
                if x_distance_to_player < 0: #right of player
                    eggnemy.center_position.x -= eggnemy.stats.speed
                elif x_distance_to_player > 0: #left
                    eggnemy.center_position.x += eggnemy.stats.speed

                if y_distance_to_player < 0: #down
                    eggnemy.center_position.y -= eggnemy.stats.speed
                elif y_distance_to_player > 0: #up
                    eggnemy.center_position.y += eggnemy.stats.speed
                    
    def eggnemy_overlap_check(self, eggnemy: Eggnemy):
        is_overlap: bool = self.is_overlapping_player(eggnemy) 

        if is_overlap and eggnemy not in self._overlapping_player_eggnemy:
            self._overlapping_player_eggnemy.append(eggnemy)

        if not is_overlap and eggnemy in self._overlapping_player_eggnemy:
            self._overlapping_player_eggnemy.remove(eggnemy)

    def eggnemy_spawn(self):
        if len(self._eggnemies) <= self._eggnemy_count - 1:
            eggnemy_width = self._eggnemy_width
            eggnemy_height = self._eggnemy_height
            eggnemy_center = None
            while True:
                test_eggnemy_x = random.randint(eggnemy_width, self._world_width - eggnemy_width)
                test_eggnemy_y = random.randint(eggnemy_height, self._world_height - eggnemy_height)
                
                eggnemy_center = Point(test_eggnemy_x, test_eggnemy_y)
                eggnemy = Eggnemy(
                    EggInfo(
                        eggnemy_width,
                        eggnemy_height,
                        self._eggnemy_max_hp,
                        self._eggnemy_max_hp,
                        self.eggnemy_speed
                    ),
                    eggnemy_center,
                    )
                
                if not self.is_overlapping_player(eggnemy):
                    break
            self._eggnemies.append(eggnemy)

    def boss_spawn(self):
        boss_width = self._boss_width
        boss_height = self._boss_height
        boss_center = None
        while True:
            test_eggnemy_x = random.randint(boss_width, self._world_width - boss_width)
            test_eggnemy_y = random.randint(boss_height, self._world_height - boss_height)
            
            boss_center = Point(test_eggnemy_x, test_eggnemy_y)
            self._boss_egg = Boss(
                EggInfo(
                    boss_width,
                    boss_height,
                    self._boss_max_hp,
                    self._boss_max_hp,
                    self.boss_speed
                    ),
                boss_center,
                )
            if not self.is_overlapping_player(self._boss_egg):
                break
    
    def boss_movement(self):
        if self._boss_egg:
            x_distance_to_player = self._player_egg.center_position.x - self._boss_egg.center_position.x
            y_distance_to_player = self._player_egg.center_position.y - self._boss_egg.center_position.y
            
            #follows player
            if not self._is_game_over:
                if x_distance_to_player < 0: #right of player
                    self._boss_egg.center_position.x -= self._boss_speed
                elif x_distance_to_player > 0: #left
                    self._boss_egg.center_position.x += self._boss_speed
                if y_distance_to_player < 0: #down
                    self._boss_egg.center_position.y -= self._boss_speed
                elif y_distance_to_player > 0: #up
                    self._boss_egg.center_position.y += self._boss_speed


    @property
    def screen_width(self):
        return self._screen_width
    
    @property
    def screen_height(self):
        return self._screen_height

    @property
    def world_width(self):
        return self._world_width
    
    @property
    def world_height(self):
        return self._world_height

    @property
    def fps(self):
        return self._fps

    @property
    def frame_count(self):
        return self._frame_count
    
    @property
    def sec(self):
        return self._sec
    
    @property
    def min(self):
        return self._min

    @property
    def player_egg(self):
        return self._player_egg
    
    @property
    def eggnemies(self):
        return self._eggnemies
    
    @property
    def overlapping_player_eggnemy(self):
        return self._overlapping_player_eggnemy
    
    @property
    def num_defeated_eggnemies(self):
        return self._num_defeated_eggnemies
    
    @property
    def eggnemy_count(self):
        return self._eggnemy_count
    
    @property
    def eggnemy_width(self):
        return self._eggnemy_width
    
    @property
    def eggnemy_height(self):
        return self._eggnemy_height
    
    @property
    def eggnemy_speed(self):
        return self._eggnemy_speed

    @property
    def eggnemy_max_hp(self):
        return self._eggnemy_max_hp
    
    @property
    def boss_egg(self):
        return self._boss_egg
    
    @property
    def boss_spawn_rate(self):
        return self._boss_spawn_rate
    
    @property
    def boss_width(self):
        return self._boss_width
    
    @property
    def boss_height(self):
        return self._boss_height
    
    @property
    def boss_speed(self):
        return self._boss_speed
    
    @property
    def boss_max_hp(self):
        return self._boss_max_hp
    
    @property
    def is_game_over(self):
        return self._is_game_over
    
    @property
    def is_game_won(self):
        return self._is_game_won