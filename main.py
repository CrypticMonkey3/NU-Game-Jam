from pygame.locals import *
from pygame.font import Font
from typing import *
import pygame
from datetime import datetime

pygame.init()
FPS_CLOCK = pygame.time.Clock()
FPS = 60
WHITE = (255, 255, 255)


class SpriteManager:
    __instance = None

    def __init__(self):
        self.__object_pool: Dict[str: List[object]] = {}

    def add_objects(self, obj_label: str, obj, quantity: int = 1, *args) -> None:
        """
        Creates an x amount of objects and adds it to the pool of objects
        :param str obj_label: The label to give to the object
        :param obj: The type of object to create
        :param int quantity: The number of objects to create
        :return: None
        """
        self.__object_pool[obj_label] = [obj(*args) for _ in range(quantity)]

    @property
    def object_pool(self):
        return self.__object_pool

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.__instance = super(SpriteManager, cls).__new__(cls)

        return cls.__instance


class Text:
    def __init__(self, *args):
        self._surface: pygame.Surface = args[0]
        self._message: str = args[1]
        self._font_dir: str = args[2]
        self._size: int = args[3]
        self._pos: Tuple[int, int] = args[4]
        self._color: Tuple[int, int, int] = args[5]
        self._font_surf: pygame.Surface = Font(args[2], args[3]).render(args[1], False, args[5]).convert_alpha(args[0])

    def update_text(self, new_message: str) -> None:
        """
        Updates the text in the currently displayed text surface
        :param str new_message: The new message
        :return: None
        """
        self._font_surf.fill(WHITE)
        self.draw()

        self._font_surf = Font(self._font_dir, self._size).render(new_message, False, self._color).\
            convert_alpha(self._surface)
        self._message = new_message
        self.draw()

    def draw(self) -> None:
        """
        Blits the text onto the screen
        :return: None
        """
        screen_pos = (
            self._surface.get_width() + self._pos[0] - self._font_surf.get_width() if self._pos[0] < 0 else self._pos[0],
            self._surface.get_height() + self._pos[1] - self._font_surf.get_height() if self._pos[1] < 0 else self._pos[1]
        )
        self._surface.blit(self._font_surf, screen_pos)
        pygame.display.update(Rect(screen_pos[0], screen_pos[1], self._font_surf.get_width(), self._font_surf.get_height()))

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new_pos):
        self._pos = new_pos

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color: Union[Tuple[int, int, int], Tuple[int, int, int, int]]):
        self._color = new_color

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size: int):
        self._size = new_size
        self._font_surf = Font(self._font_dir, new_size).render(self._message, False, self.color).\
            convert_alpha(self._surface)

    @property
    def surface(self) -> pygame.Surface:
        return self._font_surf

    @property
    def message(self):
        return self._message


