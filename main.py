from pygame.locals import *
from pygame.font import Font
from typing import *
import pygame

pygame.init()
FPS_CLOCK = pygame.time.Clock()
FPS = 60
WHITE = (255, 255, 255)


class SpriteManager:
    def __init__(self):
        ...

    def __new__(cls):
        ...


class Sprite:
    def __init__(self, surface: pygame.Surface, image_dirs: List[str], init_pos: Tuple[int, int]):
        self._surface = surface
        self._image = pygame.image.load(image_dirs[0]).convert_alpha(surface)
        self._filler_surf = self._image.copy()
        self._filler_surf.fill(WHITE)
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
            self._surface.blit(self._filler_surf, self._rect)
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
        self.__ball = Ball(self.__surface, ["Graphics/ball.png", "Graphics/ball_outline.png"],
                           (self.__surface.get_width() // 2, self.__surface.get_height() // 2))
        # [(FPS text)]
        self.__text_objects: List[Any] = [()]  # acts as an array for all the text objects

    def __countdown(self) -> None:
        ...

    def __reset_game(self) -> None:
        """
        Resets the positions of the players and the ball to the centre of the screen.
        """
        self.__player1.draw(True)
        self.__player2.draw(True)
        self.__ball.draw(True)

    def __write2screen(self, message: str, font_dir: str, size: int, pos: Tuple[int, int],
                       color: Tuple[int, int, int]) -> None:
        """
        Writes a message with the passed parameters onto the screen.
        :param str message: Message to put on the screen
        :param str font_dir: Type of font we want to use
        :param int size: Font size
        :param Tuple[int, int] pos: Where on the screen we want to place the message
        :param Tuple[int, int, int] color: The colour of the text
        """
        if self.__text_objects[0]:
            self.__text_objects[0][0].fill(WHITE)
            self.__surface.blit(self.__text_objects[0][0], self.__text_objects[0][1])
            pygame.display.update(Rect(self.__text_objects[0][1][0], self.__text_objects[0][1][1],
                                       self.__text_objects[0][0].get_width(),
                                       self.__text_objects[0][0].get_height()))

        font_surf = Font(font_dir, size).render(message, False, color).convert_alpha(self.__surface)
        pos = (self.__surface.get_width() + pos[0] - font_surf.get_width() if pos[0] < 0 else pos[0],
               self.__surface.get_height() + pos[1] - font_surf.get_height() if pos[1] < 0 else pos[1])
        self.__surface.blit(font_surf, pos)
        pygame.display.update(Rect(pos[0], pos[1], font_surf.get_width(), font_surf.get_height()))
        self.__text_objects[0] = (font_surf, pos)

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
            self.__write2screen(f"{FPS_CLOCK.get_fps():0.2f} FPS", "Fonts/Arcadepix.TTF", 16, (-5, 5), (0, 0, 0))
            FPS_CLOCK.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
