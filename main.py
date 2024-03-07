from pygame.locals import *
from typing import *
import pygame

pygame.init()
FPS_CLOCK = pygame.time.Clock()
FPS = 60


class Sprite:
    def __init__(self, surface: pygame.Surface, image_dirs: List[str], init_pos: Tuple[int, int]):
        self._surface = surface
        self._image = pygame.image.load(image_dirs[0]).convert_alpha(surface)
        self._filler_surf = self._image.copy()
        self._filler_surf.fill((255, 255, 255))
        self._start_pos = init_pos

        self._image_outline = image_dirs[1]
        if image_dirs[1]:
            self._image_outline = pygame.image.load(image_dirs[1]).convert_alpha(surface)

        self._rect = Rect(init_pos[0], init_pos[1], self._image.get_width(), self._image.get_height())

    def move_pos(self, x: int, y: int):
        """
        Moves the position of where the object is drawn on the screen
        """
        # remove the previous positioned object from the screen
        self._surface.blit(self._filler_surf, self._rect)
        pygame.display.update(self._rect)

        self._rect = Rect(  # changes the rect of the object, whilst ensuring it's in the screen
            max(0, min(self._rect[0] + x, self._surface.get_width() - self._rect.width)),
            max(0, min(self._rect[1] + y, self._surface.get_height() - self._rect.height)),
            self._image.get_width(),
            self._image.get_height()
        )

    def draw(self, outline: bool = False):
        """
        Draws the sprite onto the main surface.
        :param bool outline: Whether we are drawing the sprites outline or not.
        """
        self._surface.blit(self._image, self._rect)
        if outline and self._image_outline:
            self._surface.blit(self._image_outline, self._rect)

        # only updating a part of the screen for optimal performance.
        pygame.display.update(self._rect)


class Cat(Sprite):
    def __init__(self, surface: pygame.Surface, image_dirs: List[str], init_pos: Tuple[int, int]):
        super().__init__(surface, image_dirs, init_pos)


class Player(Sprite):
    def __init__(self, surface: pygame.Surface, image_dirs: List[str], init_pos: Tuple[int, int]):
        super().__init__(surface, image_dirs, init_pos)
        # --- Rotate paddles --- #
        self._image = pygame.transform.rotate(self._image, 90)
        self._image_outline = pygame.transform.rotate(self._image_outline, 90)
        self._filler_surf = pygame.transform.rotate(self._filler_surf, 90)
        self._rect = Rect(self._rect[0], self._rect[1], self._image.get_width(), self._image.get_height())

        self.__score = 0


class Ball(Sprite):
    def __init__(self, surface: pygame.Surface, image_dirs: List[str], init_pos: Tuple[int, int]):
        super().__init__(surface, image_dirs, init_pos)


class Game:
    def __init__(self):
        self.__running = True
        self.__surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        self.__cat = Cat(self.__surface, ["Graphics/cat.png", ""], (0, 0))
        self.__player1 = Player(self.__surface, ["Graphics/bat.png", "Graphics/bat_outline.png"],
                                (50, self.__surface.get_height() // 2))
        self.__player2 = Player(self.__surface, ["Graphics/bat.png", "Graphics/bat_outline.png"],
                                (self.__surface.get_width() - 50, self.__surface.get_height() // 2))
        self.__ball = Ball(self.__surface, ["Graphics/ball.png", "Graphics/ball_outline.png"], (0, 0))

    def __reset_game(self) -> None:
        """
        Resets the positions of the players and the ball to the centre of the screen.
        """
        self.__player1.draw(True)
        self.__player2.draw(True)

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
        self.__reset_game()

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
