from unittest.mock import MagicMock
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

def test_draw(hero):
    initial_image = hero._entity_image
    hero.draw()
    assert hero._entity_image != initial_image

def test_handle_cookie_pickup_empty(hero, game_state):
    initial_score = game_state._score
    hero.handle_cookie_pickup()
    assert initial_score == game_state._score





