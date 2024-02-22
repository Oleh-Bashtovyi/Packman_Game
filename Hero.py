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
        self.open = pygame.image.load("images/pacman_open.png")
        self.closed = pygame.image.load("images/pacman_close.png")
        self.image = self.open
        self.mouth_open = True

    ###############################


    def set_direction(self, dir):
        self.bufferDirection = dir