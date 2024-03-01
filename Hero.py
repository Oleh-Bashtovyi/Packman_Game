from GameObjects import Entity
from Direction import Direction
from Constants import ScoreType, GhostBehaviour, PACMAN_SIZE, PACMAN_MOUTH_OPEN, PACMAN_MOUTH_CLOSED
from Position import Position
import pygame as pygame


class Hero(Entity):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 hero_size: int = PACMAN_SIZE):
        super().__init__(game_state, screen_position, hero_size, (255, 255, 0), False)
        self.buffer_direction = self._current_direction
        self.open = pygame.transform.scale(pygame.image.load(PACMAN_MOUTH_OPEN), (self._size, self._size))
        self.closed = pygame.transform.scale(pygame.image.load(PACMAN_MOUTH_CLOSED), (self._size, self._size))
        self.image = self.open
        self.mouth_open = True

    def tick(self, dt):
        """
        is responsible for controlling the movement of the hero, 
        in particular, takes into account changes in the direction of movement, 
        interaction with objects on the map and game events
        """
        # якщо буфер відрізняється, то гравець нажав клавішу і змінив напрям
        if self.buffer_direction != self._current_direction:
            # якщо вдалось піти в тому напрямі, що вказав користувач
            if self._try_move_in_direction(self.buffer_direction):
                self._current_direction = self.buffer_direction
            # інакше пробуємо йти в старому напрямі
            else:
                self.buffer_direction = self._current_direction
                self._try_move_in_direction(self._current_direction)
        # інакше продовжуємо йти в поточному напрямі
        else:
            self._try_move_in_direction(self._current_direction)

        self.handle_teleport()
        self.handle_cookie_pickup()
        self.handle_ghosts()

    def _try_move_in_direction(self, direction: Direction) -> bool:
        """
        allows you to check the possibility of the hero moving in a certain direction 
        without actually moving and allows you to perform appropriate actions depending 
        on the result of this attempted movement
        """
        prev_position = self.get_position()
        self.move_in_direction(direction)

        if self.collides_with_wall():
            self.set_position(prev_position)
            return False
        else:
            return True

    def set_direction(self, direction: Direction):
        self.buffer_direction = direction

    def handle_cookie_pickup(self):
        """
        is responsible for the interaction of the hero with objects on the game map, 
        implementing the mechanics of collecting cookies and power-ups
        """
        collision_rect = pygame.Rect(self._position.x, self._position.y, self._size, self._size)
        cookies = self._renderer.get_cookies()
        powerups = self._renderer.get_powerups()
        game_objects = self._renderer.get_game_objects()
        cookie_to_remove = None
        for cookie in cookies:
            collides = collision_rect.colliderect(cookie.get_shape())
            if collides and cookie in game_objects:
                game_objects.remove(cookie)
                self._renderer.add_score(ScoreType.APPLE.value)
                cookie_to_remove = cookie

        if cookie_to_remove is not None:
            cookies.remove(cookie_to_remove)

        if len(self._renderer.get_cookies()) == 0:
            self._renderer.set_won()

        for powerup in powerups:
            collides = collision_rect.colliderect(powerup.get_shape())
            if collides and powerup in game_objects:
                game_objects.remove(powerup)
                self._renderer.add_score(ScoreType.POWERUP.value)
                self._renderer.activate_powerup()

    def handle_ghosts(self):
        """
        is responsible for the hero's interaction with the ghosts in the game, 
        determining the results of the encounters and the corresponding actions of the player
        """
        collision_rect = self.get_shape()
        ghosts = self._renderer.get_ghost_group().get_ghosts()
        for ghost in ghosts:
            collides = collision_rect.colliderect(ghost.get_shape())
            if collides:
                if ghost.get_current_state() is GhostBehaviour.FRIGHT:
                    self._renderer.add_score(self._renderer.get_ghost_group().get_points())
                    self._renderer.get_ghost_group().update_points()
                    ghost.start_spawn()
                elif ghost.get_current_state() is not GhostBehaviour.SPAWN:
                    if not self._renderer.get_won():
                        self._renderer.kill_pacman()

    def draw(self):
        """
        is responsible for selecting and processing the image of the main character of the game,
        as well as for its correct display and rotation according to the direction of movement
        """
        self._entity_image = self.open if self.mouth_open else self.closed
        self._entity_image = pygame.transform.rotate(self._entity_image, self._current_direction.to_angle())
        super().draw()
