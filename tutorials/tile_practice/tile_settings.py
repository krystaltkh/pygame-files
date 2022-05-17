import pygame as pg
vec = pg.math.Vector2

# define colours (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (122, 197, 205)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game options / settings
TITLE = "Tilemap!"
# choose approp. width / height so that there will be no partial squares
WIDTH = 1024 # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60 # Frames per second
BGCOLOUR = BROWN

TILESIZE = 64 # usually in powers of 2
GRIDWIDTH = WIDTH / TILESIZE # num of squares in W
GRIDHEIGHT = HEIGHT / TILESIZE # num of square in H

WALL_IMG = 'tile_358.png'
# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300 # pixels per second
PLAYER_ROT_SPEED = 250 # pixels per second
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10) # move 20 pixels forward(x), and down(y) of player
# so that it appears that the bullet is coming from the barrel of the gun

# Weapon settings
BULLET_IMG = 'tile_132.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg', # large / small
                     'bullet_count': 1} # number of bullets fired

WEAPONS['shotgun'] = {'bullet_speed': 400,
                     'bullet_lifetime': 500,
                     'rate': 1500,
                     'kickback': 300,
                     'spread': 20,
                     'damage': 5,
                     'bullet_size': 'sm', # large / small
                     'bullet_count': 12} # number of bullets fired

# Mob settings
MOB_IMG = 'zoimbie1_hold.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DMG = 10
MOB_KNOCKBACK = 20 # distance of being knocked back
AVOID_RADIUS = 50
DETECT_RADIUS = 600 # zombie will chase player if player is within 400 pixels

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png',
                  'whitePuff17.png', 'whitePuff18.png']
SPLAT_IMG = 'splat green.png'
FLASH_DURATION = 40 # ms
DAMAGE_ALPHA = [i for i in range(0, 255, 25)] # < 25: smoother blinks, > 25: erratic blinks
NIGHT_COLOUR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_med.png"
# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'obj_shotgun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15 # number of pixels item bobs up / down
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = 'Dark Intro.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/11.wav', 'pain/13.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav', 'zombie-roar-3.wav',
                      'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav', 'zombie-roar-8.wav']
ZOMBIE_HIT_SOUNDS =['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}
