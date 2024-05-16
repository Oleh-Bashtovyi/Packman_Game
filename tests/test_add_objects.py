import pytest
from GameObjects import *
from Hero import *
from Ghosts import *
from GameState import *
from GameObjects import GameObject, Position


@pytest.fixture
def game_state():
    return GameState(tile_size=32, maze_height=20, maze_width=20)

@pytest.fixture
def game_state():
    from GameState import GameState  
    return GameState(32, 10, 10)

def test_add_game_object(game_state):
    obj_size = 10  
    obj = GameObject(game_state, Position(1, 1), obj_size)  
    game_state.add_game_object(obj)
    assert obj in game_state.get_game_objects()

def test_add_apple(game_state):
    obj_size = 10  
    apple = GameObject(game_state, Position(1, 1), obj_size) 
    game_state.add_apple(apple)
    assert apple in game_state.get_cookies()

def test_add_powerup(game_state):
    obj_size = 10  
    powerup = GameObject(game_state, Position(1, 1), obj_size) 
    game_state.add_powerup(powerup)
    assert powerup in game_state.get_powerups()

def test_add_hero(game_state):
    hero = Hero(game_state, Position(1, 1), 20) 
    game_state.add_hero(hero)
    assert game_state.get_hero() == hero

def test_add_wall(game_state):
    wall = Wall(game_state, Position(1, 1))
    game_state.add_wall(wall)
    assert wall in game_state.get_walls()

def test_add_score(game_state):
    initial_score = game_state._score
    game_state.add_score(10)
    assert game_state._score == initial_score + 10