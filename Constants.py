from enum import Enum
from Position import *
import os

MAZE = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X            XX            X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXXPXXXXX XX XXXXXPXXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X                          X",
    "X XXXX XX XXXXXXXX XX XXXX X",
    "X XXXX XX XXXXXXXX XX XXXX X",
    "X      XX    XX    XX      X",
    "XXXXXX XXXXX XX XXXXX XXXXXX",
    "XXXXXX XXXXX XX XXXXX XXXXXX",
    "XXXXXX XX          XX XXXXXX",
    "XXXXXX XX XX XX XX XX XXXXXX",
    "XXXXXX XX XX    XX XX XXXXXX",
    "          XXXXXXXX          ",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX          XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "X            XX            X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X   XX                XX   X",
    "XXX XX XX XXXXXXXX XX XX XXX",
    "XXX XX XX XXXXXXXX XX XX XXX",
    "X      XX    XX    XX      X",
    "X XXXXXXXXXX XX XXXXXXXXXX X",
    "X XXXXXXXXXX XX XXXXXXXXXX X",
    "X   P                 P    X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

SCALE_FACTOR = 3
TILE_SIZE = 8 * SCALE_FACTOR
TILE_HALF = int(TILE_SIZE / 2)
GHOST_SIZE = TILE_SIZE
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
def __get_relative_image_path(filename):
    return os.path.join("images", filename)


RED_GHOST = __get_relative_image_path("ghost_red.png")
PINK_GHOST = __get_relative_image_path("ghost_pink.png")
BLUE_GHOST = __get_relative_image_path("ghost_blue.png")
ORANGE_GHOST = __get_relative_image_path("ghost_orange.png")
SCARED_GHOST = __get_relative_image_path("ghost_scared.png")
DEAD_GHOST = __get_relative_image_path("ghost_dead.png")
PACMAN_MOUTH_OPEN = __get_relative_image_path("pacman_open.png")
PACMAN_MOUTH_CLOSED = __get_relative_image_path("pacman_close.png")


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
