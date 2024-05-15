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

    # ��������� ��'��� �������
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', type=int)
    parser.add_argument('--sclf', type=int)

    # ������� ���������
    args = parser.parse_args(['--fps', '60', '--sclf', '2'])

    # ����������, �� ��������� ���� ���� ���������
    assert args.fps == 60
    assert args.sclf == 2

