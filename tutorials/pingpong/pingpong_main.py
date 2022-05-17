import pygame as pg
import sys
from os import path
import random
from pingpong_settings import * # imports all variables and codes from the file
from pingpong_sprite import *

class Game:
    def __init__(self):
        # intialise game window, etc
        pg.init() # initialises pygame
        pg.mixer.init() # initialises mixer: game has sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) # what will appear at top of the window
        self.clock = pg.time.Clock() # handles speed and how fast we're going
        self.running = True
        # to hold down keys for movement:
        pg.key.set_repeat(500, 100) # if key is held down for 500ms, repeat movement of key every 100ms
        self.load_data()

    def draw_text(self, text, font_name, size, colour, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        if align == "nw": # northwest
            text_rect.topleft = (x, y)
        if align == "ne": # northeast
            text_rect.topright = (x, y)
        if align == "sw": # southwest
            text_rect.bottomleft = (x, y)
        if align == "se": #southeast
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        #self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

        # Sound loading
        #pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group() # put all sprites made into this group
        self.player = Player()
        self.all_sprites.add(self.player)
        self.wall = Wall()
        self.all_sprites.add(self.wall)
        self.run() # tells game to start running

    def run(self):
        # Game loop
        self.playing = True
        #pg.mixer.music.play(loops=-1) # play bg music
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update() # updates every sprite in the group

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False # ends self.update
                self.running = False # ends the (programme) loop below
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused # allows for toggling

    def draw(self):
        # Game loop - draw
        self.screen.fill(BGCOLOUR) # fills screen with one colour(define above)
        self.all_sprites.draw(self.screen) # draws all sprites in the place <screen>
        # AFTER drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start show_go_screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new() # starts a new game
    g.show_go_screen()

pg.quit()
