from GameObjects import Entity
from Direction import Direction
from Constants import ScoreType, GhostBehaviour, PACMAN_SIZE, PACMAN_MOUTH_OPEN, PACMAN_MOUTH_CLOSED
from Position import Position
import pygame as pygame

#ініціалізація героя гри, завантаження його графічного представлення (відкритий та закритий рот) і встановлення початкового стану
class Hero(Entity):
    def __init__(self,
                 game_state,
                 screen_position: Position,
                 hero_size: int = PACMAN_SIZE):
        super().__init__(game_state, screen_position, hero_size, (255, 255, 0), False)
        self.buffer_direction = self._currentFda_direction
        self.open = pygame.transform.scale(pygame.image.load(PACMAN_MOUTH_OPEN), (self._size, self._size))
        self.closed = pygame.transform.scale(pygame.image.load(PACMAN_MOUTH_CLOSED), (self._size, self._size))
        self.image = self.open
        self.mouth_open = True

    #метод відповідає за керування рухом героя, зокрема враховує зміни напрямку руху, взаємодію з об'єктами на мапі та подіями гри
    def tick(self, dt):
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

#цей метод дозволяє перевіряти можливість руху героя у певному напрямку без фактичного переміщення та дозволяє виконати відповідні дії в залежності від результату цієї спроби переміщення
    def _try_move_in_direction(self, direction: Direction) -> bool:
        prev_position = self.get_position()
        self.move_in_direction(direction)

        if self.collides_with_wall():
            self.set_position(prev_position)
            return False
        else:
            return True

    def set_direction(self, direction: Direction):
        self.buffer_direction = direction

    #метод відповідає за взаємодію героя з об'єктами на мапі гри, реалізуючи механіку збору печива та підсилення
    def handle_cookie_pickup(self):
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
    #метод відповідає за взаємодію героя з привидами у грі, визначаючи результати зіткнень та відповідні дії гравця
    def handle_ghosts(self):
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
    #метод відповідає за вибір та обробку зображення головного героя гри, а також за його правильне відображення та обертання відповідно до напрямку руху
    def draw(self):
        self._entity_image = self.open if self.mouth_open else self.closed
        self._entity_image = pygame.transform.rotate(self._entity_image, self._current_direction.to_angle())
        super().draw()
