from GameObjects import *
from Hero import *
from Ghosts import *


class GameState:
    def __init__(self, tile_size, maze_height, maze_width):
        pygame.init()
        self.SCREEN_WIDTH = tile_size * maze_width
        self.SCREEN_HEIGHT = tile_size * maze_height
        self.TILE_SIZE = tile_size
        self.TILE_HALF = int(tile_size / 2)
        self._screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self._clock = pygame.time.Clock()
        self._done = False
        self._won = False
        self._game_objects = []
        self._walls = []
        self._cookies = []
        self._powerups = []
        self._ghosts = []
        self._hero: Hero = None
        self._ghost_group: GhostGroup = None
        self._lives = 6
        self._score = 0
        self._mouth_open_close_event = pygame.USEREVENT + 1

    def tick(self, in_fps: int):
        black = (0, 0, 0)
        self._ghost_group.start_scatter()
        pygame.time.set_timer(self._mouth_open_close_event, 200)  # open close mouth
        while not self._done:

            dt = self._clock.tick(in_fps) / 1000.0
            self._ghost_group.tick(dt)

            if self._hero is not None:
                self._hero.tick(dt)

            for obj in self._game_objects:
                obj.draw()
            self._ghost_group.draw()

            self.display_text(f"[Score: {self._score}]  [Lives: {self._lives}]")

            if self._hero is None:
                self.display_text("YOU DIED", (self.SCREEN_WIDTH / 2 - 256, self.SCREEN_HEIGHT / 2 - 256), 100)
            if self.get_won():
                self.display_text("YOU WON", (self.SCREEN_WIDTH / 2 - 256, self.SCREEN_HEIGHT / 2 - 256), 100)
            pygame.display.flip()
            self._clock.tick(in_fps)
            self._screen.fill(black)
            self._handle_events()
        print("Game over")

    def get_surface(self):
        return self._screen

    def translate_screen_to_maze(self, coordinates: Position | tuple[int, int]):
        return Position(int(coordinates[0] / self.TILE_SIZE), int(coordinates[1] / self.TILE_SIZE))

    def translate_maze_to_screen(self, coordinates: Position | tuple[int, int]):
        return Position(coordinates[0] * self.TILE_SIZE, coordinates[1] * self.TILE_SIZE)

    def add_game_object(self, obj: GameObject):
        self._game_objects.append(obj)

    def add_apple(self, obj: GameObject):
        self._game_objects.append(obj)
        self._cookies.append(obj)

    def set_ghost_group(self, group: GhostGroup):
        self._ghost_group = group

    def get_ghost_group(self) -> GhostGroup:
        return self._ghost_group

    def add_powerup(self, obj: GameObject):
        self._game_objects.append(obj)
        self._powerups.append(obj)

    def activate_powerup(self):
        self._ghost_group.reset_points()
        self._ghost_group.start_freight()

    def set_won(self):
        self._won = True

    def get_won(self):
        return self._won

    def add_score(self, in_score: int):
        self._score += in_score

    def end_game(self):
        if self._hero in self._game_objects:
            self._game_objects.remove(self._hero)
        self._hero = None

    def kill_pacman(self):
        self._lives -= 1
        self._hero.set_position(Position(self.TILE_SIZE, self.TILE_SIZE))
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

            if event.type == self._mouth_open_close_event:
                if self._hero is None:
                    break
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
