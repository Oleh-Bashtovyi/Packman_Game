import pygame
from MazeController import *
from Constants import *
from GameState import *

# TODO
# - Вся логіка запуску в нас буде тут.
# - Будь ласка, робіть все в окремих гілках, а не в гілці develop.
# - Будь ласка, не робіть merge без мого відома. Робіть pull request
#   В github репозиторії. Я спочатку подивлюсь і потім виконаю його, якщо не буде проблем.
#   Коміти можете робити без мого відома. Робіть скіки треба, але лише в своїх гілках.
# - Ваша ціль: GameState, MazeController, Pacman, зчиування лабіринту, обробка подій підбору powerup\apple.
# - Привиди знаходяться в ghost group, в якій треба викликати методи оновлення. але вона поки має пустих привидів.


if __name__ == "__main__":
    mazeController = MazeController()
    mazeController.read_maze(MAZE)
    game_state = GameState(mazeController)

    for i, row in enumerate(MAZE):
        for j, column in enumerate(row):
            if MAZE[i][j] == "X":
                vect = translate_maze_to_screen((i, j))
                wall = Wall(game_state, vect)
                game_state.add_wall(wall)
            elif MAZE[i][j] == "P":
                vect = translate_maze_to_screen((i, j))
                powerup = Powerup(game_state, vect)
                game_state.add_powerup(powerup)
            else:
                vect = translate_maze_to_screen((i, j))
                apple = Apple(game_state, vect)
                game_state.add_apple(apple)

    pacman = Hero(game_state, Position(2, 2))
    ghostGroup = GhostGroup(game_state, pacman,
                            Position(15, 13), Position(2, 27),
                            Position(15, 16), Position(2, 2),
                            Position(16, 13), Position(30, 2),
                            Position(16, 16), Position(30, 27))
    game_state.add_hero(pacman)
    game_state.set_ghost_group(ghostGroup)

    game_state.tick(120)
