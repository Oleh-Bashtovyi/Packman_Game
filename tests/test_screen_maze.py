import pytest
import pygame
from GameObjects import *
from Hero import *
from Ghosts import *
from GameState import *
from GameObjects import Position
from Constants import *


@pytest.fixture
def game_state():
    return GameState(tile_size=32, maze_height=20, maze_width=20)

@pytest.fixture
def game_state():
    from GameState import GameState  
    return GameState(32, 10, 10)

def test_translate_screen_to_maze(game_state):
    assert game_state.translate_screen_to_maze((64, 64)) == Position(2, 2)



def test_translate_maze_to_screen(game_state):
    assert game_state.translate_maze_to_screen((2, 2)) == Position(64, 64)