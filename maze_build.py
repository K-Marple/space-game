import json
import arcade
import random

WIDTH = 1280
HEIGHT = 720

FLOOR = 0
WALL = 1
KEY = 2
EXIT = 3

class LevelMap:
    def __init__(self, json_path):
        with open(json_path) as j:
            data = json.load(j)

        self.tile_size = data.get("tile_size", 32)
        self.maze = data["maze"]
        self.width = len(self.maze[0])
        self.height = len(self.maze)

        self.start = data["start"]

        self.wall_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()

        self.load_sprites()

    def load_sprites(self):
        scale_x = WIDTH / (self.width * self.tile_size)
        scale_y = HEIGHT / (self.height * self.tile_size)
        maze_scale = min(scale_x, scale_y)

        for row in range(self.height):
            for col in range(self.width):
                tile = self.maze[row][col]

                x = col * self.tile_size + (self.tile_size * maze_scale) / 2
                y = (self.height - row - 1) * self.tile_size + (self.tile_size * maze_scale) / 2

                if tile == WALL:
                    sprite = arcade.Sprite(":resources:/images/tiles/brickGrey.png", scale=0.4)
                elif tile == KEY:
                    sprite = arcade.Sprite(":resources:/images/items/keyYellow.png", scale=0.3)
                elif tile == EXIT:
                    sprite = arcade.Sprite(":resources:/images/tiles/signExit.png", scale=0.4)
                else:
                    continue

                sprite.center_x = x
                sprite.center_y = y

                if tile == WALL:
                    self.wall_list.append(sprite)
                elif tile == KEY:
                    self.key_list.append(sprite)
                elif tile == EXIT:
                    self.exit_list.append(sprite)

    def player_start(self):
        col, row = self.start
        x = col * self.tile_size + self.tile_size / 2
        y = (self.height - row - 1) * self.tile_size + self.tile_size / 2
        return x, y
    
    def open_tile(self):
        open_tiles = []

        for row in range(self.height):
            for col in range(self.width):
                tile = self.maze[row][col]

                if tile == 0:
                    open_tiles.append((col, row))

        col, row = random.choice(open_tiles)

        x = col * self.tile_size + self.tile_size / 2
        y = (self.height - row - 1) * self.tile_size + self.tile_size / 2

        return x, y
    
    def find_exit(self, x, y):
        col = int(x // self.tile_size)
        row = int(self.height - 1 - (y // self.tile_size))
        return col, row