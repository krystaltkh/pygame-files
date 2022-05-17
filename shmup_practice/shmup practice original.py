# Shmup game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
 
import pygame
import random
from os import path
import sys # used to quit the whole application

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60 # Action Game -> Higher FPS -> Faster
POWERUP_TIME = 5000 # 5000ms = 5s

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
pygame.display.set_caption("Shmup! :)") # what will appear at top of the window
clock = pygame.time.Clock() # handles speed and how fast we're going

font_name = pygame.font.match_font('arial') # pygame searches your computer for the font closest to 'arial'
def draw_text(surf, text, size, x, y): # surface you wanna draw on, string, font, location(x,y)
    # better to use a generic font so it works across all platforms
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) # True: anti-alias font, False: alias font.
                                                  # (WHITE): colour the word is in
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0 # prevents fill from going outside of rect bar
    # num of pixels the bar is:
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100)* BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    # fill of rect bar
    pygame.draw.rect(surf, GREEN, fill_rect)
    # outline of rect bar
    pygame.draw.rect(surf, WHITE, outline_rect, 2) # 2 => how wide the outline will be in pixels

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        # because each one was specified to be 25x19 below.
        # 30 gives each image a 5 pixel gap in between
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38)) # scales original image to size (width, height)
        self.image.set_colorkey(BLACK)
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()

        self.radius = 20
        # do the bottom to test the circle size of the sprite for clean collisions
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100 # sth like health

        # to hold down space bar and shoot: do this
        self.shoot_delay = 250 # in miliseconds
        self.last_shot = pygame.time.get_ticks() # keep track of what time you last shot
        #### end ####

        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1 # determines how many bullets to shoot
        self.power_time = pygame.time.get_ticks() # keeps track of time: when to drop back to power level 1

    def update(self):
        # timeout for powerups
        # pygame.time.get_ticks() - self.power_time = time now - time powerup was collected
        #if self.shield == 0:
        #    self.power = 1
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000: # 1000ms = 1s
            # after hiding for 1s,
            self.hidden = False # unhide
            # spawn location
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        # these tell the sprite that their speed is 0 unless a key is pressed
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        # can change keys to UP, DOWN, w, a, s, d, etc.
        # can change speed also so sprite moves faster
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        # self edited
        if keystate[pygame.K_UP]:
            self.speedy = -3
        if keystate[pygame.K_DOWN]:
            self.speedy = 3
        #### end ####

        # as long as space bar is held down & spaceship not hidden, cont shooting
        if keystate[pygame.K_SPACE] and not self.hidden:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # create walls at the sides:
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # create wall at the top and bottom:
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        # move player sprite to bottom of the screen, where there are no meteors
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image_orig = meteor_img => to pick one image only
        self.image_orig = random.choice(meteor_images)
        #self.image.fill(RED)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * .85 / 2)
        # do the bottom to test the circle size of the sprite for clean collisions
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        # range ensures mob appears somewhere between left and right of screen
        # or range(0, WIDTH - self.rect.width)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        # adding self.speedx makes mobs go diagonal
        self.speedx = random.randrange(-3, 3)

        self.rot = 0 # not rotating
        self.rot_speed = random.randrange(-8, 8) # how much the sprite rotates each time
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            # WRONG WAY of rotating: each rotation loses tiny amounts of information of the image:
            # self.image = pygame.transform.rotate(self.image, self.rot_speed)
            self.rot = (self.rot + self.rot_speed) % 360 # so that rotation is looped after 360º
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            # creates a new rectangle that fits the sprite each time it rotates, so it rotates about the centre
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            # so if mob sprite goes to the bottom, re-randomise to appear at the top
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y): # x & y parameters -> tells the bullet where to spawn from
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        #self.image.fill(YELLOW)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill() # deletes the sprite


