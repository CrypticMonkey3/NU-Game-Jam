import pygame
from pygame.locals import *

pygame.init()
FPS_CLOCK = pygame.time.Clock()


class Cat:
    def __init__(self):
        ...


class Game:
    def __init__(self):
        self.__running = True
        # self.__surface = pygame.display.set_mode(FULLSCREEN)

    def __check_events(self):
        ...

    def __process(self):
        ...

    def run(self) -> None:
        while self.__running:
            ...


if __name__ == "__main__":
    game = Game()
    game.run()
