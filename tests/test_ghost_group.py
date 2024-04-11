import pytest

from Direction import Direction
from Ghosts import RedGhost, PinkGhost
from GameState import GameState
from Position import Position
from Hero import Hero
from MazeController import MazeController
from Ghosts import GhostGroup
from ModeController import ModeController
from Constants import GhostBehaviour
from main import fill_gamestate_with_static_objects
from tests.helpers import (do_nothing,
                           assert_all_ghosts_have_state,
                           assert_all_ghosts_have_screen_position,
                           assert_all_ghosts_have_direction)


@pytest.fixture(autouse=True)
def dummy_maze():
    return [
        "XXXXXXXXX",
        "X r     X",
        "X X X X X",
        "XhX X X X",
        "X   p   X",
        "XXXXXXXXX",
    ]


@pytest.fixture(autouse=True)
def dummy_game_state(dummy_maze):
    width = len(dummy_maze[0])
    height = len(dummy_maze)
    return GameState(32, width, height)


@pytest.fixture(autouse=True)
def dummy_game_state_with_objects(dummy_game_state, dummy_maze):
    game_state = dummy_game_state
    fill_gamestate_with_static_objects(game_state, dummy_maze)
    return game_state


@pytest.fixture(autouse=True)
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

    red_mode_controller = ModeController(10, 20, 10, GhostBehaviour.SCATTER)
    pink_mode_controller = ModeController(10, 20, 10, GhostBehaviour.SCATTER)
    ghost_group.add_ghost(RedGhost(game_state, red_screen_pos, red_spawn_pos, red_scatter_pos,
                                   game_state.TILE_SIZE, red_mode_controller, pacmen))
    ghost_group.add_ghost(PinkGhost(game_state, pink_screen_pos, pink_spawn_pos, pink_scatter_pos,
                                    game_state.TILE_SIZE, pink_mode_controller, pacmen))
    game_state.set_ghost_group(ghost_group)
    return game_state


def test_ghosts_state_on_start(dummy_game_state_with_entities_and_objects):
    game_state = dummy_game_state_with_entities_and_objects
    assert_all_ghosts_have_state(game_state.get_ghost_group(), GhostBehaviour.SCATTER)
    assert len(game_state.get_ghost_group().get_ghosts()) == 2


def test_monkey_patch_test(dummy_game_state_with_entities_and_objects, monkeypatch):
    game_state = dummy_game_state_with_entities_and_objects
    use_monkeypatch_on_ghosts(monkeypatch, game_state.get_ghost_group(),
                              "move_in_current_direction", None)
    for ghost in game_state.get_ghost_group().get_ghosts():
        assert ghost.move_in_current_direction is None


def test_ghosts_state_2(dummy_game_state_with_entities_and_objects, monkeypatch):
    game_state = dummy_game_state_with_entities_and_objects
    ghost_group = game_state.get_ghost_group()
    use_monkeypatch_on_ghosts(monkeypatch, ghost_group,
                              "move_in_current_direction", do_nothing)
    assert_all_ghosts_have_state(ghost_group, GhostBehaviour.SCATTER)

    positions = [ghost.get_screen_position() for ghost in ghost_group.get_ghosts()]

    ghost_group.tick(8)
    assert_all_ghosts_have_state(ghost_group, GhostBehaviour.SCATTER)
    assert_all_ghosts_have_screen_position(ghost_group, positions)

    ghost_group.tick(2)
    assert_all_ghosts_have_state(ghost_group, GhostBehaviour.CHASE)
    assert_all_ghosts_have_direction(ghost_group, Direction.LEFT)


def use_monkeypatch_on_ghosts(monkeypatch, ghost_group: GhostGroup, attribute: str, value):
    for ghost in ghost_group.get_ghosts():
        monkeypatch.setattr(ghost, attribute, value)
