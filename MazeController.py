from Position import Position
from typing import Dict, Tuple, List
from  Direction import Direction


class MazeNode:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._neighbours: Dict[Direction, MazeNode] = {}

    def get_walkable_positions(self) -> List[(Direction, Position)]:
        return [(direction, node.get_position()) for direction, node in self._neighbours.items()]

    def add_neighbour(self, direction: Direction, mazeNode: 'MazeNode'):
        self._neighbours[direction] = mazeNode

    def get_position(self):
        return Position(self._x, self._y)



# TODO
# FINISH MAZE CONTROLLER
# - OLEH says:
# - контролер повинен зчитувати лабіринт і перетворювати кожну клітину в ньому на Node.
# - Node має сусідів, тобто клітини на які ми можемо перейти з цього нода.
#   Це потрібно для привидів, щоб вони знали, на які позиції можуть перейти.
# - Ваше завдання написати алгоритм зчитування, створення і заповнення сусідів нодів.
# - Думаю цей контролер має бути десь в gameState.
#   В gameState хай зберігається в змінній self.mazeController
class MazeController:
    def __init__(self):
        self.something = 1

    def get_node_at_position(self, position: Position):
        pass
