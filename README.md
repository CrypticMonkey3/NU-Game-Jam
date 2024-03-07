# NU-Game-Jam
import pygame
import sys
# Initialize Pygame
pygame.init()
# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hello, Pygame!")
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a font object
font = pygame.font.Font(None, 36)

# Game objects
paddle_width = 10
paddle_height = 100
#the window is 300 so the middle is 300
player1 = pygame.Rect(50, 300 , paddle_width, paddle_height)
ball = pygame.Rect( 385 , 285 , 30 , 30 )

def handleInputs( ):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            #end if
        #end for
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= 1

        if keys[pygame.K_s] and player1.bottom < WINDOW_HEIGHT:
            player1.y += 1
#end handleEvent

def draw():
    window.fill(WHITE)
    pygame.draw.rect(window, (0, 0, 0), player1)

#end handle event

def gameLoop():
    """this is the main game loop. The function never really returns"""
# dont forget to indent this code.
while True:
    handleInputs()
    # Clear the screen
    draw()
    pygame.time.delay(10)

    mouse_pos = pygame.mouse.get_pos()
    # Render the text
    text = font.render(f"Hello, World! {mouse_pos}", True, BLACK)
    text_rect = text.get_rect(center=(mouse_pos[0],mouse_pos[1]))
    window.blit(text, text_rect)
    # Update the display
    pygame.display.update() #stops flickering effect
    #end of while.
#end of function main
gameLoop() #actually call the function gameLoop
