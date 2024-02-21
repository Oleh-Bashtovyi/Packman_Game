from GameObjects import *
import pygame
from Constants import *
from Hero import *

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

    def set_won(self):
        self._won = True

    def get_won(self):
        return self._won

    def add_score(self, in_score: ScoreType):
        self._score += in_score.value

    def get_hero_position(self):
        return self._hero.get_position() if self._hero is not None else (0, 0)


    def end_game(self):
        if self._hero in self._game_objects:
            self._game_objects.remove(self._hero)
        self._hero = None

    def kill_pacman(self):
        self._lives -= 1
        self._hero.set_position(TILE_SIZE, TILE_SIZE)
        self._hero.set_direction(Direction.NONE)
        if self._lives == 0: self.end_game()

    def display_text(self, text, in_position=(32, 0), in_size=30):
        font = pygame.font.SysFont('Arial', in_size)
        text_surface = font.render(text, False, (255, 255, 255))
        self._screen.blit(text_surface, in_position)

