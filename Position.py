from typing import Union
import math


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def center_to(self, other: Union["Position", list, tuple]) -> "Position":
        """
        Calculate center of two position (vectors) using formula: (Vect2 - Vect1)
        :param other: other position or tuple with 2 elements
        :return:
        """
        return Position(self.x - other[0], self.y - other[1])

    def distance_to(self, other: Union["Position", list, tuple]):
        """
        Calculate distance between two positions.
        :param other: Position or tuple with 2 elements
        :return:
        """
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
        if isinstance(scalar, (Position, list, tuple)):
            if len(scalar) >= 2:
                return self.x * scalar[0] + self.y * scalar[1]
            elif len(scalar) == 1:
                return self.x * scalar[0] + self.y * scalar[0]
            else:
                return Position(self.x, self.y)
        return Position(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        if isinstance(other, (Position, list, tuple)):
            if len(other) == 2:
                return self.x == other[0] and self.y == other[1]
        return False

    def __hash__(self):
        return hash((self.x, self.y))
