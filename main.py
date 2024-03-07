from pygame.locals import *
import pygame

pygame.init()
FPS_CLOCK = pygame.time.Clock()
FPS = 60


class Sprite:
    def __init__(self, surface: pygame.Surface, image_dir: str):
        self._surface = surface
        self._image = pygame.image.load(image_dir).convert_alpha(surface)


class Cat(Sprite):
    def __init__(self, surface: pygame.Surface, image_dir: str):
        super().__init__(surface, image_dir)


class Paddle(Sprite):
    def __init__(self, surface: pygame.Surface, image_dir: str):
        super().__init__(surface, image_dir)


class Ball(Sprite):
    def __init__(self, surface: pygame.Surface, image_dir: str):
        super().__init__(surface, image_dir)


class Game:
    def __init__(self):
        self.__running = True
        self.__surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        self.__cat = Cat(self.__surface, "Graphics/cat.png")
        self.__paddle = Paddle(self.__surface, "Graphics/bat.png")
        self.__ball = Ball(self.__surface, "Graphics/ball.png")

    def __check_events(self) -> None:
        """
        Checks any pygame events that occur.
        """
        event = pygame.event.poll()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.__running = False

    def __process(self) -> None:
        """
        All the processes of the game occur inside this method.
        """
        self.__check_events()

    def run(self) -> None:
        """
        Method to call, in order to run the game
        """
        self.__surface.fill((255, 255, 255))
        pygame.display.update()

        while self.__running:
            self.__process()
            FPS_CLOCK.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
