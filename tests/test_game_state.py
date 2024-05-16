import pytest
from GameObjects import *
from Hero import *
from Ghosts import *
from GameState import *


@pytest.fixture
def game_state():
    return GameState(tile_size=32, maze_height=20, maze_width=20)

@pytest.fixture
def game_state():
    from GameState import GameState  
    return GameState(32, 10, 10)



