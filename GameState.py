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
        self._score_ghost_eaten = 400
        self._score_powerup_pickup = 50
        self._mouth_open_close_event = pygame.USEREVENT + 1

    def tick(self, in_fps: int):
        """
        ensures uninterrupted game operation by controlling the updating of game state and its display on the screen,
        making it a key element for players and the implementation of the game itself
        """
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
        """
        calculates the corresponding coordinates in the maze by dividing the x and y values ​​by the size of one tile
        (specified as self.TILE_SIZE) and returns the result in the form of a Position object.
        """
        return Position(int(coordinates[0] / self.TILE_SIZE), int(coordinates[1] / self.TILE_SIZE))

    def translate_maze_to_screen(self, coordinates: Position | tuple[int, int]):
        """
        takes the coordinates of a point in the maze (again, as an (x, y) tuple or a Position object)
        and translates them to the corresponding coordinates on the screen by multiplying the x and y values
        by the size of one tile (self.TILE_SIZE) and returns the result in the form of the Position object
        """
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
        """
        The add_powerup and activate_powerup methods are responsible for adding a power-up to the game and activating its effect, respectively
        """
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
        """
        methods add_score(self, in_score: int), end_game(self) group the functionality related to managing
        the player's score and ending the game, allowing you to conveniently manage these aspects of the game from one place
        """
        self._score += in_score

    def end_game(self):
        if self._hero in self._game_objects:
            self._game_objects.remove(self._hero)
        self._hero = None

    def kill_pacman(self):
        """
        methods kill_pacman(self), display_text(self, text, in_position=(32, 0), in_size=30),
        add_wall(self, obj: Wall) make it easy to control the main character, display text and add wall objects to the game
        """
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
        """
        provides user interaction with the game by handling various types of input, such as key presses and closing windows, 
        and also provides animation for the movement of the main character of the game
        """
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
