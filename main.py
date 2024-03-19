from pygame.locals import *
from pygame.font import Font
from typing import *
import pygame
from datetime import datetime
from random import choice
from winsound import Beep

pygame.init()
FPS_CLOCK = pygame.time.Clock()
FPS = 60
WHITE = (255, 255, 255)
FADED_BLACK = (184, 184, 184)


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


class CollisionManager:
    @staticmethod
    def check_bat_ball(bat_pool: List[Any], ball_pool: List[Any]) -> None:
        """
        Checks the collisions between a bat pool and a ball pool.
        :param List[Any] bat_pool: a list of Bat objects
        :param List[Any] ball_pool: a list of Ball objects to compare against
        :return: None
        """
        # get a list of bats and balls that have collided with each other
        collisions = [(bat_pool[ball.rect.collidelist(bat_pool)], ball) for ball in ball_pool if ball.rect.collidelist(bat_pool) != -1]
        for collision in collisions:  # iterate through each collision.
            if collision[0].rect.colliderect(Rect(collision[1].prev_rect[0], collision[1].prev_rect[1] + collision[1].velocity[1], collision[1].prev_rect[2], collision[1].prev_rect[3])):
                # moves the ball to either side of the bat depending on the direction, then moves the ball a suitable
                # distance away from the top or bottom of the bat depending on the direction of the ball
                inverse_y = -collision[1].direction[1] if collision[1].direction[1] != collision[0].direction[0] else collision[1].dsssasswisrection[1]
                collision[1].move_pos(collision[0].rect.left - collision[1].rect.right if collision[1].direction[0] < 0 else collision[0].rect.right - collision[1].rect.left, (min((collision[0].rect.bottom - collision[1].rect.top), abs(collision[0].rect.top - collision[1].rect.bottom)) * inverse_y))
                collision[1].direction = (collision[1].direction[0], inverse_y)

            # check if the previous rect of the ball with a modified x collides with the bat.
            elif collision[0].rect.colliderect(Rect(collision[1].prev_rect[0] + collision[1].velocity[0], collision[1].prev_rect[1], collision[1].prev_rect[2], collision[1].prev_rect[3])):
                # set ball position on the edge of the bat
                collision[1].move_pos(collision[0].rect.right - collision[1].rect.left if collision[1].direction[0] < 0 else collision[0].rect.left - collision[1].rect.right, 0, False)
                collision[1].direction = (-collision[1].direction[0], collision[1].direction[1])  # changes direction

            Beep(551, 16)
            collision[1].speed += 1

    @staticmethod
    def check_ball_cat(ball_pool: List[Any], cat_pool: List[Any]):
        ...


