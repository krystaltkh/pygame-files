# game options / settings
TITLE = "Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60 # Frames per second
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12 # < 0 because it slows down the player
PLAYER_GRAV = 0.8
PLAYER_JUMP = 22

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7 # % how likely a power up spawns at a platform
MOB_FREQ = 5000 # in miliseconds; means in avg mob spawns every 5s (5000ms)
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

# Starting platform_settings
# platform: (x, y, h, w)
# platform_list: a list of different platorm sizes
PLATFORM_LIST = [(0, HEIGHT-60),
                (WIDTH/2 - 50, HEIGHT * 3/4),
                (125, HEIGHT-350),
                (350, 200),
                (175, 100)]

# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (122, 197, 205)
BGCOLOUR = LIGHTBLUE
