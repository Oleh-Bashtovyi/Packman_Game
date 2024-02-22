import pygame
from Constants import *
from GameObjects import Entity
from Position import *


class Hero(Entity):
    def __init__(self,
                 game_state,
                 spawn_position: Position):
        super().__init__(game_state, spawn_position, PACMAN_SIZE, (255, 255, 0), False)
        self.last_non_colliding_position = (0, 0)
        self.open = pygame.image.load("images/paku.png")
        self.closed = pygame.image.load("images/man.png")
        self.image = self.open
        self.mouth_open = True

    ###############################


    def set_direction(self, dir):
        self.bufferDirection = dir

    def handle_cookie_pickup(self):
        collision_rect = pygame.Rect(self.x, self.y, self._size, self._size)
        cookies = self._renderer.get_cookies()
        powerups = self._renderer.get_powerups()
        game_objects = self._renderer.get_game_objects()
        cookie_to_remove = None
        for cookie in cookies:
            collides = collision_rect.colliderect(cookie.get_shape())
            if collides and cookie in game_objects:
                game_objects.remove(cookie)
                self._renderer.add_score(ScoreType.APPLE)
                cookie_to_remove = cookie

        if cookie_to_remove is not None:
            cookies.remove(cookie_to_remove)

        if len(self._renderer.get_cookies()) == 0:
            self._renderer.set_won()

        for powerup in powerups:
            collides = collision_rect.colliderect(powerup.get_shape())
            if collides and powerup in game_objects:
                if not self._renderer.is_powerup_active():
                    game_objects.remove(powerup)
                    self._renderer.add_score(ScoreType.POWERUP)
                    self._renderer.activate_powerup()