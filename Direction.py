from enum import Enum, auto
from typing import Tuple


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

    def to_shift(self) -> Tuple[int, int]:
        if self == Direction.UP:
            return 0, -1
        elif self == Direction.DOWN:
            return 0, 1
        elif self == Direction.LEFT:
            return -1, 0
        elif self == Direction.RIGHT:
            return 1, 0
        return 0, 0

    def to_angle(self) -> int:
        if self == Direction.UP:
            return 90
        elif self == Direction.DOWN:
            return 270
        elif self == Direction.LEFT:
            return 180
        elif self == Direction.RIGHT:
            return 0
        return 0
