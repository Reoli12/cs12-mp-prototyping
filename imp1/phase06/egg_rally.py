from model import Model
from view import View
from controller import Controller
from project_types import Point, PlayerEgg, EggInfo, GameSettings, EgghancementSettings
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

def main():
    #Game Settings
    fps: int = data["fps"]
    world_width: int = data["worldWidth"]
    world_height: int = data["worldHeight"]
    screen_width: int = data["screenWidth"]
    screen_height: int = data["screenHeight"]

    settings = GameSettings(
        fps,
        world_width,
        world_height,
        screen_width,
        screen_height
    )

    #Player Info
    egg_hp: int = data["playerEggHp"]
    egg_width: int = data["playerEggWidth"]
    egg_height: int = data["playerEggHeight"]
    egg_speed: int = data["playerEggSpeed"]
    egg_damage: int = data["playerAttackDamage"]
    egg_attack_radius: int = data["playerAttackRadius"]

    player_egg = PlayerEgg(
        EggInfo(
            egg_width,
            egg_height,
            egg_hp,
            egg_hp,
            egg_damage,
            egg_speed
        ),
        Point(world_width / 2, world_height / 2),
        egg_attack_radius
    )

    #eggnemy Info
    eggnemy_hp: int = data["eggnemInitialHp"]
    eggnemy_count: int = data["eggnemyInitialCount"]
    eggnemy_width: int = data["eggnemyWidth"]
    eggnemy_height: int = data["eggnemyHeight"]
    eggnemy_speed: int = data["eggnemySpeed"]

    eggnemy_info = EggInfo(
        eggnemy_width,
        eggnemy_height,
        eggnemy_hp,
        eggnemy_hp,
        1,
        eggnemy_speed
    )

    #boss Info
    boss_spawn_rate: int = data["bossSpawnRate"]
    boss_hp: int = data["bossInitialHp"]
    boss_width: int = data["bossWidth"]
    boss_height: int = data["bossHeight"]
    boss_speed: int = data["bossSpeed"]

    boss_info = EggInfo(
        boss_width,
        boss_height,
        boss_hp,
        boss_hp,
        3,
        boss_speed
    )

    #Egghancement Settings
    egghancementNeededXp: int = data["egghancementNeededXp"]
    maxHpEgghancement: int = data["maxHpEgghancement"]
    atkEgghancement: int = data["attackEgghancement"]
    spdEgghancement: int = data["speedEgghancement"]

    egghancement = EgghancementSettings(
        egghancementNeededXp,
        maxHpEgghancement,
        atkEgghancement,
        spdEgghancement
    )

    #MVC init
    model: Model = Model(player_egg, settings, eggnemy_count, eggnemy_info, boss_info, boss_spawn_rate, egghancement)
    view: View = View(settings)
    controller: Controller = Controller(model, view)

    controller.start()

if __name__ == '__main__':
    main()
