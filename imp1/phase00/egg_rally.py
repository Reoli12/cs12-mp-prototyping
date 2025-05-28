from model import Model
from view import View
from controller import Controller
from project_types import Point, PlayerEgg

def main():
    #Window Size
    window_width = 300
    window_height = 300

    #Player Info
    egg_height = 20
    egg_width = 10
    egg_hp = 10

    player_egg = PlayerEgg(
        egg_height,
        egg_width,
        egg_hp,
        Point(window_width / 2, window_height / 2)
    )

    #MVC init
    model = Model(player_egg, window_width, window_height)
    view = View(model.player_egg, model.window_width, model.window_height)
    controller = Controller(model, view)

    controller.start()

if __name__ == '__main__':
    main()
