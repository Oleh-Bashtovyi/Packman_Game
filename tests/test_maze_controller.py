import pytest
from MazeController import MazeController, MazeNode, Direction, Position

@pytest.fixture
def empty_maze_controller():
    return MazeController()

@pytest.fixture
def maze_controller_with_nodes():
    controller = MazeController()
    controller.add_node(Position(0, 0))
    controller.add_node(Position(1, 0))
    controller.add_node(Position(0, 1))
    return controller

def test_get_walkable_positions():
    node1 = MazeNode(0, 0)
    node2 = MazeNode(1, 0)
    node3 = MazeNode(0, 1)
    node1.add_neighbour(Direction.RIGHT, node2)
    node1.add_neighbour(Direction.DOWN, node3)

    expected_positions = [(Direction.RIGHT, Position(1, 0)), (Direction.DOWN, Position(0, 1))]
    assert node1.get_walkable_positions() == expected_positions

def test_get_position():
    node = MazeNode(3, 4)
    assert node.get_position() == Position(3, 4)

def test_node_creation():
    node = MazeNode(2, 3)
    assert node.get_position() == Position(2, 3)

def test_add_neighbour():
    node1 = MazeNode(0, 0)
    node2 = MazeNode(1, 0)
    node1.add_neighbour(Direction.RIGHT, node2)
    assert node1._neighbours[Direction.RIGHT] == node2

def test_add_node(empty_maze_controller):
    empty_maze_controller.add_node(Position(2, 3))
    assert Position(2, 3) in empty_maze_controller.nodes

def test_add_edge(maze_controller_with_nodes):
    maze_controller_with_nodes.add_edge(Position(0, 0), Position(1, 0), Direction.RIGHT)
    assert maze_controller_with_nodes.nodes[Position(0, 0)]._neighbours[Direction.RIGHT]

def test_read_maze():
    controller = MazeController()
    maze = [
        ['.', '.', '.'],
        ['X', 'X', '.'],
        ['.', '.', '.']
    ]
    controller.read_maze(maze)
    assert Position(0, 0) in controller.nodes
    assert Position(2, 2) in controller.nodes
    assert controller.nodes[Position(0, 0)]._neighbours.get(Direction.RIGHT) is not None
    assert controller.nodes[Position(0, 0)]._neighbours.get(Direction.DOWN) is None

def test_get_node_at_position(maze_controller_with_nodes):
    assert maze_controller_with_nodes.get_node_at_position(Position(0, 0)).get_position() == Position(0, 0)
    assert maze_controller_with_nodes.get_node_at_position(Position(1, 0)).get_position() == Position(1, 0)
    assert maze_controller_with_nodes.get_node_at_position(Position(0, 1)).get_position() == Position(0, 1)
    assert maze_controller_with_nodes.get_node_at_position(Position(2, 2)) is None

