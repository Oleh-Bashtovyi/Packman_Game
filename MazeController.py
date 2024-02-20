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



class MazeController:
     def __init__(self):
        self.numpy_maze = []
        self.cookie_spaces = []
        self.powerup_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []
        self.size = (0, 0)
        self.convert_maze_to_numpy()
        self.p = Pathfinder(self.numpy_maze)
        self.nodes: Dict[Tuple[int, int], MazeNode] = {}


     def add_node(self, position: Position):
        if position not in self.nodes:
            self.nodes[position] = MazeNode(position.x, position.y)

     def add_edge(self, position1: Position, position2: Position, direction: Direction):
        node1 = self.nodes.get(position1)
        node2 = self.nodes.get(position2)
        if node1 and node2:
            node1.add_neighbour(direction, node2)
            opposite_direction = self.opposite(direction)
            node2.add_neighbour(opposite_direction, node1)


     def read_maze(self, maze: List[str]):
        for y, row in maze:
            for x, cell in row:
                position = Position(x, y)
                self.add_node(position)
                if (x > 0 and row[x-1] != 'X'):
                    self.add_edge(position, Position(x - 1, y), Direction.LEFT)
                if (x < len(row) - 1 and row[x+1] != 'X'):
                    self.add_edge(position, Position(x + 1, y), Direction.RIGHT)
                if (y > 0 and maze[y-1, x] != 'X'): 
                    self.add_edge(position, Position(x, y - 1), Direction.UP)
                if (y < len(maze) - 1 and maze[y+1, x] != 'X'):
                    self.add_edge(position, Position(x, y + 1), Direction.DOWN)

     def get_node_at_position(self, position: Position) -> MazeNode:
       return self.nodes.get(position)
