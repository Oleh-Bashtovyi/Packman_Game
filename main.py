import argparse
import Constants
import MazeController
from GameState import *

#метод призначений для обробки аргументів командного рядка, які можуть бути передані програмі при її запуску
def parse_args():
    """
    handles command-line arguments that can be passed to the program when it starts
    """
    parser = argparse.ArgumentParser(description='Pacman app')
    parser.add_argument('--fps', default=Constants.FPS, type=int, help='FPS')
    parser.add_argument('--sclf', default=Constants.SCALE_FACTOR, type=int, help='Scale factor')
    args = parser.parse_args()
    Constants.FPS = args.fps
    Constants.set_scale_factor(args.sclf)


def fill_gamestate(game_state: GameState, MAZE):
    for i, row in enumerate(MAZE):
        for j, column in enumerate(row):
            vect = Constants.translate_maze_to_screen((j, i))
            if MAZE[i][j] == "X":
                wall = Wall(game_state, vect)
                game_state.add_wall(wall)
            elif MAZE[i][j] == "P":
                powerup = Powerup(game_state, vect, Constants.POWERUP_SIZE)
                game_state.add_powerup(powerup)
            else:
                apple = Apple(game_state, vect, Constants.APPLE_SIZE)
                game_state.add_apple(apple)


#цей код встановлює основи гри та починає її виконання, створюючи об'єкти гри, додаючи їх до головного об'єкту game_state та запускаючи головний цикл гри
if __name__ == "__main__":
    """
    sets up the game framework and starts the game by creating game objects,
    adding them to the main game_state object, and starting the main game loop
    """
    parse_args()
    MAZE = Constants.MAZE
    mzController = MazeController.MazeController()
    mzController.read_maze(MAZE)
    game_state = GameState(Constants.TILE_SIZE, Constants.MAZE_HEIGHT, Constants.MAZE_WIDTH)

    fill_gamestate(game_state, MAZE)

    # for i, row in enumerate(MAZE):
    #     for j, column in enumerate(row):
    #         vect = Constants.translate_maze_to_screen((j, i))
    #         if MAZE[i][j] == "X":
    #             wall = Wall(game_state, vect)
    #             game_state.add_wall(wall)
    #         elif MAZE[i][j] == "P":
    #             powerup = Powerup(game_state, vect, Constants.POWERUP_SIZE)
    #             game_state.add_powerup(powerup)
    #         else:
    #             apple = Apple(game_state, vect, Constants.APPLE_SIZE)
    #             game_state.add_apple(apple)

    pacman = Hero(game_state, game_state.translate_maze_to_screen(Position(1, 1)),  Constants.PACMAN_SIZE)
    ghostGroup = GhostGroup(game_state, pacman, Constants.GHOST_SIZE, mzController,
                            Position(12, 13), Position(2, 27),
                            Position(13, 13), Position(2, 2),
                            Position(14, 13), Position(30, 2),
                            Position(15, 13), Position(30, 27))
    game_state.add_hero(pacman)
    game_state.set_ghost_group(ghostGroup)
    game_state.tick(Constants.FPS)
    print('finished!')
