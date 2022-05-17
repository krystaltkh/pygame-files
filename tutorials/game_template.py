# Python template - for a new pygame project
# run with command + I
import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30 # Frames per second

# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialise pygame and create window
pygame.init() # initialises pygame
pygame.mixer.init() # initialises mixer: game has sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game") # what will appear at top of the window
clock = pygame.time.Clock() # handles speed and how fast we're going

all_sprites = pygame.sprite.Group() # put all sprites made into this group
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS) # tells pygame: if clock
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update: tells the sprites what to do
    all_sprites.update() # updates every sprite in the group

    # Draw / Render: creates each sprite
    screen.fill(BLACK) # fills screen with one colour(define above)
    all_sprites.draw(screen) # draws all sprites in the place <screen>
    # AFTER drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
