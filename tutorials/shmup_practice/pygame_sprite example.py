# Python template - for a new pygame project
# run with command + I
import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30 # Frames per second

# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up assets (folders that contain graphics and sound files)
# 1. Create a folder in the path of the code first. Name it (in this case,) "img"
# Windows: "C:\Users\krystaltay\Downloads"
# Mac: "/Users/krystaltay/Downloads"
# 2. move the graphics to this "img" folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # SUPER IMPORTANT LINE
        # Surface((pixels, pixels)) -> Surface is a place you can draw on on Pygame
        self.image = pygame.image.load(os.path.join(img_folder, "p1_jump.png")).convert()
        # .convert() is SUPER IMPORTANT!! converts image into a form pygame can use more efficiently
        #self.image.fill(GREEN) # defined above
        self.image.set_colorkey(BLACK) # colour to ignore on the image (cos as a transparent vector it still has a black rectangle bg)
        self.rect = self.image.get_rect() # rectangle that enclose the sprite
        self.rect.center = (WIDTH / 2, HEIGHT / 2) # put player in the centre
        self.y_speed = 5

    def update(self):
        self.rect.x += 5 # everytime the game updates,
                         # the rectangle moves 5 spaces to the right
        self.rect.y += self.y_speed # character moves down
        # to prevent rectangle from moving off from the screen,

        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -5 # char moves back up
        if self.rect.top < 200:
            self.y_speed = 5 # char moves back down
        
        # do this to loop and make the rectangle look like its moving full circle
        if self.rect.left > WIDTH: # if left space of rectangle more than WIDTH
            self.rect.right = 0
        
# initialise pygame and create window
pygame.init() # initialises pygame
pygame.mixer.init() # initialises mixer: game has sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game") # what will appear at top of the window
clock = pygame.time.Clock() # handles speed and how fast we're going

all_sprites = pygame.sprite.Group() # put all sprites made into this group
player = Player()
all_sprites.add(player) # adds player object to group

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
    screen.fill(BLUE) # fills screen with one colour(define above)
    all_sprites.draw(screen) # draws all sprites in the place <screen>
    # AFTER drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
