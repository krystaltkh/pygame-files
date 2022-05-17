import pygame as pg
import pytmx
from tile_settings import *

def collide_hit_rect(one, two): # takes in 2 sprites
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f: # rt: reads txt file
            for line in f: # reads each line in map.txt
                self.data.append(line.strip()) # each line contains a string of characters
                # line.strip() takes away the '/n' character that python has when we enter a new line
                # without line.strip(), pygame reads this character and creates a new line of tiles

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        # pixelapha = True means it accounts for the transparency of the map
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    # loads the file
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        # each tile image has a gid (global identity) to identify itself from other tiles
        # ti ^ helps to identify each image when reading through the tmx file
        for layer in self.tmxdata.visible_layers:
        # reads all visible layers in the file. if any are made invisible, they will not be read
            if isinstance(layer, pytmx.TiledTileLayer):
            # if layer is a Tile Layer
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    # makes the map after loading
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    # create 2 options for camera to move in:
    def __init__(self, width, height):
        # use rectangle to track camera scope
        self.camera = pg.Rect(0, 0, width, height)
        # width & height are the size of the camera:
        self.width = width
        self.height = height

    # option 1: camera follows a sprite
    def apply(self, entity):
        # entity is a sprite
        # below tells the entity to move by self.camera.topleft amount
        return entity.rect.move(self.camera.topleft)
        # rect.move is an existing function that moves the rectangle

    # option 2: camera follows a rectangle
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        # target in this case is the player. we want camera to follow the target
        # if player moves to the right, offset of camera moves left
        x = -target.rect.centerx + int(WIDTH / 2) # add half of screen size to get player centred in the screen
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x) # left
        y = min (0, y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
