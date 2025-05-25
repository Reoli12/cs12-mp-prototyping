import pyxel
from project_types import Egg

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
FPS = 30

EGG_HEIGHT = 20
EGG_WID = 10
EGG_HP = 10

EGG = Egg(EGG_HEIGHT, EGG_WID, EGG_HP, EGG_HP)

def update():
    ...

def draw():
    ...

pyxel.init(SCREEN_HEIGHT, SCREEN_WIDTH)
pyxel.run(update, draw)