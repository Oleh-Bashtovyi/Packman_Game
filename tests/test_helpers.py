from ModeController import ModeController
from Constants import GhostBehaviour


def almost_equal(a, b, tolerance=1e-9):
    """
    Checks if two numbers are almost equal within a given tolerance.
    """
    return abs(a - b) <= tolerance


def controller_has_state_and_time_left(controller: ModeController, behaviour: GhostBehaviour, duration):
    """
    Checks if specified ghost behaviour controller
    has specified state currently and checks
    time left equality for current state
    """
    assert controller.get_current_state() == behaviour
    assert almost_equal(controller.get_current_state_time_left(), duration)
    return True
