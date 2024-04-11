from GameObjects import Entity
import MazeController
from ModeController import ModeController
from Constants import GhostBehaviour
from Constants import ScoreType
from Constants import RED_GHOST, BLUE_GHOST, PINK_GHOST, ORANGE_GHOST, SCARED_GHOST, DEAD_GHOST
from Direction import Direction
from Position import Position
from typing import Tuple
import random
import pygame as pygame


class Ghost(Entity):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 spawn_position_in_grid: Position,
                 scatter_position_in_grid: Position,
                 obj_size: int,
                 mode_controller: ModeController,
                 pacman=None,
                 obj_color: Tuple[int, int, int] = (255, 0, 0),
                 entity_image=None):
        super().__init__(game_state, screen_position, obj_size, obj_color, is_circle=False, entity_image=entity_image)
        self._mode_controller: ModeController = mode_controller
        self._fright_image = pygame.transform.scale(pygame.image.load(SCARED_GHOST), (self._size, self._size))
        self._dead_image = pygame.transform.scale(pygame.image.load(DEAD_GHOST), (self._size, self._size))
        self._alive_image = pygame.transform.scale(pygame.image.load(entity_image), (self._size, self._size))
        self._spawn_position: Position = spawn_position_in_grid
        self._scatter_position: Position = scatter_position_in_grid
        self._current_target: Position = scatter_position_in_grid
        self._select_direction_method = self._move_to_target_method
        self._pacman = pacman
        self._handle_states()

    def tick(self, dt):
        self._mode_controller.update(dt)
        self._handle_states()

        # якщо напряму ще нема, або привид стоїть ЧІТКО на плитці
        if (self._current_direction is Direction.NONE or
                (self.get_x() % self._renderer.TILE_SIZE == 0 and
                 self.get_y() % self._renderer.TILE_SIZE == 0)):
            self._select_direction_method()
        self.move_in_current_direction()
        self.handle_teleport()

    def get_current_state(self):
        """
        Returns current ghost behaviour (chase\freight etc.)
        :return: Current behaviour
        """
        return self._mode_controller.get_current_state()

    def _set_chase_target(self):
        self._set_target(self._pacman.get_grid_position())

    def _set_scatter_target(self):
        self._set_target(self._scatter_position)

    def _set_spawn_target(self):
        self._set_target(self._spawn_position)

    def _set_target(self, target: Position):
        """
        Sets target to wich ghost fill follow.
        :param target: Position of this target
        """
        self._current_target = target

    def _get_target(self) -> Position:
        """
        Returns current followed target.
        """
        return self._current_target

    def start_scatter(self):
        """
        Change current ghost behaviour to scatter.
        """
        self._mode_controller.start_scatter()
        if self._mode_controller.get_current_state() is GhostBehaviour.SCATTER:
            self._select_direction_method = self._move_to_target_method
            self._set_scatter_target()

    def start_chase(self):
        """
        Change current ghost behaviour to chase.
        """
        self._mode_controller.start_chase()
        if self._mode_controller.get_current_state() is GhostBehaviour.CHASE:
            self._select_direction_method = self._move_to_target_method
            self._set_scatter_target()

    def start_spawn(self):
        """
        Change current ghost behaviour to spawn.
        """
        self._mode_controller.start_spawn()
        if self._mode_controller.get_current_state() is GhostBehaviour.SPAWN:
            self._select_direction_method = self._move_to_target_method
            self._set_spawn_target()

    def start_fright(self):
        """
        Change current ghost behaviour to fright.
        """
        self._mode_controller.start_fright()
        if self._mode_controller.get_current_state() is GhostBehaviour.FRIGHT:
            self._select_direction_method = self._random_move_method

    def is_at_spawn_position(self) -> bool:
        """
        Checks if currently on spawn position.
        :return: is on spawn position.
        """
        grid_position = self.get_grid_position()
        return self._spawn_position.x == grid_position.x and self._spawn_position.y == grid_position.y

    def _handle_states(self):
        """
        Handles mode controller current states
        and sets apropriate followed targets.
        """
        state = self._mode_controller.get_current_state()
        if state is GhostBehaviour.SPAWN:
            if self.is_at_spawn_position():
                self.start_chase()
            else:
                self._set_spawn_target()
        elif state is GhostBehaviour.SCATTER:
            self._set_scatter_target()
        elif state is GhostBehaviour.CHASE:
            self._set_chase_target()

    # методи, які будуть використовуватись для різних станів привидів.
    # В стані страху буде використовуватись метод випадкового напряму.
    def _move_to_target_method(self):
        """
        Method that selects and set direction that
        has the shortest path to target.
        """
        directions = self._get_movable_directions()

        # напрям один (це тільки в коридорах, де не можна повертати назад)
        if len(directions) == 1:
            self.set_current_direction(directions[0][0])
        else:
            # напрямів кілька (це на перехрестях), тому треба обрати той,
            # що матиме найменший шлях до поточної цілі
            target_position = self._get_target()
            current_best_direction = directions[0][0]
            current_best_distance = 1000000
            for direction_item in directions:
                current_direction = direction_item[0]
                current_position = direction_item[1]
                current_distance = current_position.distance_to(target_position)
                if current_distance < current_best_distance:
                    current_best_distance = current_distance
                    current_best_direction = current_direction
            self.set_current_direction(current_best_direction)

    def _random_move_method(self):
        """
        Method that randomly selects and set direction (used in ghost freight mode).
        """
        directions = self._get_movable_directions()
        self.set_current_direction(random.choice(directions)[0])

    def _get_movable_directions(self) -> list[(Direction, Position)]:
        """
        Returns all movable directions from
        current position and excludes direction to
        move back.
        """
        all_directions = (self._renderer.get_ghost_group().maze_controller
                          .get_node_at_position(self.get_grid_position())
                          .get_walkable_positions())

        opposite_direction = self._current_direction.opposite()
        walkable_directions = [tup for tup in all_directions if tup[0] != opposite_direction]

        if len(walkable_directions) == 0:
            walkable_directions.append((Direction.NONE, self.get_grid_position()))

        return walkable_directions

    def draw(self):
        state = self._mode_controller.get_current_state()
        if state is GhostBehaviour.SPAWN:
            self._entity_image = self._dead_image
        elif state is GhostBehaviour.FRIGHT:
            self._entity_image = self._fright_image
        else:
            self._entity_image = self._alive_image
        super().draw()