class Text:
    def __init__(self, *args):
        self._surface: pygame.Surface = args[0]
        self._message: str = args[1]
        self._font_dir: str = args[2]
        self._size: int = args[3]
        self._pos: Tuple[int, int] = args[4]
        self._color: Tuple[int, int, int] = args[5]
        self._font_surf: pygame.Surface = Font(args[2], args[3]).render(args[1], False, args[5]).convert_alpha(args[0])

    def update_text(self, new_message: str, centralise: bool = False) -> None:
        """
        Updates the text in the currently displayed text surface
        :param str new_message: The new message
        :param bool centralise: Whether we need to centralise the text around the given position
        :return: None
        """
        self._font_surf.fill(WHITE)
        # if it was centralised before, good chance it will be again.
        self.draw(mod_x=(-self._font_surf.get_rect().centerx if centralise else 0))

        self._font_surf = Font(self._font_dir, self._size).render(new_message, False, self._color).\
            convert_alpha(self._surface)
        self._message = new_message
        self.draw(mod_x=(-self._font_surf.get_rect().centerx if centralise else 0))

    def draw(self, mod_x: int = 0, mod_y: int = 0) -> None:
        """
        Blits the text onto the screen
        :return: None
        """
        screen_pos = (
            mod_x + (self._surface.get_width() + self._pos[0] - self._font_surf.get_width() if self._pos[0] < 0 else self._pos[0]),
            mod_y + (self._surface.get_height() + self._pos[1] - self._font_surf.get_height() if self._pos[1] < 0 else self._pos[1])
        )
        self._surface.blit(self._font_surf, screen_pos)

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
        self._font_surf = Font(self._font_dir, new_size).render(self._message, False, self.color). \
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

        self._image_outline = args[1][1]
        if args[1][1]:
            self._image_outline = pygame.image.load(args[1][1]).convert_alpha(args[0])

        self._rect = Rect(args[2][0], args[2][1], self._image.get_width(), self._image.get_height())
        self._prev_rect = self._rect
        self._direction = (0, 0)
        self._base_speed = 0
        self._speed = 0

    def move_pos(self, x: int, y: int, update_prev_rect: bool = True) -> None:
        """
        Moves the position of where the object is drawn on the screen
        :param int x: x modifier
        :param int y: y modifier
        :param bool update_prev_rect: Whether we change the previous rect during a movement, only False for collisions.
        :return: None
        """
        # remove the previous positioned object from the screen
        self._surface.blit(self._filler_surf, self._rect)

        if update_prev_rect:
            self._prev_rect = self._rect

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

    @property
    def surface(self):
        """
        Returns the sprite's surface
        """
        return self._image

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction: Tuple[int, int]):
        self._direction = new_direction

    @property
    def base_speed(self):
        return self._base_speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed):
        self._speed = new_speed

    @property
    def rect(self):
        return self._rect

    @property
    def prev_rect(self):
        return self._prev_rect

    @property
    def velocity(self):
        return self._direction[0] * self._speed, self._direction[1] * self._speed


class Cat(Sprite):
    def __init__(self, *args):
        super().__init__(*args)

    def disappear_move(self, x: int, y: int) -> None:
        """
        Slowly shrinks the image from the screen, then moves the position elsewhere and reappears.
        :param int x: x-coordinate
        :param int y: y-coordinate
        :return: None
        """

    def appear(self) -> None:
        """
        Slowly enlarge the image to a particular size.
        :return: None
        """
        ...

    def rotate(self, degrees: int) -> None:
        """
        Rotate a cat by a certain amount of degrees.
        :param int degrees: The amount of degrees to rotate object.
        :return: None
        """
        ...


class Player(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        # --- Rotate paddles --- #
        self._image = pygame.transform.rotate(self._image, 90)
        self._image_outline = pygame.transform.rotate(self._image_outline, 90)
        self._filler_surf = pygame.transform.rotate(self._filler_surf, 90)
        self._rect = Rect(self._rect[0], self._rect[1], self._image.get_width(), self._image.get_height())

        self._base_speed = 7
        self._speed = 7
        self._direction = (0, 1)
        self.__score = 0

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, new_score):
        self.__score = new_score


