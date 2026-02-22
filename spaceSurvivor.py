import arcade
import random
import math
from maze_build import LevelMap

WIDTH = 958
HEIGHT = 720
PLAYER_SCALING = 0.35
ENEMY_SCALING = 0.2
MOVEMENT_SPEED = 5
ENEMY_COUNT = 5
ENEMY_SPEED = 2

class MenuView(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WIDTH, HEIGHT))
        arcade.draw_text("Welcome to Space Survivor", WIDTH / 2, HEIGHT / 2, arcade.color.DARK_ORANGE, font_size=50, anchor_x="center")
        arcade.draw_text("Press ENTER to start", WIDTH / 2, HEIGHT / 2 - 100, arcade.color.DARK_ORANGE, font_size=30, anchor_x="center")
        arcade.draw_text("Press G for gameplay", WIDTH / 2, HEIGHT / 2 - 150, arcade.color.DARK_ORANGE, font_size=20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)

        if key == arcade.key.G:
            gameplay = GameplayView()
            self.window.show_view(gameplay)

class GameplayView(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")


    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WIDTH, HEIGHT))
        arcade.draw_text("Gameplay", WIDTH / 2, HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Clark is stuck on an alien spaceship.", WIDTH / 2, HEIGHT / 2 - 75, arcade.color.DARK_ORANGE, font_size=20, anchor_x="center")
        arcade.draw_text("Collect keys and make it to the exit to escape the aliens.", WIDTH / 2, HEIGHT / 2 - 95, arcade.color.DARK_ORANGE, font_size=20, anchor_x="center")
        arcade.draw_text("Don't get caught by the aliens or its game over.", WIDTH / 2, HEIGHT / 2 - 115, arcade.color.DARK_ORANGE, font_size=20, anchor_x="center")
        arcade.draw_text("Press BACKSPACE to return to main menu", WIDTH / 2, HEIGHT / 2 - 200, arcade.color.DARK_ORANGE, font_size=16, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.BACKSPACE:
            menu = MenuView()
            self.window.show_view(menu)

class Player(arcade.Sprite):
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > WIDTH - 1:
            self.right = WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > HEIGHT - 1:
            self.top = HEIGHT - 1

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.level = 1
        self.max_level = 5

        self.maze = None
        self.physics_engine = None

        self.time_taken = 0

        # self.key_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.window.score = 0

        self.player_sprite = Player(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", scale=PLAYER_SCALING)

        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.load_level(self.level)

        for j in range(ENEMY_COUNT):
            enemy = arcade.Sprite(":resources:images/alien/alienBlue_front.png", scale=ENEMY_SCALING)
            
            enemy.direction = random.choice(["up", "down", "right", "left"])

            x, y = self.maze.open_tile()
            enemy.center_x = x
            enemy.center_y = y
    
            self.enemy_list.append(enemy)

    def move_enemy(self, enemy):
        delta_x, delta_y = 0, 0
        if enemy.direction == "up":
            delta_y = ENEMY_SPEED
        elif enemy.direction == "down":
            delta_y = -ENEMY_SPEED   
        elif enemy.direction == "right":
            delta_x = ENEMY_SPEED 
        elif enemy.direction == "left":
            delta_x = -ENEMY_SPEED   

        enemy.center_x += delta_x
        enemy.center_y += delta_y

        if arcade.check_for_collision_with_list(enemy, self.maze.wall_list):
            enemy.center_x -= delta_x
            enemy.center_y -= delta_y 

            enemy.direction = random.choice(["up", "down", "left", "right"])    

    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_MIDNIGHT_BLUE

        self.window.set_mouse_visible(False)

    def load_level(self, level):
        self.maze = LevelMap(f"levels/level_{level}.json")

        self.player_sprite.center_x, self.player_sprite.center_y = self.maze.player_start()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            self.maze.wall_list
        )

    def on_draw(self):
        self.clear()

        self.maze.wall_list.draw()
        self.maze.exit_list.draw()
        self.player_list.draw()
        self.maze.key_list.draw()
        self.enemy_list.draw()

        arcade.draw_text(f"Level {self.level}", 10, HEIGHT - 30, arcade.color.WHITE, 20)

        output = f"Score: {self.window.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_update(self, delta_time):
        self.time_taken += delta_time

        self.physics_engine.update()

        self.maze.key_list.update()
        self.player_list.update(delta_time)

        for enemy in self.enemy_list:
            self.move_enemy(enemy)

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.maze.key_list)
        kill_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)

        for key in hit_list:
            key.kill()
            self.window.score += 1

        for player in kill_list:
            player.kill()

        col, row = self.maze.find_exit(self.player_sprite.center_x, self.player_sprite.center_y)

        if len(self.maze.key_list) == 0 and self.maze.maze[row][col] == 3:
            if self.level < self.max_level:
                self.level += 1
                self.load_level(self.level)
            if self.level == self.max_level:    
                game_won_view = GameWonView()
                game_won_view.time_taken = self.time_taken
                self.window.set_mouse_visible(True)
                self.window.show_view(game_won_view)
    
        if kill_list:
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.show_view(game_over_view)

        # if not kill_list:
        #     self.physics_engine.update()    

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()

class GameWonView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WIDTH, HEIGHT))
        arcade.draw_text("Congratulations! You Survived!", x=WIDTH / 2, y=400, color=arcade.color.WHITE, font_size=54, anchor_x="center")
        arcade.draw_text("Play Again? (P)", x=WIDTH / 2, y=300, color=arcade.color.WHITE, font_size=24, anchor_x="center")
        arcade.draw_text("Main Menu (M)", x=WIDTH / 2, y=250, color=arcade.color.WHITE, font_size=24, anchor_x="center")


        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}", WIDTH / 2, 200, arcade.color.WHITE, font_size=15, anchor_x="center")

        output_total = f"Score: {self.window.score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.P:
            game = GameView()
            self.window.show_view(game)

        if key == arcade.key.M:
            menu = MenuView()
            self.window.show_view(menu)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")

    
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WIDTH, HEIGHT))
        arcade.draw_text("You Died. Game Over.", x=WIDTH / 2, y=400, color=arcade.color.WHITE, font_size=54, anchor_x="center")
        arcade.draw_text("Restart? (R)", x=WIDTH / 2, y=300, color=arcade.color.WHITE, font_size=24, anchor_x="center")
        arcade.draw_text("Main Menu (M)", x=WIDTH / 2, y=250, color=arcade.color.WHITE, font_size=24, anchor_x="center")

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}", WIDTH / 2, 200, arcade.color.WHITE, font_size=15, anchor_x="center")

        output_total = f"Score: {self.window.score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.R:
            game = GameView()
            self.window.show_view(game)

        if key == arcade.key.M:
            menu = MenuView()
            self.window.show_view(menu)

def main():
    window = arcade.Window(WIDTH, HEIGHT)
    window.score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()        
