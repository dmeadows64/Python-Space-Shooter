import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Code relating to alien characters"""

    def __init__(self, ai_game, enemy_type, start_y):
        # Initialize the Sprite class
        super().__init__()

        # Get the game's screen
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Sets the enemy type using a boolean value.
        # True results in an advanced enemy, False results in a basic enemy
        # I consider using a boolean here acceptable as there are only two possible values
        self.enemy_type = enemy_type

        # Set the values that vary depending on type
        if self.enemy_type == True:
            self.image=pygame.image.load('images/adv_alien.bmp')
            self.enemy_health = 3
        else:
            self.image=pygame.image.load('images/alien.bmp')
            self.enemy_health = 1

        # Get game settings
        self.settings=ai_game.settings

        #Get alien's rectangle
        self.rect = self.image.get_rect()

        # Set the starting X and Y positions.
        # X is offscreen to the right
        # Y is a random number
        self.rect.x = self.settings.screen_width + self.rect.width
        self.rect.y = start_y

        # Set a float value for the X position for decimal speeds.
        # Y is not modified, so I did not consider it needed to use a variable for that
        self.x=float(self.rect.x)   

    def update(self):
        """Move the alien left across the screen"""
        self.x -= self.settings.alien_speed
        self.rect.x = self.x

    def check_edges(self):
        """Check to see if the alien is offscreen to the left. If so, remove the alien."""
        if self.rect.left <= self.screen_rect.left:
            return True