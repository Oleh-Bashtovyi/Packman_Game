import pygame

from GameObjects import GameObject, Wall, Powerup, Entity, Apple
from GameState import GameState
from Position import Position


def test_position_manipulation():
    game_state = GameState(32, 4, 4)
    screen_position = game_state.translate_maze_to_screen((1, 2))
    some_object = GameObject(game_state, screen_position, 32)

    assert some_object.get_screen_position() == [32, 64]
    assert some_object.get_grid_position() == [1, 2]
    assert some_object.get_x() == 32
    assert some_object.get_y() == 64
    assert some_object.get_screen_center_position() == [48, 80]
    assert some_object.get_shape() == pygame.rect.Rect(32, 64, 32, 32)

    some_object.set_screen_position([48, 98])
    assert some_object.get_screen_position() == [48, 98]
    assert some_object.get_grid_position() == [2, 3]


def test_grid_position():
    game_state = GameState(32, 4, 4)
    screen_position = game_state.translate_maze_to_screen((1, 2))
    some_object = GameObject(game_state, screen_position, 32)
    assert some_object.get_grid_position() == [1, 2]

    some_object.set_screen_position((48, 72))
    assert some_object.get_grid_position() == [2, 2]
