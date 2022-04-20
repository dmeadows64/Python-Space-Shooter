import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        #Set the game's screen, screen rectangle, and settings
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #Set the base speed from the settings' speed. This can be modified later.
        self.actual_speed=self.settings.ship_speed

        #Load the ship image and get its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the middle left of the screen, then move it right a bit.
        self.rect.midleft=self.screen_rect.midleft
        self.rect.x += 20

        #Set two float variables to contain the ship's position
        #This helps to position it when the speed is a decimal number
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

        #Movement flags
        self.moving_right=False
        self.moving_left=False
        self.moving_up=False
        self.moving_down=False

    def update(self):
        """Handles all code regarding the ship's movement."""
        #If the ship is moving both horizontally and vertically then the speed is modified.
        #Multiplying it by 0.707 worked out perfectly somehow, I don't fully understand the math.
        if self.moving_up or self.moving_down:
            
            #Temporarily sets the speed to its normal value
            #I found that in some cases the speed would not reset properly without this
            self.actual_speed = self.settings.ship_speed
            
            if self.moving_left or self.moving_right:
                self.actual_speed = self.settings.ship_speed * .707
        else:
            self.actual_speed = self.settings.ship_speed

        #Test to see if a movement flag is on and the ship is not at the edge of the screen.
        #If both resolve to True then the ship moves in the given direction
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.actual_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.actual_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.actual_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.actual_speed
        
        #Set the ship's actual position to equal the float value position
        self.rect.x=self.x
        self.rect.y=self.y

    def blitme(self):
        """draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def reset_ship(self):
        """Reset the ship's position to the default location."""
        self.rect.midleft=self.screen_rect.midleft
        self.rect.x += 20
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)