import pygame
import pytest

from GameObjects import GameObject, Wall, Powerup, Entity
from GameState import GameState
from Position import Position
from Direction import Direction


@pytest.fixture(autouse=True)
def default_game_state_and_entity():
    game_state = GameState(32, 4, 4)
    screen_pos = game_state.translate_maze_to_screen((1, 1))
    entity = Entity(game_state, screen_pos, 32)
    return game_state, entity


def test_get_set_directions(default_game_state_and_entity):
    game_state, entity = default_game_state_and_entity
    assert entity.get_current_direction() == Direction.NONE

    entity.set_current_direction(Direction.RIGHT)
    assert entity.get_current_direction() == Direction.RIGHT

    entity.set_current_direction(Direction.LEFT)
    assert entity.get_current_direction() == Direction.LEFT


def test_move_in_direction(default_game_state_and_entity):
    game_state, entity = default_game_state_and_entity
    entity.set_current_direction(Direction.LEFT)
    assert entity.get_current_direction() == Direction.LEFT
    entity.set_screen_position((32, 32))

    entity.move_in_current_direction()
    assert entity.get_screen_position() == [31, 32]
    entity.move_in_direction(Direction.RIGHT)
    assert entity.get_screen_position() == [32, 32]


def test_handle_teleport_left(default_game_state_and_entity):
    game_state, entity = default_game_state_and_entity
    entity.set_screen_position((0, 32))
    entity.set_current_direction(Direction.LEFT)
    entity.handle_teleport()
    assert entity.get_screen_position() == [0, 32]

    for i in range(16):
        entity.move_in_current_direction()

    entity.handle_teleport()
    assert entity.get_screen_position() == [-16, 32]
    entity.move_in_current_direction()
    entity.handle_teleport()
    assert entity.get_screen_position() == [game_state.SCREEN_WIDTH - 16, 32]


def test_handle_teleport_right():
    game_state = GameState(32, 3, 3)
    screen_pos = game_state.translate_maze_to_screen((2, 1))
    entity = Entity(game_state, screen_pos, 32)
    entity.set_current_direction(Direction.RIGHT)
    entity.handle_teleport()
    assert entity.get_screen_position() == [64, 32]

    for i in range(16):
        entity.move_in_current_direction()

    entity.handle_teleport()
    assert entity.get_screen_position() == [80, 32]
    entity.move_in_current_direction()
    entity.handle_teleport()
    pos = entity.get_screen_position()
    assert pos.x == -16


def test_collide_with_walls(default_game_state_and_entity):
    game_state, entity = default_game_state_and_entity
    entity.set_screen_position((32, 32))
    wall_1 = Wall(game_state, game_state.translate_maze_to_screen((0, 1)))
    wall_2 = Wall(game_state, game_state.translate_maze_to_screen((1, 0)))
    game_state.add_wall(wall_1)
    game_state.add_wall(wall_2)
    assert entity.collides_with_wall() is False

    entity.move_in_direction(Direction.UP)
    assert entity.collides_with_wall() is True
