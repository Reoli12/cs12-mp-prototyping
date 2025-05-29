from model import Model
from view import View
from controller import Controller
from project_types import Point, PlayerEgg, GameSettings
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

def main():
    #Game Settings
    fps = data["fps"]
    world_width = data["worldWidth"]
    world_height = data["worldHeight"]
    screen_width = data["screenWidth"]
    screen_height = data["screenHeight"]

    settings = GameSettings(
        fps,
        world_width,
        world_height,
        screen_width,
        screen_height
    )

    #Player Info
    egg_hp = data["playerEggHp"]
    egg_width = data["playerEggWidth"]
    egg_height = data["playerEggHeight"]
    egg_speed = data["playerEggSpeed"]
    egg_damage = data["playerAttackDamage"]
    egg_attack_radius = data["playerAttackRadius"]

    player_egg = PlayerEgg(
        egg_height,
        egg_width,
        egg_hp,
        Point(world_width / 2, world_height / 2),
        egg_speed,
        egg_damage,
        egg_attack_radius
    )

    #eggnemy Info
    eggnemy_initial_hp = data["eggnemInitialHp"]
    eggnemy_count = data["eggnemyInitialCount"]
    eggnemy_width = data["eggnemyWidth"]
    eggnemy_height = data["eggnemyHeight"]
    eggnemy_speed = data["eggnemySpeed"]

    #MVC init
    model = Model(player_egg, settings, eggnemy_count, eggnemy_width, eggnemy_height, eggnemy_speed, eggnemy_initial_hp)
    view = View(settings)
    controller = Controller(model, view)

    controller.start()

if __name__ == '__main__':
    main()
