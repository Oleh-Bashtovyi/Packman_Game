from typing import List
from enum import Enum, auto

SCALE_FACTOR = 3
TILE_SIZE = 8 * SCALE_FACTOR
APPLE_SIZE = int(TILE_SIZE / 4)
POWERUP_SIZE = int(TILE_SIZE / 3)
WALL_COLOR = (0, 0, 255)
APPLE_COLOR = (255, 255, 0)
POWERUP_COLOR = (255, 255, 255)


class Direction(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def opposite(self):
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.LEFT
        return Direction.NONE


DIRECTION_DICT = {
    Direction.NONE: [0, 0],
    Direction.LEFT: [-1, 0],
    Direction.RIGHT: [1, 0],
    Direction.DOWN: [0, 1],
    Direction.UP: [0, -1]
}


def get_direction_shift(direction: Direction) -> list[int]:
    return DIRECTION_DICT[direction]
