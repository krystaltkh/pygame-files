# run with command + I
# Art from Kenney.nl
# Happy Tune by syncopika, https://opengameart.org/content/happy-tune
# Yippee by Snabisch, https://opengameart.org/content/yippee-0

# Jumpy! - platform game settings
import pygame as pg
import random
#import platformer_settings
# ^ runs the code from another file, but variable from the
# file used here must be used as platform_settings.WIDTH for example
### ALTERNATIVELY, ###
from platformer_settings import * # imports all variables and codes from the file
from platformer_sprites import *
from os import path # for loading files

class Game:
    def __init__(self):
        # intialise game window, etc
        pg.init() # initialises pygame
        pg.mixer.init() # initialises mixer: game has sound
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) # what will appear at top of the window
        self.clock = pg.time.Clock() # handles speed and how fast we're going
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        #snd_dir = path.join(self.dir, 'snd')
        #we want to make sure the file is always closed when the game is closed
        #this makes sure that not more than one programme is running and making changes to the file
        if path.isfile(path.join(self.dir, HS_FILE)):
            # if file exists, read & write
            self.file_exist = 'r+'
        else: # if file does not exist, write a new file
            self.file_exist = 'w'
        with open(path.join(self.dir, HS_FILE), self.file_exist) as f:
        # r+: read & write, r: read, rb: binary file, rt: text file, w: creates a file if it doesn't exist
            try: # catches an error that is thrown
                self.highscore = int(f.read())
            except: # file is empty
                self.highscore = 0
        # load spritesheet image
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # cloud images
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump.wav'))
        # note that (long) music can only be streamed one at a time, so make sure to load them at
        # the appropriate functions only!
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'boost.wav'))

    def new(self):
        # start a new game
        self.score = 0
        # LayeredUpdates group allows for groups to be given an order of who to layer over who
        # lower layer gets drawn first
        self.all_sprites = pg.sprite.LayeredUpdates() # put all sprites made into this group
        self.platforms = pg.sprite.Group() # platform Group for collisions
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()

        # sends a reference to the player sprite -> player knows all the game's variables
        # reference made with: < self.game = game > in Player class in sprites file
        self.player = Player(self)

        for plat in PLATFORM_LIST:
            Platform(self, *plat) # *plat: splits the list accordingly to fit the 4 parameters
        self.mob_timer = 0 # keeps track of when the last mob is spawned
        pg.mixer.music.load(path.join(self.snd_dir, 'happytune.ogg'))
        # spawn some clouds at the start of the level
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        self.run() # tells game to start running

    def run(self):
        # Game loop
        pg.mixer.music.play(loops=-1) # infinitely repeat
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500) # fades out when you die in the game

    def update(self):
        # Game Loop - Update
        self.all_sprites.update() # updates every sprite in the group

        # spawn a mob?
        now = pg.time.get_ticks()
        # sprite spawns randomly every 6, 5.5, 5, 4.5, 4 seconds
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # hit mobs?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False) # rect collision
        if mob_hits:
            mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
            if mob_hits:
                self.playing = False

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            # False means platform is not deleted on collision
            if hits:
                lowest = hits[0] # make sure we only jump to the lower (closest) platforms
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                # backslash makes sure python sees it as one line
                # +- 10 to make falling off the platform more natural
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10:
                   # only land on platform if jump allows feet to be higher than platform
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 1
                        # +1 because the player is not actually touching the platform -- offsets 1 pixel btn platform & player
                        self.player.vel.y = 0 # so that player sprite does not fall through platform
                        self.player.jumping = False

        # if player reaches top 1/4 of screen, scroll up
        if self.player.rect.top <= HEIGHT/4:
            # need abs because when player goes up, vel is < 0
            # makes sure that screen scrolls up even when vel is 0
            if random.randrange(100) < 15:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 6)
            for cloud in self.clouds:
                rand_speed = randrange(1, 3)
                cloud.rect.y += max(abs(self.player.vel.y / rand_speed), 2)
            for mob in self.mobs: # so that mobs are scrolled down as well
                mob.rect.y += max(abs(self.player.vel.y), 6)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 6)
                if plat.rect.top >= HEIGHT:
                    # to prevent lag, kill platforms when they disappear off the screen
                    plat.kill()
                    # but this means that platforms won't be there anymore
                    self.score += 10

        # if player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True) # delete the powerup
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER # pushes player upwards
                self.player.jumping = False # makes sure jumping does not interfere w boost

        # Die! x.x
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                # max: ensures that the speed of scroll is kinda proportionate to how high the player falls from
                if sprite.rect.bottom < 0: # player falls off the bottom of screen
                    sprite.kill() # restarts game
        if len(self.platforms) == 0:
            self.playing = False # restarts game

        # spawn new platforms to keep same average number of platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH-width), # x
                     random.randrange(-75, -30)) # y

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False # ends self.update
                self.running = False # ends the (programme) loop below
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game loop - draw
        self.screen.fill(BGCOLOUR) # fills screen with one colour(define above)
        self.all_sprites.draw(self.screen) # draws all sprites in the place <screen>
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        # AFTER drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start show_go_screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOUR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
        if not self.running: # checks if game is ended halfway while playing
            # if ended halfway, exit this function at the bottom of the loop
            # and don't display game over screen
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOUR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH/2, HEIGHT*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH/2, HEIGHT/2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH/2, HEIGHT/2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False # ends programme
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, colour, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour) # True: for anti-aliased font
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new() # starts a new game
    g.show_go_screen()

pg.quit()
