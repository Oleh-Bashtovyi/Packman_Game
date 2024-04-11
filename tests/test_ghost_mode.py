import pytest

from tests.helpers import almost_equal, controller_has_state_and_time_left
from ModeController import ModeController
from Constants import GhostBehaviour


@pytest.fixture
def default_scatter_time():
    return 10


@pytest.fixture
def default_chase_time():
    return 20


@pytest.fixture
def default_freight_time():
    return 5


@pytest.fixture
def default_state():
    return GhostBehaviour.SCATTER


@pytest.fixture
def default_mode_controller(default_scatter_time, default_chase_time, default_freight_time, default_state):
    return ModeController(default_scatter_time, default_chase_time, default_freight_time, default_state)


@pytest.fixture
def default_scatter_mode_controller(default_scatter_time, default_chase_time, default_freight_time):
    return ModeController(default_scatter_time, default_chase_time, default_freight_time, GhostBehaviour.SCATTER)


def test_initial_mode_state_scatter(default_mode_controller, default_state):
    controller = default_mode_controller
    assert controller.get_current_state() == default_state


def test_initial_mode_state_chase():
    controller = ModeController(10, 10, 10, GhostBehaviour.CHASE)
    assert controller.get_current_state() == GhostBehaviour.CHASE


def test_initial_mode_state_spawn():
    controller = ModeController(10, 10, 10, GhostBehaviour.SPAWN)
    assert controller.get_current_state() == GhostBehaviour.SPAWN


def test_initial_mode_state_fright():
    controller = ModeController(10, 10, 10, GhostBehaviour.FRIGHT)
    assert controller.get_current_state() == GhostBehaviour.FRIGHT


def test_start_scatter_while_scatter(default_scatter_mode_controller):
    controller = default_scatter_mode_controller
    controller.start_scatter()
    assert controller.get_current_state() == GhostBehaviour.SCATTER


def test_start_scatter_after_scatter_some_time(default_scatter_mode_controller, default_scatter_time):
    controller = default_scatter_mode_controller
    assert almost_equal(controller.get_current_state_time_left(), default_scatter_time)
    controller.update(default_scatter_time - 2.5)
    assert almost_equal(controller.get_current_state_time_left(), 2.5)
    controller.start_scatter()
    assert controller.get_current_state() == GhostBehaviour.SCATTER
    assert almost_equal(controller.get_current_state_time_left(), default_scatter_time)


def test_from_scatter_to_chase_transition(default_scatter_mode_controller, default_scatter_time, default_chase_time):
    controller = default_scatter_mode_controller
    assert controller_has_state_and_time_left(controller, GhostBehaviour.SCATTER, default_scatter_time)
    controller.update(default_scatter_time - 1.5)
    assert controller_has_state_and_time_left(controller, GhostBehaviour.SCATTER, 1.5)
    controller.update(default_scatter_time)
    assert controller_has_state_and_time_left(controller, GhostBehaviour.CHASE, default_chase_time)
    controller.update(default_chase_time - 3.71)
    assert controller_has_state_and_time_left(controller, GhostBehaviour.CHASE, 3.71)


def test_start_freight_while_spawn():
    """
    While spawn ghost should not be able to freight
    """
    controler = ModeController(10, 10, 10, GhostBehaviour.SPAWN)
    controler.start_fright()
    assert controler.get_current_state() == GhostBehaviour.SPAWN


def test_mode_start_scatter_from_scatter():
    controller = ModeController(10, 10, 10, GhostBehaviour.SCATTER)
    controller.start_scatter()
    controller.update(3)
    assert almost_equal(controller.get_current_state_time_left(), 7)
    assert controller.get_current_state() == GhostBehaviour.SCATTER
    controller.update(0.5)
    assert almost_equal(controller.get_current_state_time_left(), 6.5)


def test_mode_spawn():
    controller = ModeController(10, 10, 10, GhostBehaviour.SCATTER)
    controller.start_spawn()
    assert controller.get_current_state() == GhostBehaviour.SPAWN
    controller.start_fright()
    assert controller.get_current_state() == GhostBehaviour.SPAWN



