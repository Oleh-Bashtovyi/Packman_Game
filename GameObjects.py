import random

from Position import Position
from Direction import Direction
from typing import Tuple, List
import random
from ModesController import ModesController
from Constants import *
import pygame as pygame


class GameObject:
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 obj_size: int,
                 obj_color: Tuple[int, int, int] = (255, 0, 0),
                 is_circle: bool = False):
        self._size = obj_size
        self._half_size = int(obj_size / 2)
        self._renderer = game_state
        self._surface = game_state.get_surface()
        self._position = screen_position
        self._color = obj_color
        self._circle = is_circle
        self._shape = pygame.Rect(self._position.x, self._position.y, self._size, self._size)

    def draw(self):
        if self._circle:
            pygame.draw.circle(self._surface, self._color, (self.get_x(), self.get_y()), self._size)
        else:
            rect_object = pygame.Rect(self._position.x, self._position.y, self._size, self._size)
            pygame.draw.rect(self._surface, self._color, rect_object, border_radius=3)

    def get_x(self):
        return self._position.x

    def get_y(self):
        return self._position.y

    def get_shape(self):
        return pygame.Rect(self._position.x, self._position.y, self._size, self._size)

    def set_position(self, position: Position | tuple | list):
        self._position.x = position[0]
        self._position.y = position[1]

    def get_position(self) -> Position:
        return Position(self._position.x, self._position.y)

    def get_center_position(self) -> Position:
        return self._position + [self._half_size, self._half_size]

    def get_grid_position(self) -> Position:
        center = self.get_center_position()
        x = center.x // TILE_SIZE
        y = center.y // TILE_SIZE
        return Position(x, y)


class Wall(GameObject):
    def __init__(self, game_state, screen_position: Position):
        super().__init__(game_state, screen_position, TILE_SIZE, WALL_COLOR)


class Apple(GameObject):
    def __init__(self, game_state, screen_position: Position):
        super().__init__(game_state, screen_position, APPLE_SIZE, APPLE_COLOR, True)


class Powerup(GameObject):
    def __init__(self, game_state, screen_position: Position):
        super().__init__(game_state, screen_position, POWERUP_SIZE, POWERUP_COLOR, True)


class Entity(GameObject):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 obj_size: int,
                 obj_color: Tuple[int, int, int] = (255, 0, 0),
                 is_circle: bool = False,
                 entity_image='images/packman.png'):
        super().__init__(game_state, screen_position, obj_size, obj_color, is_circle)
        self._current_direction = Direction.NONE
        self._entity_image = pygame.transform.scale(pygame.image.load(entity_image), (self._size, self._size))

    def tick(self, dt):
        pass

    def draw(self):
        self._surface.blit(self._entity_image, self.get_shape())

    def move_in_current_direction(self):
        self.move_in_direction(self._current_direction)

    def move_in_direction(self, direction: Direction):
        self._position += direction.to_shift()

    def get_current_direction(self):
        return self._current_direction

    def set_current_direction(self, direction: Direction):
        self._current_direction = direction

    def handle_teleport(self):
        center = self.get_center_position()
        if center.x < 0:
            self.set_position((SCREEN_WIDTH - self._half_size, center.y))
        elif center.x > SCREEN_WIDTH:
            self.set_position((-self._half_size, center.y))

    def collides_with_wall(self):
        collision_rect = pygame.Rect(self.get_x(), self.get_y(), self._size, self._size)
        collides = False
        walls = self._renderer.get_walls()
        for wall in walls:
            collides = collision_rect.colliderect(wall.get_shape())
            if collides:
                break
        return collides


# TODO
# -Packman:
# *Make movement for packman like this:
# *if key pressed (W,A,S,D) - change buffer direction
# *in tick: move in buffer direction
# *if no collision with walls - set current direction as buffered
# *otherwise - return to first position and set buffer direction as current
# -Ghost:
# *Blinky(chase player)
# *Pinky(chase 4 cells ahead of player)
# *Inky (idk)
# *Clyde (chase and scatter)


# TODO:
# FOR SASHA
# ========================================
class Pacman(Entity):
    def __init__(self):
        a = "initialize pacman"


# ========================================


