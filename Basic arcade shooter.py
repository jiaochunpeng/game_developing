# Basic arcade shooter

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Arcade Space Shooter"
SCALING = 1.0

class SpaceShooter(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width, height, title):
        """Initialize the game
        """
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        self.setup()

    def setup(self):
        """Get the game ready to play
        """

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Set up the player
        self.player = arcade.Sprite("images/jet.png", SCALING)
        self.player.bottom = 10
        self.player.center_x = self.width / 2 
        self.all_sprites.append(self.player)
        self.paused=False

        # Spawn a new enemy every 0.25 seconds
        arcade.schedule(self.add_enemy, 0.25)

        # Spawn a new cloud every second
        arcade.schedule(self.add_cloud, 1.0)

    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """

        # First, create the new enemy sprite
        enemy = arcade.Sprite("images/missile.png", SCALING,angle=90)

        # Set its position to a random height and off screen up
        enemy.center_x = random.randint(10, self.width-10)
        enemy.top = random.randint(self.height - 10,self.height)
        
        # Set its speed to a random speed heading down
        enemy.velocity = (0,random.randint(-10, -5))

        # Add it to the enemies list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_cloud(self, delta_time: float):
        """Adds a new cloud to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """

        # First, create the new cloud sprite
        cloud = arcade.Sprite("images/cloud.png", random.randint(1,3)*SCALING)

        # Set its position to a random height and off screen right
        cloud.center_x = random.randint(10, self.width-10)
        cloud.top = random.randint(self.height - 10,self.height)

        # Set its speed to a random speed heading left
        cloud.velocity = (0,random.randint(-5, -2))

        # Add it to the enemies list
        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        P: Pause/Unpause the game
        I/J/K/L: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = 5

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -5

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 5

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
        If paused, do nothing

        Arguments:
            delta_time {float} -- Time since the last update
        """

        #If paused, don't update anything
        if self.paused:
            return

        # Update everything
        self.all_sprites.update()

        # Did you hit anything? If so, end the game
        # if self.player.collides_with_list(self.enemies_list):
        #     arcade.close_window()        

        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

        for a in self.enemies_list:
            if a.bottom<=0:
                a.remove_from_sprite_lists()
        for a in self.clouds_list:
            if a.bottom<=-a.height+60:
                a.remove_from_sprite_lists()

    def on_draw(self):
        """Draw all game objects
        """
        arcade.start_render()
        self.all_sprites.draw()

if __name__ == "__main__":
    app = SpaceShooter(800,600,'Space Shooter')
    arcade.run()