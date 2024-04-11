import argparse
import Constants
import MazeController
from GameState import *


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


def fill_gamestate_with_static_objects(game_state: GameState, MAZE):
    for i, row in enumerate(MAZE):
        for j, column in enumerate(row):
            vect = game_state.translate_maze_to_screen((j, i))
            if MAZE[i][j] == "X":
                wall = Wall(game_state, vect)
                game_state.add_wall(wall)
            elif MAZE[i][j] == "U":
                powerup = Powerup(game_state, vect, Constants.POWERUP_SIZE)
                game_state.add_powerup(powerup)
            else:
                apple = Apple(game_state, vect, Constants.APPLE_SIZE)
                game_state.add_apple(apple)


if __name__ == "__main__":
    """
    sets up the game framework and starts the game by creating game objects,
    adding them to the main game_state object, and starting the main game loop
    """
    parse_args()
    MAZE = Constants.MAZE
    game_state = GameState(Constants.TILE_SIZE, Constants.MAZE_HEIGHT, Constants.MAZE_WIDTH)

    fill_gamestate_with_static_objects(game_state, MAZE)
    pacman = Hero(game_state, game_state.translate_maze_to_screen(Position(1, 1)), Constants.PACMAN_SIZE)

    mzController = MazeController.MazeController()
    mzController.read_maze(MAZE)
    ghost_group = GhostGroup(game_state, mzController)

    ghosts_size = Constants.GHOST_SIZE

    pinky_spawn_pos = Position(12, 13)
    pinky_scatter_pos = Position(2, 27)
    pinky_screen_pos = game_state.translate_maze_to_screen(Position(12, 13))
    pinky = PinkGhost(game_state, pinky_screen_pos, pinky_spawn_pos, pinky_scatter_pos, ghosts_size, pacman)

    red_spawn_pos = Position(13, 13)
    red_scatter_pos = Position(2, 2)
    red_screen_pos = game_state.translate_maze_to_screen(Position(13, 13))
    red = RedGhost(game_state, red_screen_pos, red_spawn_pos, red_scatter_pos, ghosts_size, pacman)



    # ghostGroup = GhostGroup(game_state, pacman, Constants.GHOST_SIZE, mzController,
    #                         Position(12, 13), Position(2, 27),
    #                         Position(13, 13), Position(2, 2),
    #                         Position(14, 13), Position(30, 2),
    #                         Position(15, 13), Position(30, 27))

    ghost_group.add_ghost(pinky)
    ghost_group.add_ghost(red)
    game_state.add_hero(pacman)
    game_state.set_ghost_group(ghost_group)
    game_state.tick(Constants.FPS)
    print('finished!')