class Sprite:
    def __init__(self, *args):
        self._surface: pygame.Surface = args[0]
        self._image: pygame.Surface = pygame.image.load(args[1][0]).convert_alpha(args[0])
        self._filler_surf = self._image.copy()
        self._filler_surf.fill(WHITE)
        self._start_pos: Tuple[int, int] = args[2]

        self._image_outline = args[1][1]
        if args[1][1]:
            self._image_outline = pygame.image.load(args[1][1]).convert_alpha(args[0])

        self._rect = Rect(args[2][0], args[2][1], self._image.get_width(), self._image.get_height())

    def move_pos(self, x: int, y: int) -> None:
        """
        Moves the position of where the object is drawn on the screen
        :param int x: x modifier
        :param int y: y modifier
        :return: None
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

    def draw(self, outline: bool = False) -> None:
        """
        Draws the sprite onto the main surface.
        :param bool outline: Whether we are drawing the sprites outline or not.
        :return: None
        """
        self._surface.blit(self._image, self._rect)
        if outline and self._image_outline:
            self._surface.blit(self._filler_surf, self._rect)
            self._surface.blit(self._image_outline, self._rect)

        # only updating a part of the screen for optimal performance.
        pygame.display.update(self._rect)

    @property
    def surface(self):
        """
        Returns the sprite's surface
        """
        return self._image


class Cat(Sprite):
    def __init__(self, *args):
        super().__init__(*args)


class Player(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        # --- Rotate paddles --- #
        self._image = pygame.transform.rotate(self._image, 90)
        self._image_outline = pygame.transform.rotate(self._image_outline, 90)
        self._filler_surf = pygame.transform.rotate(self._filler_surf, 90)
        self._rect = Rect(self._rect[0], self._rect[1], self._image.get_width(), self._image.get_height())

        self.__score = 0


class Ball(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.__speed = 1


class Game:
    def __init__(self):
        self.__running = True
        self.__surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        self.__timer = datetime(2000, 1, 1, 0, 0, 0, 0)
        self.__countdown_values = ["3", "2", "1", "GO!", ""]

        self.__sprite_manager = SpriteManager()
        self.__sprite_manager.add_objects("Cat", Cat, 1, self.__surface, ["Graphics/cat.png", ""], (0, 0))

        self.__sprite_manager.add_objects("Player", Player, 2, self.__surface,
                                          ["Graphics/bat.png", "Graphics/bat_outline.png"],
                                          (0, 0))

        self.__sprite_manager.add_objects("Ball", Ball, 1, self.__surface,
                                          ["Graphics/ball.png", "Graphics/ball_outline.png"],
                                          (0, 0))

        self.__sprite_manager.add_objects("Text", Text, 2, self.__surface,
                                          "", "Fonts/Arcadepix.TTF", 16, (0, 0), (0, 0, 0))
        self.__sprite_manager.object_pool["Text"][0].pos = (-5, 5)
        self.__sprite_manager.object_pool["Text"][1].color = (184, 184, 184)
        self.__sprite_manager.object_pool["Text"][1].size = 256
        self.__sprite_manager.object_pool["Text"][1].pos = ((self.__surface.get_width() // 2) - (self.__sprite_manager.object_pool["Text"][1].surface.get_width() // 2), 100)

    def __countdown(self) -> None:
        """
        Countdown until game restarts.
        :return: None
        """
        # if a second has elapsed
        if (datetime.now() - self.__timer).total_seconds() > 1:
            self.__sprite_manager.object_pool["Text"][1].update_text(self.__countdown_values[self.__countdown_values.index(self.__sprite_manager.object_pool["Text"][1].message) + 1])
            self.__timer = datetime.now()

    def __reset_game(self) -> None:
        """
        Resets the positions of the players and the ball to the centre of the screen.
        :return: None
        """
        # --- Align the player bats' centres to the centre of the screen.
        self.__sprite_manager.object_pool["Player"][0].move_pos(50,
                                                                (self.__surface.get_height() // 2) - (self.__sprite_manager.object_pool["Player"][0].surface.get_height() // 2))
        self.__sprite_manager.object_pool["Player"][1].move_pos(self.__surface.get_width() - 50,
                                                                (self.__surface.get_height() // 2) - (self.__sprite_manager.object_pool["Player"][1].surface.get_height() // 2))

        self.__sprite_manager.object_pool["Ball"][0].move_pos(self.__surface.get_width() // 2,
                                                              self.__surface.get_height() // 2)

        self.__sprite_manager.object_pool["Player"][0].draw(True)  # Player 1
        self.__sprite_manager.object_pool["Player"][1].draw(True)  # Player 2
        self.__sprite_manager.object_pool["Ball"][0].draw(True)  # Ball 1

        self.__sprite_manager.object_pool["Text"][1].update_text("3")  # kickstart the countdown
        self.__timer = datetime.now()

    def __check_events(self) -> None:
        """
        Checks any pygame events that occur.
        :return: None
        """
        event = pygame.event.poll()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.__running = False

    def __process(self) -> None:
        """
        All the processes of the game occur inside this method.
        :return: None
        """
        self.__check_events()
        self.__sprite_manager.object_pool["Text"][0].update_text(f"{FPS_CLOCK.get_fps():0.2f} FPS")  # update FPS

        if self.__sprite_manager.object_pool["Text"][1].message:
            self.__countdown()

        elif not self.__sprite_manager.object_pool["Text"][1].message:  # quicker then else
            # run the game
            print("game running")
            ...

    def run(self) -> None:
        """
        Method to call, in order to run the game
        :return: None
        """
        self.__surface.fill((255, 255, 255))
        self.__reset_game()
        pygame.display.update()

        while self.__running:
            self.__process()
            FPS_CLOCK.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
