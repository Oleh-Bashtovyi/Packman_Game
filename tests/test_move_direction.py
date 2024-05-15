from unittest.mock import MagicMock
from GameObjects import Entity
from Direction import Direction
from Constants import ScoreType, GhostBehaviour, PACMAN_SIZE, PACMAN_MOUTH_OPEN, PACMAN_MOUTH_CLOSED
from Position import Position
from Hero import Hero 
from GameState import GameState
import pytest

@pytest.fixture
def game_state():
    tile_size = 10  
    maze_height = 20  
    maze_width = 30  
    return GameState(tile_size, maze_height, maze_width)

@pytest.fixture
def hero(game_state):
    hero = Hero(game_state, Position(0, 0))
    hero._renderer = MagicMock()
    return hero

def test_try_move_in_direction_collision(hero):
    prev_position = hero.get_screen_position()
    hero.collides_with_wall = lambda: True
    hero._try_move_in_direction(Direction.UP)
    assert hero.get_screen_position() == prev_position

def test_try_move_in_direction_no_collision(hero):
    prev_position = hero.get_screen_position()
    hero.collides_with_wall = lambda: False
    hero._try_move_in_direction(Direction.UP)
    assert hero.get_screen_position() != prev_position

def test_set_direction(hero):
    hero.set_direction(Direction.DOWN)
    assert hero.buffer_direction == Direction.DOWN


