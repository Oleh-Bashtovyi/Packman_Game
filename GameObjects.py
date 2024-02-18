from Position import Position
from Direction import Direction
from typing import Tuple
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
        self.entity_image = pygame.transform.scale(pygame.image.load(entity_image), (self._size, self._size))

    def tick(self):
        pass

    def draw(self):
        self._surface.blit(self.entity_image, self.get_shape())

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
