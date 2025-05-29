from model import Model
from view import View
from controller import Controller
from project_types import Point, PlayerEgg
import json

with open('settings.json', 'r') as file:
    data = json.load(file)

def main():
    #Window Size
    window_width = data["worldWidth"]
    window_height = data["worldHeight"]
    fps = data["fps"]

    #Player Info
    egg_width = data["playerEggWidth"]
    egg_height = data["playerEggHeight"]
    egg_hp = data["playerEggHp"]
    egg_speed = data["playerEggSpeed"]

    player_egg = PlayerEgg(
        egg_height,
        egg_width,
        egg_hp,
        Point(window_width / 2, window_height / 2),
        egg_speed
    )

    #eggnemy Info
    eggnemy_count = data['eggnemyCount']
    eggnemy_width = data["eggnemyWidth"]
    eggnemy_height = data["eggnemyHeight"]
    eggnemy_speed = data["eggnemySpeed"]

    #MVC init
    model = Model(player_egg, fps, window_width, window_height, eggnemy_count, eggnemy_width, eggnemy_height, eggnemy_speed)
    view = View(model.window_width, model.window_height)
    controller = Controller(model, view)

    controller.start()

if __name__ == '__main__':
    main()
