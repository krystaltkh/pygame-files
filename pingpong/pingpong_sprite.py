import pygame as pg
#from pingpong_main import*
from pingpong_settings import*
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((120, 20))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.rect.center = vec(WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH - 15, HEIGHT - 15)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # create walls at side of screen
        if self.pos.x + 60 > WIDTH:
            self.pos.x = WIDTH - 60
        if self.pos.x - 60 < 0:
            self.pos.x = 60

        self.rect.center = self.pos

class Wall(pg.sprite.Sprite):
    def __init__(self):
        #self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((80, 20))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.rect.center = vec(80, 10)
        self.pos = vec(20, 20)
