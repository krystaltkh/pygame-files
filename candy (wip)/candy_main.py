import pygame as pg
import sys
from os import path
from candy_settings import * # imports all variables and codes from the file
from candy_sprites import *
from candy_map import *

# HUD (Heads Up Display) functions
def draw_player_health(surf, x, y, pct):
    pass

class Game:
    def __init__(self):
        # intialise game window, etc
        # create less lag for sound: 2048 can be edited to other powers of 2.
        pg.mixer.pre_init(44100, -16, 1, 2048) # values < 2048 will reduce lag, but twists the sound played
        pg.init() # initialises pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) # what will appear at top of the window
        self.clock = pg.time.Clock() # handles speed and how fast we're going
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
        self.map_folder = path.join(game_folder, 'maps')
        # self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        # self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        # self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        # self.dim_screen.fill((0, 0, 0, 180)) # larger alpha channel -> darker
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

        # Sound loading
        #pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}

    def new(self):
        # initialise all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates() # put all sprites made into this group
        # LayeredUpdates -> can set layers
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        # start with new map each new game to remove splats
        self.map = TiledMap(path.join(self.map_folder, 'castle_map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # for tile_object in self.map.tmxdata.objects: # finds all objects
        #     obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
        #     # objects are stored in a dictionary
        #     if tile_object.name == "player":
        #         self.player = Player(self, obj_center.x, obj_center.y)
        #     if tile_object.name == "wall":
        #         Obstacle(self, tile_object.x, tile_object.y,
        #                  tile_object.width, tile_object.height)
        #     if tile_object.name == "zombie":
        #         Mob(self, obj_center.x, obj_center.y)
        #     if tile_object.name in ['health', 'shotgun']:
        #         Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = True
        #self.effects_sounds['level_start'].play()

    def run(self):
        # Game loop
        self.playing = True
        pg.mixer.music.play(loops=-1) # play bg music
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update() # updates every sprite in the group
        self.camera.update(self.player)

        # game over?
        if len(self.mobs) == 0:
            self.playing = False

        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        # for hit in hits:
        #     if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
        #         hit.kill()
        #         self.effects_sounds['health_up'].play()
        #         self.player.add_health(HEALTH_PACK_AMOUNT)
        #     if hit.type == 'shotgun':
        #         hit.kill()
        #         self.effects_sounds['gun_pickup'].play()
        #         self.player.weapon = 'shotgun'

        # mobs hit player
        # hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        # for hit in hits:
        #     if random() < 0.7:
        #         choice(self.player_hit_sounds).play()
        #     self.player.health -= MOB_DMG
        #     hit.vel = vec(0, 0) # mob pauses if it hits the player
        #     if self.player.health <= 0:
        #         self.playing = False
        # if hits: # knock the player back after getting hit
        #     self.player.hit()
        #     self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

    def draw_grid(self):
        # pg.draw.line: (surface, colour, from A, to B)
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        # keep this only when developing game to track game performance:
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # Game loop - draw
        #self.screen.fill(BGCOLOUR) # fills screen with one colour(define in settings)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        # for sprite in self.all_sprites:
        #     if isinstance(sprite, Mob): # == if sprite is a Mob
        #         sprite.draw_health()
        #     self.screen.blit(sprite.image, self.camera.apply(sprite))
        #     if self.draw_debug:
        #         pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        #draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        #self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE,
        #                WIDTH - 10, 10, align="ne")
        if self.paused:
            # dim_screen is same size as screen, so can start drawing from (0, 0)
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        # AFTER drawing everything, flip the display
        pg.display.flip()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug # allows for toggling
                if event.key == pg.K_p:
                    self.paused = not self.paused # allows for toggling

    def show_start_screen(self):
        # game splash/start show_go_screen
        pass

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE,
                           WIDTH / 2, HEIGHT * 3/4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        # ^ ensures that person playing must keyup a new key (and not prev held down key) before game starts
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    # impt!! do keyup event so that game only starts when key is released
                    waiting = False

g = Game()
g.show_start_screen()
while True:
    g.new() # starts a new game
    g.run()
    g.show_go_screen()

pg.quit()
