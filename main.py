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
            vect = translate_maze_to_screen((j, i))
            if MAZE[i][j] == "X":
                wall = Wall(game_state, vect)
                game_state.add_wall(wall)
            elif MAZE[i][j] == "P":
                powerup = Powerup(game_state, vect)
                game_state.add_powerup(powerup)
            else:
                apple = Apple(game_state, vect)
                game_state.add_apple(apple)

    pacman = Hero(game_state, translate_maze_to_screen(Position(1, 1)))
    ghostGroup = GhostGroup(game_state, pacman,
                            Position(12, 13), Position(2, 27),
                            Position(13, 13), Position(2, 2),
                            Position(14, 13), Position(30, 2),
                            Position(15, 13), Position(30, 27))
    game_state.add_hero(pacman)
    game_state.set_ghost_group(ghostGroup)

    game_state.tick(240)
