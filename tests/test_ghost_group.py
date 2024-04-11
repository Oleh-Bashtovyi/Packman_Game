import pytest

import Constants
from Ghosts import RedGhost, PinkGhost
from GameState import GameState
from Position import Position
from Hero import Hero
from MazeController import MazeController
from Ghosts import GhostGroup
from tests.test_helpers import almost_equal, controller_has_state_and_time_left
from ModeController import ModeController
from Constants import GhostBehaviour
from main import fill_gamestate_with_static_objects


@pytest.fixture
def dummy_maze():
    return [
        "XXXXXXXXX",
        "X r     X",
        "X X X X X",
        "XhX X X X",
        "X   p   X",
        "XXXXXXXXX",
    ]


@pytest.fixture
def dummy_game_state(dummy_maze):
    width = len(dummy_maze[0])
    height = len(dummy_maze)
    return GameState(32, width, height)


@pytest.fixture
def dummy_game_state_with_objects(dummy_game_state, dummy_maze):
    game_state = dummy_game_state
    fill_gamestate_with_static_objects(game_state, dummy_maze)
    return game_state


@pytest.fixture
def dummy_game_state_with_entities_and_objects(dummy_game_state_with_objects, dummy_maze):
    game_state = dummy_game_state_with_objects
    maze = dummy_maze
    maze_controller = MazeController()
    maze_controller.read_maze(maze)
    ghost_group = GhostGroup(game_state, maze_controller)
    for i, row in enumerate(maze):
        for j, column in enumerate(row):
            screen_pos = game_state.translate_maze_to_screen((j, i))
            if maze[i][j] == "h":
                pacmen = Hero(game_state, screen_pos, game_state.TILE_SIZE)
                game_state.add_hero(pacmen)
            elif maze[i][j] == "r":
                red_screen_pos = screen_pos
                red_spawn_pos = Position(j, i)
                red_scatter_pos = Position(0, 0)
            elif maze[i][j] == "p":
                pink_screen_pos = screen_pos
                pink_spawn_pos = Position(j, i)
                pink_scatter_pos = Position(0, 5)

    ghost_group.add_ghost(RedGhost(game_state, red_screen_pos, red_spawn_pos, red_scatter_pos,
                                   game_state.TILE_SIZE,  pacmen))
    ghost_group.add_ghost(PinkGhost(game_state, pink_screen_pos, pink_spawn_pos, pink_scatter_pos,
                                    game_state.TILE_SIZE, pacmen))
    game_state.set_ghost_group(ghost_group)
    return game_state


def test_ghosts_position(dummy_game_state_with_entities_and_objects, monkeypatch):
    game_state = dummy_game_state_with_entities_and_objects
    assert_all_ghosts_have_state(game_state.get_ghost_group(), GhostBehaviour.SCATTER)
    assert len(game_state.get_ghost_group().get_ghosts()) == 2


def assert_all_ghosts_have_state(ghost_group: GhostGroup, state: GhostBehaviour):
    ghosts = ghost_group.get_ghosts()
    for ghost in ghosts:
        assert ghost.get_current_state() == state
