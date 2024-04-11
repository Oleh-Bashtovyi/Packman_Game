from Constants import RED_GHOST
from Constants import APPLE_COLOR, POWERUP_COLOR, APPLE_SIZE, POWERUP_SIZE, WALL_COLOR
from Direction import Direction
from Position import Position
from typing import Tuple
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

    def draw(self):
        """
        Draws object on screen. Call on every pygame frame.
        """
        if self._circle:
            tile_half = self._renderer.TILE_HALF
            pygame.draw.circle(self._surface, self._color, self.get_screen_position() + [tile_half, tile_half], self._size)
        else:
            rect_object = pygame.Rect(self._position.x, self._position.y, self._size, self._size)
            pygame.draw.rect(self._surface, self._color, rect_object, border_radius=3)

    def get_x(self):
        return self._position.x

    def get_y(self):
        return self._position.y

    def get_shape(self):
        """
        Get object shape. Required in collision check.
        :return: Rectangle shape of object
        """
        if self._circle:
            tile_half_half = int(self._renderer.TILE_HALF / 2)
            pos_x = self._position.x + tile_half_half
            pos_y = self._position.y + tile_half_half
            return pygame.Rect(pos_x, pos_y, self._size, self._size)
        else:
            return pygame.Rect(self._position.x, self._position.y, self._size, self._size)

    def set_screen_position(self, position: Position | tuple | list):
        self._position.x = position[0]
        self._position.y = position[1]

    def get_screen_position(self) -> Position:
        return Position(self._position.x, self._position.y)

    def get_screen_center_position(self) -> Position:
        return self._position + [self._half_size, self._half_size]

    def get_grid_position(self) -> Position:
        """
        Returns position of object in renderer field.
        :return: Grid position
        """
        center = self.get_screen_center_position()
        x = center.x // self._renderer.TILE_SIZE
        y = center.y // self._renderer.TILE_SIZE
        return Position(x, y)


class Wall(GameObject):
    def __init__(self,
                 game_state,
                 screen_position: Position):
        super().__init__(game_state, screen_position, game_state.TILE_SIZE, WALL_COLOR)


class Apple(GameObject):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 apple_size: int = APPLE_SIZE):
        super().__init__(game_state, screen_position, apple_size, APPLE_COLOR, True)


class Powerup(GameObject):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 powerup_size: int = POWERUP_SIZE):
        super().__init__(game_state, screen_position, powerup_size, POWERUP_COLOR, True)


class Entity(GameObject):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 obj_size: int,
                 obj_color: Tuple[int, int, int] = (255, 0, 0),
                 is_circle: bool = False,
                 entity_image=None):
        super().__init__(game_state, screen_position, obj_size, obj_color, is_circle)
        self._current_direction = Direction.NONE

        if entity_image is not None:
            self._entity_image = pygame.transform.scale(pygame.image.load(entity_image), (self._size, self._size))
        else:
            self._entity_image = None

    def tick(self, dt):
        """
        Called on every pygame frame. Moves entity
        and handle events.
        :param dt: time (in seconds) since last frame
        """
        pass

    def draw(self):
        if self._entity_image is not None:
            self._surface.blit(self._entity_image, self.get_shape())

    def move_in_current_direction(self):
        self.move_in_direction(self._current_direction)

    def move_in_direction(self, direction: Direction):
        """
        Moves entity in specified direction without
        collision check
        :param direction: Movable direction
        """
        self._position += direction.to_shift()

    def get_current_direction(self):
        return self._current_direction

    def set_current_direction(self, direction: Direction):
        self._current_direction = direction

    def handle_teleport(self):
        """
        Handles horizontal entity teleportation.
        Depend on gamestate.
        """
        center = self.get_screen_center_position()
        if center.x < 0:
            self.set_screen_position((self._renderer.SCREEN_WIDTH - self._half_size, self.get_y()))
        elif center.x > self._renderer.SCREEN_WIDTH:
            self.set_screen_position((-self._half_size, self.get_y()))

    def collides_with_wall(self) -> bool:
        """
        Checks collision with all walls in gamestate
        in current position.
        :return: wether collide with any wall or not
        """
        collision_rect = pygame.Rect(self.get_x(), self.get_y(), self._size, self._size)
        collides = False
        walls = self._renderer.get_walls()
        for wall in walls:
            collides = collision_rect.colliderect(wall.get_shape())
            if collides:
                break
        return collides
