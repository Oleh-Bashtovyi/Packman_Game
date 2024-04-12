import pygame
import pytest

from Constants import GhostBehaviour, RED_GHOST
from GameObjects import GameObject, Wall, Powerup, Entity
from GameState import GameState
from Ghosts import RedGhost, Ghost, GhostGroup
from Hero import Hero
from MazeController import MazeController
from ModeController import ModeController
from Position import Position
from Direction import Direction
from main import fill_gamestate_with_static_objects
import random

@pytest.fixture(autouse=True)
def default_game_state_and_ghost():
    maze = ["h    ",
            " XgX ",
            " X X ",
            "     "]
    game_state = GameState(4, 5, 5)
    fill_gamestate_with_static_objects(game_state, maze)

    pacmen = Hero(game_state, Position(0, 0), 4)
    mode_controller = ModeController(10, 20, 10, GhostBehaviour.SCATTER)
    ghost = Ghost(game_state,
                  game_state.translate_maze_to_screen((2, 1)),
                  Position(2, 1),
                  Position(4, 0), 4, mode_controller, pacmen, entity_image=RED_GHOST)
    maze_controller = MazeController()
    maze_controller.read_maze(maze)
    ghost_group = GhostGroup(game_state, maze_controller)
    ghost_group.add_ghost(ghost)
    game_state.set_ghost_group(ghost_group)
    return game_state


def test_tick(default_game_state_and_ghost):
    game_state = default_game_state_and_ghost
    ghost = game_state.get_ghost_group().get_ghosts()[0]
    assert ghost.get_screen_position() == [8, 4]
    assert ghost.get_current_direction() == Direction.NONE
    ghost.start_chase()

    for i in range(4):
        game_state.get_ghost_group().tick(1)

    assert ghost.get_grid_position() == [2, 0]
    assert ghost.get_screen_position() == [8, 0]


def test_freight_state(default_game_state_and_ghost, monkeypatch):
    game_state = default_game_state_and_ghost
    ghost = game_state.get_ghost_group().get_ghosts()[0]
    ghost.set_screen_position([8, 0])
    assert ghost.get_current_direction() == Direction.NONE
    monkeypatch.setattr(random, "random", lambda: 2)
    assert random.random() == 2
    monkeypatch.setattr(random, "choice", lambda choices: choices[1])
    assert random.choice([1, 5, 2]) == 5

    maze_controller = game_state.get_ghost_group().maze_controller
    expected_direction = (maze_controller.get_node_at_position(Position(2, 0)).get_walkable_positions())[1][0]

    ghost.start_fright()
    ghost.tick(1)

    assert ghost.get_current_direction() == expected_direction
    assert ghost.get_current_state() == GhostBehaviour.FRIGHT


# def assert_has_screen_position(obj: GameObject, expected_pos: tuple|list|Position):
#     pos = obj.get_screen_position()
#     assert pos.x == expected_pos[0]
#     assert pos.y == expected_pos[1]
#
#
# def assert_has_grid_position(obj: GameObject, expected_pos: tuple|list|Position):
#     pos = obj.get_grid_position()
#     assert pos.x == expected_pos[0]
#     assert pos.y == expected_pos[1]