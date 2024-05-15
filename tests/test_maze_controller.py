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

