from Position import Position
from typing import Dict
from Direction import Direction
# дозволяє представити вузол у лабіринті та взаємодіяти з його сусідніми вузлами

class MazeNode:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._neighbours: Dict[Direction, MazeNode] = {}

    def get_walkable_positions(self) -> list[(Direction, Position)]:
        return [(direction, node.get_position()) for direction, node in self._neighbours.items()]

    def add_neighbour(self, direction: Direction, mazeNode: 'MazeNode'):
        self._neighbours[direction] = mazeNode

    def get_position(self):
        return Position(self._x, self._y)

class MazeController:
    def __init__(self):
        self.nodes: Dict[Position, MazeNode] = {}

    def add_node(self, position: Position):
        if position not in self.nodes:
            self.nodes[position] = MazeNode(position.x, position.y)

    def add_edge(self, from_position: Position, to_position: Position, direction: Direction):
        from_node = self.nodes.get(from_position)
        to_node = self.nodes.get(to_position)
        if from_node and to_node:
            from_node.add_neighbour(direction, to_node)

    def read_maze(self, maze):

        # створити вузли MazeNode
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                position = Position(x, y)
                self.add_node(position)

        # Заповнити вузли сусідами
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                position = Position(x, y)
                # додати телепорти
                if x == 0:
                    self.add_edge(position, Position(len(row)-1, y), Direction.LEFT)
                if x == len(row) - 1:
                    self.add_edge(position, Position(0, y), Direction.RIGHT)

                # звичайні напрями вліво\вправо\вгору\вниз
                if x > 0 and row[x - 1] != 'X':
                    self.add_edge(position, Position(x - 1, y), Direction.LEFT)
                if x < len(row) - 1 and row[x + 1] != 'X':
                    self.add_edge(position, Position(x + 1, y), Direction.RIGHT)
                if y > 0 and maze[y - 1][x] != 'X':
                    self.add_edge(position, Position(x, y - 1), Direction.UP)
                if y < len(maze) - 1 and maze[y + 1][x] != 'X':
                    self.add_edge(position, Position(x, y + 1), Direction.DOWN)

    def get_node_at_position(self, position: Position) -> MazeNode:
        return self.nodes.get(position)
