from GameObjects import *
import pygame
from Constants import *

class GameState:
    def __init__(self, maze_controller):
        pygame.init()
        self._width = SCREEN_WIDTH
        self._height = SCREEN_HEIGHT
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pacman')
        self._clock = pygame.time.Clock()
        self._done = False
        self._won = False
        self.maze_controller = maze_controller
        self._game_objects = []
        self._walls = []
        self._cookies = []
        self._powerups = []
        self._ghosts = []
        self._hero: Hero = None
        self.ghsotGroup = ()
        self._lives = 3
        self._score = 0
        self._score_cookie_pickup = 10
        self._score_ghost_eaten = 400
        self._score_powerup_pickup = 50
        self._powerup_active = False  # powerup, special ability
        self._current_mode = GhostBehaviour.SCATTER
        self._mode_switch_event = pygame.USEREVENT + 1  # custom event
        self._powerup_end_event = pygame.USEREVENT + 2
        self._pakupaku_event = pygame.USEREVENT + 3

    def add_game_object(self, obj: GameObject):
        self._game_objects.append(obj)

    def add_cookie(self, obj: GameObject):
        self._game_objects.append(obj)
        self._cookies.append(obj)

    def add_ghost(self, obj: GameObject):
        self._game_objects.append(obj)
        self._ghosts.append(obj)

    def add_powerup(self, obj: GameObject):
        self._game_objects.append(obj)
        self._powerups.append(obj)

    def activate_powerup(self):
        self.ghsotGroup.reset()
        self.ghsotGroup.resetScore()
        self.ghsotGroup.startFreight()


