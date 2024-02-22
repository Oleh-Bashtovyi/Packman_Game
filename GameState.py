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
        self.ghostGroup: GhostGroup = None
        self._lives = 3
        self._score = 0
        self._score_ghost_eaten = 400
        self._score_powerup_pickup = 50
        self._mode_switch_event = pygame.USEREVENT + 1  # custom event
        self._powerup_end_event = pygame.USEREVENT + 2
        self._pakupaku_event = pygame.USEREVENT + 3

    def tick(self, in_fps: int):
        black = (0, 0, 0)
        self.ghostGroup.start_scatter()
        pygame.time.set_timer(self._pakupaku_event, 200)  # open close mouth
        while not self._done:

            dt = self._clock.tick(in_fps) / 1000.0
            self.ghostGroup.tick(dt)

            if self._hero is not None:
                self._hero.tick(dt)

            for obj in self._game_objects:
                obj.draw()

            self.display_text(f"[Score: {self._score}]  [Lives: {self._lives}]")

            if self._hero is None: self.display_text("YOU DIED", (self._width / 2 - 256, self._height / 2 - 256), 100)
            if self.get_won(): self.display_text("YOU WON", (self._width / 2 - 256, self._height / 2 - 256), 100)
            pygame.display.flip()
            self._clock.tick(in_fps)
            self._screen.fill(black)
            self._handle_events()
        print("Game over")

    def get_surface(self):
        return self._screen

    def add_game_object(self, obj: GameObject):
        self._game_objects.append(obj)

    def add_apple(self, obj: GameObject):
        self._game_objects.append(obj)
        self._cookies.append(obj)

    def set_ghost_group(self, group: GhostGroup):
        self.ghostGroup = group

    def get_ghost_group(self) -> GhostGroup:
        return self.ghostGroup

    def add_powerup(self, obj: GameObject):
        self._game_objects.append(obj)
        self._powerups.append(obj)

    def activate_powerup(self):
        self.ghostGroup.reset_points()
        self.ghostGroup.start_freight()

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
        self._hero.set_position(Position(TILE_SIZE, TILE_SIZE))
        self._hero.set_direction(Direction.NONE)
        if self._lives == 0: self.end_game()

    def display_text(self, text, in_position=(32, 0), in_size=30):
        font = pygame.font.SysFont('Arial', in_size)
        text_surface = font.render(text, False, (255, 255, 255))
        self._screen.blit(text_surface, in_position)

    def add_wall(self, obj: Wall):
        self.add_game_object(obj)
        self._walls.append(obj)

    def get_walls(self):
        return self._walls

    def get_cookies(self):
        return self._cookies

    def get_powerups(self):
        return self._powerups

    def get_game_objects(self):
        return self._game_objects

    def add_hero(self, in_hero):
        self.add_game_object(in_hero)
        self._hero = in_hero

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True

            if event.type == self._mode_switch_event:
                self.handle_mode_switch()

            if event.type == self._pakupaku_event:
                if self._hero is None: break
                self._hero.mouth_open = not self._hero.mouth_open

        pressed = pygame.key.get_pressed()
        if self._hero is None: return
        if pressed[pygame.K_UP]:
            self._hero.set_direction(Direction.UP)
        elif pressed[pygame.K_LEFT]:
            self._hero.set_direction(Direction.LEFT)
        elif pressed[pygame.K_DOWN]:
            self._hero.set_direction(Direction.DOWN)
        elif pressed[pygame.K_RIGHT]:
            self._hero.set_direction(Direction.RIGHT)
