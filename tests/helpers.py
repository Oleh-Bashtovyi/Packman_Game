from Position import Position
from Ghosts import GhostGroup
from ModeController import ModeController
from Constants import GhostBehaviour
from Direction import Direction


def almost_equal(a, b, tolerance=1e-9):
    """
    Checks if two numbers are almost equal within a given tolerance.
    """
    return abs(a - b) <= tolerance


def do_nothing():
    pass


def controller_has_state_and_time_left(controller: ModeController, behaviour: GhostBehaviour, duration):
    """
    Checks if specified ghost behaviour controller
    has specified state currently and checks
    time left equality for current state
    """
    assert controller.get_current_state() == behaviour
    assert almost_equal(controller.get_current_state_time_left(), duration)
    return True


def assert_all_ghosts_have_state(ghost_group: GhostGroup, state: GhostBehaviour):
    """
    Checks if all ghosts has specified state
    """
    ghosts = ghost_group.get_ghosts()
    for ghost in ghosts:
        assert ghost.get_current_state() == state


def assert_all_ghosts_have_direction(ghost_group: GhostGroup, direction: Direction):
    """
    Checks if all ghosts look at specified direction
    """
    ghosts = ghost_group.get_ghosts()
    for ghost in ghosts:
        assert ghost.get_current_direction() == direction


def assert_all_ghosts_have_screen_position(ghost_group: GhostGroup, positions: list[Position]):
    ghosts = ghost_group.get_ghosts()
    counter = 0
    for ghost in ghosts:
        assert ghost.get_screen_position() == positions[counter]
        counter += 1