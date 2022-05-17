# Sprite classes for platform game
import pygame as pg
from platformer_settings import *
from random import choice, randrange
vec = pg.math.Vector2 # vector with 2 variables

class Spritesheet(pg.sprite.Sprite):
    # utility class for loading and parsing spritesheets
    # reduces load time to constantly read images from system
    # uses .xml spritesheet file to parse the .png spritesheet file
    def __init__(self, filename):
        self.spritesheet= pg.image.load(filename)

    # this function ensures we don't need a .xml file. a .txt file will suffice
    def get_image(self, x, y, width, height):
        # grab an image out of a larger spreadsheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # ^ we take (x,y,w,h) of self.spritesheet and blit it onto (0, 0) location
        # scale images here so that we don't need to keep doing so in each sprite class
        image = pg.transform.scale(image, (width//2, height//2)) # pixels need to be in integer
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        ## important ^ must be done before __init__ below
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game # has a reference to the main game loop
        self.walking = False
        self.jumping = False
        self.current_frame = 0 # number of images used to animate
        self.last_update = 0 # keeps track of what time was the last change
        self.load_images()
        self.image = self.standing_frames[0]
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT-100) # where the sprite spawns at
        self.pos = vec(40, HEIGHT-100) # position
        self.vel = vec(0, 0) # velocity
        self.acc = vec(0, 0) # acceleration

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                                self.game.spritesheet.get_image(690, 406, 120, 201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walking_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                                 self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame, True, False)) # (img, horiz flip, vert flip)
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3: # short presses of space bar jumps
                self.vel.y = -3 # fix speed to upwards (-3)


    def jump(self):
        # value of +-= 2 ensures that sprite checks 2 pixels below and above it that it is on a platform to jump
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        # self.game.platforms: reference to platforms variable in main game loop
        self.rect.y -= 2
        if hits and not self.jumping: # ensures jump only if standing on a platform, cannot stack jumps in air
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP # gives an upward speed

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
         # force velocity to be 0 when too small, so that the player is idle and not walking when still
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the show_go_screen
        # add the self.rect.width/2 so that the sprite can travel further off the screen
        if self.pos.x > WIDTH + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width/2:
            self.pos.x = WIDTH + self.rect.width/2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0: # walking to the right
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking: # just standing
            if now - self.last_update > 350: # changes frame every 350ms
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show jump animation
        if self.jumping and not self.walking: # just jumping, no direction
            bottom = self.rect.bottom
            self.image = self.jump_frame
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image) # makes a mask from the image

class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds # groups we want plat sprites to be in
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50, 101) / 100 # because randrange needs integers
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale),
                                                    int(self.rect.height * scale)))
        # decide spawn location
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT*2:
            self.kill()

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms # groups we want plat sprites to be in
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(0, 576, 380, 94),
                 self.game.spritesheet.get_image(218, 1456, 201, 100)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups # these are the two groups you want pow sprites to be in
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx # powerup at the centre of the platform
        self.rect.bottom = self.plat.rect.top - 5 # powerup to be floating above platform

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        # when we move up, platform sprite gets deleted.
        # so we must make sure powerup sprite gets deleted too
        if not self.game.platforms.has(self.plat): # has command (for Groups) checks if platform is in the group
            self.kill() # delete powerup sprite

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs # these are the two groups you want pow sprites to be in
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100]) # so that mob can randomly spawn from left or right of screen
        self.vx = randrange(1, 4) # random speed
        if self.rect.centerx > WIDTH: # if mob spawns on the right
            self.vx *= -1 # speed moves it to the left
        self.rect.y = randrange(HEIGHT/2) # spawns randomly at top half of screen
        self.vy = 0 # starts stationary
        self.dy = 0.5 # y 'acceleration' of mob

    def update(self):
        self.rect.x += self.vx # move horizontally
        self.vy += self.dy # vertical speed
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1 # change direction
        center = self.rect.center
        if self.dy < 0: # moving upwards
            self.image = self.image_up
        else: # moving downwards
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image) # makes a mask from the image
        self.rect.center = center
        self.rect.y += self.vy # move vertically
        # if mob moved off the screen:
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
