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
    MAZE = [['X', ' ', 'U'],
            [' ', 'X', ' '],
            ['X', 'X', 'X']]
    fill_gamestate_with_static_objects(game_state, MAZE)
    assert len(game_state.get_powerups()) == 1

