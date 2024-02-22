from enum import Enum
from Position import *

MAZE = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP           XX            X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXXOXXXXX XX XXXXXOXXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X                          X",
    "X XXXX XX XXXXXXXX XX XXXX X",
    "X XXXX XX XXXXXXXX XX XXXX X",
    "X      XX    XX    XX      X",
    "XXXXXX XXXXX XX XXXXX XXXXXX",
    "XXXXXX XXXXX XX XXXXX XXXXXX",
    "XXXXXX XX     G    XX XXXXXX",
    "XXXXXX XX XXX  XXX XX XXXXXX",
    "XXXXXX XX X      X XX XXXXXX",
    "   G      X      X          ",
    "XXXXXX XX X      X XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX    G     XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "X            XX            X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X   XX       G        XX   X",
    "XXX XX XX XXXXXXXX XX XX XXX",
    "XXX XX XX XXXXXXXX XX XX XXX",
    "X      XX    XX    XX      X",
    "X XXXXXXXXXX XX XXXXXXXXXX X",
    "X XXXXXXXXXX XX XXXXXXXXXX X",
    "X   O                 O    X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

SCALE_FACTOR = 3
TILE_SIZE = 8 * SCALE_FACTOR
TILE_HALF = int(TILE_SIZE / 2)
GHOST_SIZE = int(TILE_SIZE * (3 / 4))
PACMAN_SIZE = int(TILE_SIZE)
MAZE_WIDTH = len(MAZE[0])
MAZE_HEIGHT = len(MAZE)
SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * TILE_SIZE
APPLE_SIZE = int(TILE_SIZE / 6)
POWERUP_SIZE = int(TILE_SIZE / 4)

# Ghost behaviour
SCATTER_TIME = 7
CHASE_TIME = 20
FRIGHT_TIME = 10

# Colors
WALL_COLOR = (0, 0, 255)
APPLE_COLOR = (255, 255, 0)
POWERUP_COLOR = (255, 255, 255)

# Images
RED_GHOST = "images/ghost_red.png"
PINK_GHOST = "images/ghost_pink.png"
BLUE_GHOST = "images/ghost_blue.png"
ORANGE_GHOST = "images/ghost_orange.png"
SCARED_GHOST = "images/ghost_scared.png"
DEAD_GHOST = "images/ghost_dead.png"


class ScoreType(Enum):
    APPLE = 10
    POWERUP = 50
    GHOST = 400


class GhostBehaviour(Enum):
    CHASE = 1
    SCATTER = 2
    FRIGHT = 3
    SPAWN = 4


def translate_screen_to_maze(coordinates: Position | tuple[int, int]):
    return Position(int(coordinates[0] / TILE_SIZE), int(coordinates[1] / TILE_SIZE))


def translate_maze_to_screen(coordinates):
    return Position(coordinates[0] * TILE_SIZE, coordinates[1] * TILE_SIZE)
