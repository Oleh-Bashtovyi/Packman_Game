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


def test_handle_events(game_state):
    event_quit = pygame.event.Event(QUIT)
    event_keydown = pygame.event.Event(pygame.KEYDOWN, {'key': K_UP})

    pygame.event.post(event_quit)
    pygame.event.post(event_keydown)

    game_state._handle_events()

    assert game_state._done == True
    hero = game_state.get_hero()
    if hero is not None:
        assert hero.direction == Direction.UP


def test_display_text(game_state):
    game_state._screen = pygame.Surface((800, 600)) 
    text_surface = pygame.Surface((100, 50))  
    text = "Test Message"
    font = pygame.font.SysFont('Arial', 20)
    text_surface.blit(font.render(text, True, (255, 255, 255)), (0, 0))  
    position = (100, 100)  

    game_state.display_text(text, position, 20)

    assert game_state._screen.blit(text_surface, position) == pygame.Rect(position, (100, 50))

def test_kill_pacman(game_state):
    game_state._lives = 3  
    game_state._hero = GameObject(game_state, Position(0, 0), 10, obj_color=(255, 0, 0), is_circle=False)  
    game_state.kill_pacman()

    assert game_state._lives == 2 
    assert game_state._hero._position == Position(game_state.TILE_SIZE, game_state.TILE_SIZE) 


def test_set_won(game_state):
    game_state.set_won()
    assert game_state.get_won() == True