class Ball(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self._base_speed = 3
        self._speed = 3
        self._direction = (choice([1, -1]), choice([1, -1]))

    def move_pos(self, x: int, y: int, update_prev_rect: bool = True) -> int:
        """
        The same functionality as in the parent class, but also checks if we hit screen boundaries.
        :return: int, which player has scored, 0 denoting that no one has scored yet.
        """
        super(Ball, self).move_pos(x, y, update_prev_rect)

        if self._rect[1] == 0 or self._rect[1] == self._surface.get_height() - self._rect.height:
            self._direction = (self._direction[0], -self._direction[1])
            Beep(441, 16)

        elif self._rect[0] == 0:
            return 2

        elif self._rect[0] == self._surface.get_width() - self._rect.width:
            return 1

        return 0


class Game:
    def __init__(self):
        self.__running = True
        self.__surface = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        self.__timer = datetime(2000, 1, 1, 0, 0, 0, 0)
        self.__countdown_values = ["3", "2", "1", "GO!", ""]

        self.__collision_manager = CollisionManager()
        self.__sprite_manager = SpriteManager()
        self.__sprite_manager.add_objects("White Cat", Cat, 5, self.__surface, ["Graphics/cat.png", ""], (0, 0))

        for i in range(1, 3):  # repeats for stop - start number of players
            self.__sprite_manager.add_objects(f"Player{i}", Player, 1, self.__surface,
                                              ["Graphics/bat.png", "Graphics/bat_outline.png"],
                                              (0, 0))

        self.__sprite_manager.add_objects("Ball", Ball, 1, self.__surface,
                                          ["Graphics/ball.png", "Graphics/ball_outline.png"],
                                          (0, 0))

        # Text 0: FPS, Text 1: Reset Countdown, Text 2: Player1 Score, Text3: Player2 Score, Text4: Exit Notice
        self.__sprite_manager.add_objects("Text", Text, 5, self.__surface,
                                          "", "Fonts/Arcadepix.TTF", 16, (0, 0), (0, 0, 0))
        self.__sprite_manager.object_pool["Text"][0].pos = (-5, 5)
        self.__sprite_manager.object_pool["Text"][1].size = 256
        self.__sprite_manager.object_pool["Text"][1].pos = ((self.__surface.get_width() // 2) - (self.__sprite_manager.object_pool["Text"][1].surface.get_width() // 2), 100)
        self.__sprite_manager.object_pool["Text"][2].size = 128
        self.__sprite_manager.object_pool["Text"][2].pos = ((self.__surface.get_width() // 4) - (self.__sprite_manager.object_pool["Text"][2].surface.get_width() // 2), 200)
        self.__sprite_manager.object_pool["Text"][3].size = 128
        self.__sprite_manager.object_pool["Text"][3].pos = (((self.__surface.get_width() // 4) * 3) - (self.__sprite_manager.object_pool["Text"][3].surface.get_width() // 2), 200)
        self.__sprite_manager.object_pool["Text"][4].pos = (5, 5)

    def __countdown(self) -> None:
        """
        Countdown until game restarts.
        :return: None
        """
        # if a second has elapsed
        if (datetime.now() - self.__timer).total_seconds() > 1:
            self.__sprite_manager.object_pool["Text"][1].update_text(self.__countdown_values[self.__countdown_values.index(self.__sprite_manager.object_pool["Text"][1].message) + 1], True)
            self.__timer = datetime.now()

            # have to chain if here so we can change the colour of the scores once, instead of setting it during
            # every cycle
            if not self.__sprite_manager.object_pool["Text"][1].message:
                self.__sprite_manager.object_pool["Text"][2].color = (0, 0, 0)
                self.__sprite_manager.object_pool["Text"][3].color = (0, 0, 0)

    def __reset_game(self) -> None:
        """
        Resets the positions of the players and the ball to the centre of the screen.
        :return: None
        """
        # --- Re-aligns the player bats' centres to the centre of the screen, no matter where it is
        self.__sprite_manager.object_pool["Player1"][0].move_pos(50 - self.__sprite_manager.object_pool["Player1"][0].rect.left,
                                                                 (self.__surface.get_height() // 2) - (self.__sprite_manager.object_pool["Player1"][0].surface.get_height() // 2) - self.__sprite_manager.object_pool["Player1"][0].rect.top)
        self.__sprite_manager.object_pool["Player2"][0].move_pos(self.__surface.get_width() - 50 - self.__sprite_manager.object_pool["Player2"][0].rect.left,
                                                                 (self.__surface.get_height() // 2) - (self.__sprite_manager.object_pool["Player2"][0].surface.get_height() // 2) - self.__sprite_manager.object_pool["Player2"][0].rect.top)

        self.__sprite_manager.object_pool["Ball"][0].move_pos((self.__surface.get_width() // 2) - self.__sprite_manager.object_pool["Ball"][0].rect.left,
                                                              (self.__surface.get_height() // 2) - self.__sprite_manager.object_pool["Ball"][0].rect.top)

        self.__sprite_manager.object_pool["Player1"][0].draw(True)  # Player 1
        self.__sprite_manager.object_pool["Player2"][0].draw(True)  # Player 2
        self.__sprite_manager.object_pool["Ball"][0].draw(True)  # Ball 1

        self.__sprite_manager.object_pool["Ball"][0].speed = self.__sprite_manager.object_pool["Ball"][0].base_speed

        # --- kickstart the countdown
        self.__sprite_manager.object_pool["Text"][1].update_text("3", True)
        self.__timer = datetime.now()

        self.__sprite_manager.object_pool["Text"][2].color = FADED_BLACK
        self.__sprite_manager.object_pool["Text"][3].color = FADED_BLACK

    def __spawn_cats(self) -> None:
        """
        Randomly places a cat on a particular area of the screen.
        :return: None
        """
        # every 6 amount of seconds
        if (datetime.now() - self.__timer).total_seconds() > 6:
            # randomly choose a cat of varying probability, and make it appear at a random point on the screen.
            ...

    def __check_events(self) -> None:
        """
        Checks any pygame events that occur.
        :return: None
        """
        event = pygame.event.poll()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.__running = False

    def __check_inputs(self) -> None:
        """
        Checks for any peripheral inputs
        :return: None
        """
        keys = pygame.key.get_pressed()

        self.__sprite_manager.object_pool["Player1"][0].move_pos(0,
                                                                 self.__sprite_manager.object_pool["Player1"][0].velocity[1] * (-keys[K_w] + keys[K_s]))

        self.__sprite_manager.object_pool["Player2"][0].move_pos(0,
                                                                 self.__sprite_manager.object_pool["Player2"][0].velocity[1] * (-keys[K_UP] + keys[K_DOWN]))

    def __process(self) -> None:
        """
        All the processes of the game occur inside this method.
        :return: None
        """
        self.__check_events()
        self.__sprite_manager.object_pool["Text"][0].update_text(f"{FPS_CLOCK.get_fps():0.2f} FPS")  # update FPS
        self.__sprite_manager.object_pool["Text"][2].update_text(f"{self.__sprite_manager.object_pool['Player1'][0].score:02d}", True)  # update Player 1's score
        self.__sprite_manager.object_pool["Text"][3].update_text(f"{self.__sprite_manager.object_pool['Player2'][0].score:02d}", True)  # update Player 2's score
        self.__sprite_manager.object_pool["Text"][4].update_text("Press (ESC) to EXIT")

        if self.__sprite_manager.object_pool["Text"][1].message:
            self.__countdown()

        elif not self.__sprite_manager.object_pool["Text"][1].message:  # else if not counting down, run the game
            self.__check_inputs()

            player_scored = self.__sprite_manager.object_pool["Ball"][0].move_pos(self.__sprite_manager.object_pool["Ball"][0].velocity[0], self.__sprite_manager.object_pool["Ball"][0].velocity[1])

            self.__sprite_manager.object_pool["Ball"][0].draw()  # Ball 1
            self.__sprite_manager.object_pool["Player1"][0].draw()  # Player 1
            self.__sprite_manager.object_pool["Player2"][0].draw()  # Player 2

            self.__collision_manager.check_bat_ball(self.__sprite_manager.object_pool["Player1"], self.__sprite_manager.object_pool["Ball"])
            self.__collision_manager.check_bat_ball(self.__sprite_manager.object_pool["Player2"], self.__sprite_manager.object_pool["Ball"])

            if player_scored != 0:
                self.__sprite_manager.object_pool[f"Player{player_scored}"][0].score += 1
                Beep(600, 32)
                self.__reset_game()

    def run(self) -> None:
        """
        Method to call, in order to run the game
        :return: None
        """
        self.__surface.fill((255, 255, 255))
        self.__reset_game()

        while self.__running:
            self.__process()
            FPS_CLOCK.tick(FPS)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
