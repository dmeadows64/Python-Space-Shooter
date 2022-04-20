import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Code relating to the player's bullets"""
    def __init__(self, ai_game):
        # Initialize the Sprite class
        super().__init__()

        # Get the screen
        self.screen=ai_game.screen

        # Get the settings
        self.settings=ai_game.settings

        # Get the bullet's colors out of settings
        self.color=self.settings.bullet_color

        
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midright=ai_game.ship.rect.midright

        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.bullet_speed
        self.rect.x=self.x

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)