class Ghost(Entity):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 spawn_position_in_grid: Position,
                 scatter_position_in_grid: Position,
                 obj_size: int,
                 pacman: Pacman = None,
                 obj_color: Tuple[int, int, int] = (255, 0, 0),
                 is_circle: bool = False,
                 entity_image=RED_GHOST):
        super().__init__(game_state, screen_position, obj_size, obj_color, is_circle, entity_image)
        self._mode_controller: ModesController = ModesController()
        self._fright_image = pygame.transform.scale(pygame.image.load(SCARED_GHOST), (self._size, self._size))
        self._dead_image = pygame.transform.scale(pygame.image.load(DEAD_GHOST), (self._size, self._size))
        self._spawn_position: Position = spawn_position_in_grid
        self._scatter_position: Position = scatter_position_in_grid
        self._current_target: Position = scatter_position_in_grid
        self._move_method = self._move_to_target_method
        self._pacman = pacman
        self._handle_states()

    def tick(self, dt):
        self._mode_controller.update(dt)
        self._handle_states()
        self._move_method()
        self.move_in_current_direction()
        self.handle_teleport()

    def _set_chase_target(self):
        self._set_target(self._pacman.get_grid_position())

    def _set_scatter_target(self):
        self._set_target(self._scatter_position)

    def _set_spawn_target(self):
        self._set_target(self._spawn_position)

    def _set_target(self, target: Position):
        self._current_target = target

    def _get_target(self) -> Position:
        return self._current_target

    def start_scatter(self):
        self._mode_controller.start_scatter()
        if self._mode_controller.get_current_state() is GhostBehaviour.SCATTER:
            self._move_method = self._move_to_target_method
            self._set_scatter_target()

    def start_chase(self):
        self._mode_controller.start_chase()
        if self._mode_controller.get_current_state() is GhostBehaviour.CHASE:
            self._move_method = self._move_to_target_method
            self._set_scatter_target()

    def start_spawn(self):
        self._mode_controller.start_spawn()
        if self._mode_controller.get_current_state() is GhostBehaviour.SPAWN:
            self._move_method = self._move_to_target_method
            self._set_spawn_target()

    def start_fright(self):
        self._mode_controller.start_fright()
        if self._mode_controller.get_current_state() is GhostBehaviour.FRIGHT:
            self._move_method = self._random_move_method

    def _handle_states(self):
        state = self._mode_controller.get_current_state()
        if state is GhostBehaviour.SPAWN:
            self._set_spawn_target()
        elif state is GhostBehaviour.SCATTER:
            self._set_scatter_target()
        elif state is GhostBehaviour.CHASE:
            self._set_chase_target()

    # методи, які будуть використовуватись для різних станів привидів.
    # В стані страху буде використовуватись метод випадкового напряму.
    def _move_to_target_method(self):
        directions = self._get_movable_directions()

        if len(directions) == 1:
            self.set_current_direction(directions[0][0])
        else:
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
        directions = self._get_movable_directions()
        self.set_current_direction(random.choice(directions)[0][0])

    def _get_movable_directions(self) -> list[(Direction, Position)]:
        all_directions = (self._renderer.mazeController
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
            self._surface.blit(self._dead_image, self.get_shape())
        elif state is GhostBehaviour.FRIGHT:
            self._surface.blit(self._fright_image, self.get_shape())
        else:
            self._surface.blit(self._entity_image, self.get_shape())


class RedGhost(Ghost):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 spawn_position_in_grid: Position,
                 scatter_position_in_grid: Position,
                 obj_size: int,
                 pacman: Pacman = None):
        super().__init__(game_state,
                         screen_position,
                         spawn_position_in_grid,
                         scatter_position_in_grid,
                         obj_size=obj_size,
                         pacman=pacman,
                         entity_image=RED_GHOST)


class PinkGhost(Ghost):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 spawn_position_in_grid: Position,
                 scatter_position_in_grid: Position,
                 obj_size: int,
                 pacman: Pacman = None):
        super().__init__(game_state,
                         screen_position,
                         spawn_position_in_grid,
                         scatter_position_in_grid,
                         obj_size=obj_size,
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
                 pacman: Pacman = None,
                 red_ghost: RedGhost = None):
        super().__init__(game_state,
                         screen_position,
                         spawn_position_in_grid,
                         scatter_position_in_grid,
                         obj_size=obj_size,
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
                 pacman: Pacman = None):
        super().__init__(game_state,
                         screen_position,
                         spawn_position_in_grid,
                         scatter_position_in_grid,
                         obj_size=obj_size,
                         pacman=pacman,
                         entity_image=ORANGE_GHOST)

    def _set_chase_target(self):
        if self.get_grid_position().distance_to(self._pacman.get_grid_position()) > 8:
            self._current_target = self._pacman.get_grid_position()
        else:
            self._current_target = self._scatter_position


class GhostGroup:
    def __init__(self, game_state, packman,
                 red_ghost_spawn_position: Position, red_ghost_scatter_position: Position,
                 pink_ghost_spawn_position: Position, pink_ghost_scatter_position: Position,
                 blue_ghost_spawn_position: Position, blue_ghost_scatter_position: Position,
                 orange_ghost_spawn_position: Position, orange_ghost_scatter_position: Position):
        red_screen_position = red_ghost_spawn_position * TILE_SIZE
        pink_screen_position = pink_ghost_spawn_position * TILE_SIZE
        blue_screen_position = blue_ghost_spawn_position * TILE_SIZE
        orange_screen_position = orange_ghost_spawn_position * TILE_SIZE
        self._red_ghost: RedGhost = RedGhost(game_state,
                                             red_screen_position,
                                             red_ghost_spawn_position,
                                             red_ghost_scatter_position,
                                             GHOST_SIZE, packman)
        self._pink_ghost: PinkGhost = PinkGhost(game_state,
                                                pink_screen_position,
                                                pink_ghost_spawn_position,
                                                pink_ghost_scatter_position,
                                                GHOST_SIZE, packman)
        self._blue_ghost: BlueGhost = BlueGhost(game_state,
                                                blue_screen_position,
                                                blue_ghost_spawn_position,
                                                blue_ghost_scatter_position,
                                                GHOST_SIZE,
                                                packman, self._red_ghost)
        self._orange_ghost: OrangeGhost = OrangeGhost(game_state,
                                                      orange_screen_position,
                                                      orange_ghost_spawn_position,
                                                      orange_ghost_scatter_position,
                                                      GHOST_SIZE, packman)
        self._ghosts: Tuple[Ghost, Ghost, Ghost, Ghost] = (
            self._red_ghost,
            self._pink_ghost,
            self._orange_ghost,
            self._orange_ghost)
        self._current_points: int = ScoreType.GHOST.value

    def draw(self):
        for ghost in self._ghosts:
            ghost.draw()

    def tick(self, dt):
        for ghost in self._ghosts:
            ghost.tick(dt)

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
