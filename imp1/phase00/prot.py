import pyxel
from project_types import Egg, Point

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
FPS = 30

EGG_HEIGHT = 20
EGG_WID = 10
EGG_HP = 10

EGG = Egg(EGG_HEIGHT, EGG_WID, EGG_HP, EGG_HP, Point(SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2))

def update():
    if pyxel.btn(pyxel.KEY_W):
        EGG.center_position.y -= 2

    if pyxel.btn(pyxel.KEY_A):
        EGG.center_position.x -= 2

    if pyxel.btn(pyxel.KEY_S):
        EGG.center_position.y += 2  

    if pyxel.btn(pyxel.KEY_D):
        EGG.center_position.x += 2

    if is_out_of_bounds(EGG):
        return_to_within_bounds(EGG)
    print(EGG.center_position, EGG.topmost_point)

def draw():
    pyxel.cls(0)

    pyxel.rect(
        EGG.center_position.x - EGG.width / 2,
        EGG.center_position.y - EGG.height / 2,
        EGG_WID,
        EGG_HEIGHT,
        5
    )

def is_out_of_bounds(egg: Egg) -> bool:
    return (   egg.leftmost_point < 0 
            or egg.rightmost_point < 0
            or egg.rightmost_point > SCREEN_WIDTH
            or egg.bottom_point > SCREEN_HEIGHT )

def return_to_within_bounds(egg: Egg):
    assert is_out_of_bounds(egg)     

    if egg.leftmost_point < 0:
        egg.center_position.x = egg.width / 2
    if egg.rightmost_point > SCREEN_WIDTH:
        egg.center_position.x = SCREEN_WIDTH - (egg.width / 2)
    if egg.bottom_point > SCREEN_HEIGHT:
        print('below bottom bound')
        egg.center_position.y = SCREEN_HEIGHT - (egg.height / 2)
    if egg.topmost_point < 0:
        print('above top bound')
        egg.center_position.y = egg.height / 2


pyxel.init(SCREEN_HEIGHT, SCREEN_WIDTH)
pyxel.run(update, draw)