import pytest
import pygame
from GameObjects import *
from Hero import *
from Ghosts import *
from GameState import *
from pygame import QUIT, K_UP
from GameObjects import GameObject, Position


@pytest.fixture
def game_state():
    return GameState(tile_size=32, maze_height=20, maze_width=20)

@pytest.fixture
def game_state():
    from GameState import GameState  
    return GameState(32, 10, 10)


def test_end_game(game_state):
    hero = Hero(game_state, Position(1, 1))  
    game_state.add_hero(hero)
    game_state.end_game()
    assert game_state.get_hero() == None

