import pygame
from pygame.sprite import Sprite

class Health_Pips(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        #Set the game's screen and screen rectangle
        #self.screen=ai_game.screen
        #self.screen_rect=ai_game.screen.get_rect()

        #Load the health pip image and get its rectangle
        self.image = pygame.image.load('images/health_pip.bmp')
        self.rect = self.image.get_rect()