class Pow(pygame.sprite.Sprite): # Power Up
    def __init__(self, center): # we want power up to randomly spawn from center of meteor
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5 # power up moves downwards

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill() # deletes the sprite


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size): # center: where to appear
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        # frame rate: how long do we wat btn each frame
        self.frame_rate = 75 # smaller number => faster

    def update(self):
        now = pygame.time.get_ticks()
        # check if enough time has passed to change the image
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]): # all images of expl run already
                self.kill() # kills the expl animation
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    # draw_text(surf, text, size, x, y)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys to move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            # check for quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # pygame.KEYDOWN: game starts when key is still pressed down
            # pygame.KEYUP: game starts when player lets go of the pressed key
            if event.type == pygame.KEYUP:
                waiting = False

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "spaceshooter_bg.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med3.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue16.png")).convert()
# to load more than one image:
meteor_images = []
meteor_list = ['meteorBrown_small2.png', 'meteorBrown_big2.png', 'meteorBrown_tiny2.png',
               'meteorBrown_big4.png', 'meteorBrown_med3.png', 'meteorBrown_med1.png',
               'meteorBrown_small1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
### end ###

explosion_anim = {} # dictionary
explosion_anim['lg'] = [] # large: for meteors that get hit by bullet
explosion_anim['sm'] = [] # small: for spaceship when it hits a meteor
explosion_anim['player'] = [] # explosion pics for player spaceship
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75)) # scale based on original image
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32)) # scale based on original image
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow2.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow1.wav'))
expl_sounds = [] # list
for snd in ['boom 1.wav', 'boom 2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

# player die sound
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
# bg music
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4) # lowers music volume


all_sprites = pygame.sprite.Group() # put all sprites made into this group
mobs = pygame.sprite.Group() # put all mobs here
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(8):
    newmob()

score = 0
# we want bg music to start before game loop
pygame.mixer.music.play(loops=-1) # tells pygame to keep looping

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group() # put all sprites made into this group
        mobs = pygame.sprite.Group() # put all mobs here
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
    # keep loop running at the right speed
    clock.tick(FPS) # keeps track of time
    # Process input (events)
    for event in pygame.event.get():
        # event: things that happen outside the game that affects it (i.e. clicking stufF)
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

        ## COMMENTED OUT: this is for one shot / space bar press
        #elif event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_SPACE:
        #        player.shoot() # define .shoot() in player class

    # Update: tells the sprites what to do
    all_sprites.update() # updates every sprite in the group

    # check to see if a bullet hits a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # checks if two groups of sprites collide
    # Boolean means mobs & bullets get deleted when they collide
    for hit in hits: # everytime a mob gets deleted, this will spawn a new mob
        score += 60 - hit.radius # score is given based on radius of meteor
        random.choice(expl_sounds).play() # plays a random sound from the list
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9: # random.random() gives a num, 0<num<1 ==>> 0.9 means 10% chance
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # check to see if a mob hit the player
    # create a list of stuff you hit
    # checks if a sprite(player) hits a group(mob)
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    # Boolean decides if mob hit should be deleted or not. True means delete => not enough mobs later. need to spawn new mob
    # pygame.sprite.collide_circle => tells you what kind of collision you want to use (if left blank, assumes rect)

    # ensure that life bar does not respawn after player dies:
    if player.lives == 0:
        player.shield = 0
    #### end ####

    for hit in hits: # hits is a list of hits taken
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            # spawning a new life
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30) # random health
            shield_sound.play()
            if player.shield >= 100: # cap the shield bar at 100
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()

    # if the player died and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Draw / Render: creates each sprite
    screen.fill(BLACK) # fills screen with one colour(define above)
    screen.blit(background, background_rect) # copy pixels of image (bg) to the location (bg_rect)
    all_sprites.draw(screen) # draws all sprites in the place <screen>

    # placing the score text after the sprites => sprites will appear behind the score
    draw_text(screen, str(score), 22, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield) # (x, y, % value of bar to fill)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # AFTER drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
