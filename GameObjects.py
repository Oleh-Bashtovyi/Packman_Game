from Position import Position
import pygame as pygame


class GameObject:
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 obj_size: int,
                 obj_color: tuple[int, int, int] = (255, 0, 0),
                 is_circle: bool = False):
        self._size = obj_size
        self._half_size = int(obj_size / 2)
        self._renderer = game_state
        self._surface = game_state.get_surface()
        self.position = screen_position
        self._color = obj_color
        self._circle = is_circle
        self._shape = pygame.Rect(self.position.x, self.position.y, self._size, self._size)

    def draw(self):
        if self._circle:
            pygame.draw.circle(self._surface, self._color, (self.get_x(), self.get_y()), self._size)
        else:
            rect_object = pygame.Rect(self.position.x, self.position.y, self._size, self._size)
            pygame.draw.rect(self._surface, self._color, rect_object, border_radius=3)

    def get_x(self):
        return self.position.x

    def get_y(self):
        return self.position.y

    def get_shape(self):
        return pygame.Rect(self.position.x, self.position.y, self._size, self._size)

    def set_position(self, position: Position | tuple | list):
        self.position.x = position[0]
        self.position.y = position[1]

    def get_position(self) -> Position:
        return Position(self.position.x, self.position.y)

    def get_center_position(self) -> Position:
        return self.position + [self._half_size, self._half_size]
