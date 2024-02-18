from enum import Enum

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

# Colors
WALL_COLOR = (0, 0, 255)
APPLE_COLOR = (255, 255, 0)
POWERUP_COLOR = (255, 255, 255)

# Images
RED_GHOST = "images/redghost.png"
PINK_GHOST = "images/redghost.png"
BLUE_GHOST = "images/redghost.png"
ORANGE_GHOST = "images/redghost.png"
SCARED_GHOST = "images/redghost.png"
DEAD_GHOST = "images/redghost.png"


class ScoreType(Enum):
    APPLE = 10
    POWERUP = 50
    GHOST = 400


class GhostBehaviour(Enum):
    CHASE = 1
    SCATTER = 2
    FREIGHT = 3
    SPAWN = 4