class RedGhost(Ghost):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 spawn_position_in_grid: Position,
                 scatter_position_in_grid: Position,
                 obj_size: int,
                 mode_controller: ModeController,
                 pacman=None):
        super().__init__(game_state,
                         screen_position,
                         spawn_position_in_grid,
                         scatter_position_in_grid,
                         obj_size=obj_size,
                         mode_controller=mode_controller,
                         pacman=pacman,
                         entity_image=RED_GHOST)


class PinkGhost(Ghost):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 spawn_position_in_grid: Position,
                 scatter_position_in_grid: Position,
                 obj_size: int,
                 mode_controller: ModeController,
                 pacman=None):
        super().__init__(game_state,
                         screen_position,
                         spawn_position_in_grid,
                         scatter_position_in_grid,
                         obj_size=obj_size,
                         mode_controller=mode_controller,
                         pacman=pacman,
                         entity_image=PINK_GHOST)

    def _set_chase_target(self):
        self._current_target = self._pacman.get_grid_position() + 4 * self._pacman.get_current_direction().to_shift()


class BlueGhost(Ghost):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 spawn_position_in_grid: Position,
                 scatter_position_in_grid: Position,
                 obj_size: int,
                 mode_controller: ModeController,
                 pacman=None,
                 red_ghost: RedGhost = None):
        super().__init__(game_state,
                         screen_position,
                         spawn_position_in_grid,
                         scatter_position_in_grid,
                         obj_size=obj_size,
                         mode_controller=mode_controller,
                         pacman=pacman,
                         entity_image=BLUE_GHOST)
        self._red_ghost = red_ghost

    def _set_chase_target(self):
        pacman_position = self._pacman.get_grid_position()
        red_ghost_position = self._red_ghost.get_grid_position()
        self._current_target = pacman_position * 2 - red_ghost_position


class OrangeGhost(Ghost):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 spawn_position_in_grid: Position,
                 scatter_position_in_grid: Position,
                 obj_size: int,
                 mode_controller: ModeController,
                 pacman=None):
        super().__init__(game_state,
                         screen_position,
                         spawn_position_in_grid,
                         scatter_position_in_grid,
                         obj_size=obj_size,
                         mode_controller=mode_controller,
                         pacman=pacman,
                         entity_image=ORANGE_GHOST)

    def _set_chase_target(self):
        if self.get_grid_position().distance_to(self._pacman.get_grid_position()) > 8:
            self._current_target = self._pacman.get_grid_position()
        else:
            self._current_target = self._scatter_position


class GhostGroup:
    def __init__(self, game_state, maze_controller: MazeController):
        self._current_points: int = ScoreType.GHOST.value
        self.maze_controller = maze_controller
        self._ghosts = []

    def add_ghost(self, ghost: Ghost):
        self._ghosts.append(ghost)

    def draw(self):
        for ghost in self._ghosts:
            ghost.draw()

    def tick(self, dt):
        for ghost in self._ghosts:
            ghost.tick(dt)

    def get_ghosts(self) -> list[Ghost]:
        return self._ghosts[:]

    def update_points(self):
        self._current_points *= 2

    def get_points(self):
        return self._current_points

    def reset_points(self):
        self._current_points = ScoreType.GHOST.value

    def start_freight(self):
        self.reset_points()
        for ghost in self._ghosts:
            ghost.start_fright()

    def start_chase(self):
        for ghost in self._ghosts:
            ghost.start_chase()

    def start_scatter(self):
        for ghost in self._ghosts:
            ghost.start_scatter()
