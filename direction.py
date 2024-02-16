class Direction(Enum):
    RIGHT = 0
    UP = 90
    LEFT = 180
    DOWN = 270
    NONE = 360

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

    def __eq__(self, other):
        if isinstance(other, Direction):
            return self.value == other.value
        return False

