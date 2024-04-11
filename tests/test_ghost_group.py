import pytest

from GameState import GameState
from main import fill_gamestate
from Position import Position
from Hero import Hero
from MazeController import MazeController
from Ghosts import GhostGroup
from tests.test_helpers import almost_equal, controller_has_state_and_time_left
from ModeController import ModeController
from Constants import GhostBehaviour


@pytest.fixture
def dummy_maze():
    return [
        "XXXXXXXXX",
        "X       X",
        "X X X X X",
        "X X X X X",
        "X       X",
        "XXXXXXXXX",
    ]


@pytest.fixture
def dummy_maze_tile_size():
    return 32


@pytest.fixture
def game_state_arguments_for_dummy_maze(dummy_maze_tile_size, dummy_maze):
    maze = dummy_maze
    width = len(dummy_maze[0])
    height = len(dummy_maze)
    return dummy_maze_tile_size, width, height


@pytest.fixture
def dummy_maze_ghosts_scatter_position(game_state_arguments_for_dummy_maze):
    _, width, height = game_state_arguments_for_dummy_maze
    width -= 1
    height -= 1
    return Position(0, 0), Position(width, 0), Position(0, height), Position(width, height)


@pytest.fixture
def dummy_maze_ghsot_spawn_position(dummy_maze_ghosts_scatter_position):
    left_up, right_up, left_down, right_down = dummy_maze_ghosts_scatter_position
    left_up += [2, 1]
    right_up += [-2, 1]
    left_down += [2, -1]
    right_down += [-2, -1]
    return left_up, right_up, left_down, right_down


@pytest.fixture
def dummy_game_state(game_state_arguments_for_dummy_maze, dummy_maze):
    tile_size, width, height = game_state_arguments_for_dummy_maze
    game_state = GameState(tile_size, height, width)
    fill_gamestate(game_state, dummy_maze)
    return game_state


@pytest.fixture
def dummy_game_state_with_ghost_group(dummy_game_state,
                                     dummy_maze,
                                     dummy_maze_tile_size,
                                     dummy_maze_ghosts_scatter_position,
                                     dummy_maze_ghsot_spawn_position):
    game_state = dummy_game_state
    red_sct, purple_sct, blue_sct, orange_sct = dummy_maze_ghosts_scatter_position
    red_spn, purple_spn, blue_spn, ornage_spn = dummy_maze_ghsot_spawn_position
    packman = Hero(game_state, Position(3, 2), dummy_maze_tile_size)
    controller = MazeController()
    controller.read_maze(dummy_maze)
    ghost_group = GhostGroup(game_state, packman, dummy_maze_tile_size, controller,
                             red_spn, red_sct, purple_spn, purple_sct,
                             blue_spn, blue_sct, ornage_spn, orange_sct)
    game_state.set_ghost_group(ghost_group)
    return game_state


def test_ghosts_position(dummy_game_state_with_ghost_group):
    game_state = dummy_game_state_with_ghost_group
    assert_all_ghosts_have_state(game_state.get_ghost_group(), GhostBehaviour.SCATTER)


def assert_all_ghosts_have_state(ghsot_group: GhostGroup, state: GhostBehaviour):
    ghosts = ghsot_group.get_ghosts()
    for ghost in ghosts:
        assert  ghost.get_current_state() == state