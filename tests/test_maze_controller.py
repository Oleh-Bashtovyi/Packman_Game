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


