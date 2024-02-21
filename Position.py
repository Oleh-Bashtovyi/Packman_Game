from typing import Union
import math


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def center_to(self, other: Union["Position", list, tuple]) -> "Position":
        return Position(self.x - other[0], self.y - other[1])

    def distance_to(self, other: Union["Position", list, tuple]):
        center = self.center_to(other)
        return math.sqrt(center.x ** 2 + center.y ** 2)

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
        elif isinstance(other, int):
            return Position(self.x + other, self.y + other)
        else:
            raise TypeError("Unsupported operand type")

    def __sub__(self, other):
        if isinstance(other, (Position, list, tuple)):
            if len(other) >= 2:
                return Position(self.x - other[0], self.y - other[1])
            else:
                raise ValueError("Input list or tuple must have exactly 2 elements")
        elif isinstance(other, int):
            return Position(self.x - other, self.y - other)
        else:
            raise TypeError("Unsupported operand type")

    def __mul__(self, scalar):
        return Position(self.x * scalar, self.y * scalar)

