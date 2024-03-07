from ModesController import ModesController
from Constants import GhostBehaviour


def test_mode_scatter():
    controller = ModesController(10, 10, 10, GhostBehaviour.SCATTER)
    controller.start_scatter()
    assert controller.get_current_state() == GhostBehaviour.SCATTER


def test_mode_spawn():
    controller = ModesController(10, 10, 10, GhostBehaviour.SCATTER)
    controller.start_spawn()
    assert controller.get_current_state() == GhostBehaviour.SPAWN
    controller.start_fright()
    assert controller.get_current_state() == GhostBehaviour.SPAWN
