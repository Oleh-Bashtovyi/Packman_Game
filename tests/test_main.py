import argparse
import pytest
import Constants
from GameState import GameState
import MazeController
from Position import Position
from main import parse_args, fill_gamestate_with_static_objects
from Hero import Hero
from Ghosts import GhostGroup
import ModeController
from Ghosts import PinkGhost



def test_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', type=int)
    parser.add_argument('--sclf', type=int)
    args = parser.parse_args(['--fps', '60', '--sclf', '2'])

    assert args.fps == 60
    assert args.sclf == 2

def test_fill_walls():
    game_state = GameState(10, 3, 3)
    MAZE = [['X', ' ', 'U'],
            [' ', 'X', ' '],
            ['X', 'X', 'X']]
    fill_gamestate_with_static_objects(game_state, MAZE)
    assert len(game_state.get_walls()) == 5

def test_fill_powerups():
    game_state = GameState(10, 3, 3)
    MAZE = [['X', ' ', 'P'],
            [' ', 'X', ' '],
            ['X', 'X', 'X']]
    fill_gamestate_with_static_objects(game_state, MAZE)
    assert len(game_state.get_powerups()) == 1

def test_fill_apples():
    game_state = GameState(10, 3, 3)
    MAZE = [['X', ' ', 'P'],
            [' ', 'X', ' '],
            ['X', 'X', 'X']]
    fill_gamestate_with_static_objects(game_state, MAZE)
    assert len(game_state.get_cookies()) == 3


def test_create_ghost_group_instance():
    game_state = GameState(10, 3, 3)
    MAZE = [['X', ' ', 'P'],
            [' ', 'X', ' '],
            ['X', 'X', 'X']]
    fill_gamestate_with_static_objects(game_state, MAZE)
    mzController = MazeController.MazeController()
    mzController.read_maze(MAZE)
    ghost_group = GhostGroup(game_state, mzController)
    assert isinstance(ghost_group, GhostGroup)

def test_add_ghost_to_group():
    game_state = GameState(10, 3, 3)
    MAZE = [['X', ' ', 'U'],
            [' ', 'X', ' '],
            ['X', 'X', 'X']]
    fill_gamestate_with_static_objects(game_state, MAZE)
    pacman = Hero(game_state, game_state.translate_maze_to_screen(Position(1, 1)), Constants.PACMAN_SIZE)
    mzController = MazeController.MazeController()
    mzController.read_maze(MAZE)
    ghost_group = GhostGroup(game_state, mzController)
    pinky_spawn_pos = Position(12, 13)
    pinky_scatter_pos = Position(2, 27)
    pinky_screen_pos = game_state.translate_maze_to_screen(Position(12, 13))
    pinky_mode_controller = ModeController.ModeController(10, 40, 10, Constants.GhostBehaviour.SCATTER)
    pinky = PinkGhost(game_state, pinky_screen_pos, pinky_spawn_pos, pinky_scatter_pos,
                      Constants.GHOST_SIZE, pinky_mode_controller, pacman)
    ghost_group.add_ghost(pinky)
    assert len(ghost_group.get_ghosts()) == 1

def test_get_ghosts_from_group():
    game_state = GameState(10, 3, 3)
    MAZE = [['X', ' ', 'U'],
            [' ', 'X', ' '],
            ['X', 'X', 'X']]
    fill_gamestate_with_static_objects(game_state, MAZE)
    mzController = MazeController.MazeController()
    mzController.read_maze(MAZE)
    ghost_group = GhostGroup(game_state, mzController)
    assert isinstance(ghost_group.get_ghosts(), list)
