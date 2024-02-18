from Constants import *


class ModesController:
    def __init__(self,
                 scatter_time: int = SCATTER_TIME,
                 chase_time: int = CHASE_TIME,
                 fright_time: int = FRIGHT_TIME,
                 initial_state: GhostBehaviour = GhostBehaviour.SCATTER):
        self._scatter_time = scatter_time
        self._chase_time = chase_time
        self._fright_time = fright_time
        self._current_state = initial_state
        self._timer = 0
        self._time = 0

    def update(self, dt):
        if self._current_state is GhostBehaviour.SPAWN:
            return

        self._timer += dt

        if self._timer < self._time:
            return

        if self._current_state is GhostBehaviour.CHASE:
            self.start_scatter()
        elif self._current_state is GhostBehaviour.CHASE:
            self.start_chase()

    def get_current_state(self):
        return self._current_state

    def _reset_timer(self):
        self._timer = 0

    def start_spawn(self):
        self._current_state = GhostBehaviour.SPAWN

    def start_scatter(self):
        self._current_state = GhostBehaviour.SCATTER
        self._time = self._scatter_time
        self._reset_timer()

    def start_chase(self):
        self._current_state = GhostBehaviour.CHASE
        self._time = self._chase_time
        self._reset_timer()

    def start_fright(self):
        if self._current_state is GhostBehaviour.SPAWN:
            return
        self._current_state = GhostBehaviour.FRIGHT
        self._time = self._fright_time
        self._reset_timer()
