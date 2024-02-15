from typing import Union
import math

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other: Union["Position", list, tuple]):
        return math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __add__(self, other):
        if isinstance(other, (Position, list, tuple)):
            if len(other) >= 2:
                return Position(self.x + other[0], self.y + other[1])
            else:
                raise ValueError("Input list or tuple must have exactly 2 elements")
        else:
            raise TypeError("Unsupported operand type")
