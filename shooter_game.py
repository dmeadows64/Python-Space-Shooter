import sys
import pygame
import random
from bullet import Bullet
from settings import Settings
from ship import Ship
from alien import Alien
from time import sleep
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from random import seed
from random import randint

# Generates a random seed for use elsewhere in the program
seed(None)

class ShooterGame:
    """Handles general game loop code"""

    def __init__(self):
        """Initialize game values"""
        
        # Initialize PyGame
        pygame.init()
        
        # Grab the game's settings
        self.settings=Settings()
        
        # Set window width and title, then get the screen rectangle for later use
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("2-D Shooter Game")
        self.screen_rect = self.screen.get_rect()

        # Set game statistics and scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Set the player's ship to exist
        self.ship = Ship(self)

        # Set the groups used to handle bullets and aliens
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Set the number of enemies per level, how many have spawned, and how many have been destroyed
        self.enemies_per_level = self.settings.enemies_per_level
        self.enemies_spawned = 0
        self.enemies_destroyed = 0

        # Initialize the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the game's main loop"""
        
        while True:
            # Check for all keyboard and mouse events
            self._check_events()

            # Only do the following if the game is in an active state
            if self.stats.game_active:

                # Update the ship's position
                self.ship.update()
                
                # Update the bullet's position
                self._update_bullets()

                # Attempt to spawn an enemy
                self._spawn_test()

                # Move all aliens that exist
                self._update_aliens()
            
            # Redraw the game's screen after everything is updated.
            self._update_screen()
    
    def _check_events(self):
        """Check for keypresses and mouse events"""
        
        # Store all events in a list, iterate through that list
        for event in pygame.event.get():
            
            # Exit the game when the X on the top right is clicked
            if event.type == pygame.QUIT:
                sys.exit(0)
            
            # If a key is pressed, test to see what key it is and respond appropriately
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            
            # If a key is released, test to see what key it is and respond appropriately
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            # If the mouse button is pressed then get the mouse's position and check to see if it intersects the play button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_keydown_events(self, event):
        """Handles all cases in which a key is pressed"""
        # Arrow key handling
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        
        # Space bar handling
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

        # Extra quit condition
        if event.key == pygame.K_q:
            sys.exit(0)
        
    def _check_keyup_events(self, event):
        """Handle all cases in which a key is released"""
        # Arrow key handling
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False

    def _fire_bullet(self):
        """Creates new player-controlled projectiles"""
        # If there are less bullets than the allowed number of bullets then create a new bullet.
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Updates the positions of all bullets on the screen"""

        # Run the update method on everything in the bullets group
        self.bullets.update()

        # If a bullet is off the right side of the screen then delete that bullet.
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.screen_rect.right:
                self.bullets.remove(bullet)
        
        # Test to see if any bullets have collided with any aliens.
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Code for checking collisions between bullets and aliens, as well as reducing enemy health and adding to score"""

        # Form a dictionary of all collisions between bullets and aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)

        # Test to see if any collisions occured
        if collisions:
            
            # Get a list of all aliens involved in collisions
            for items in collisions.values():
                
                # Iterate through all items in that list
                for alien in items:
                    
                    # Reduce the enemy's health by 1
                    alien.enemy_health -= 1

                    # Test to see if the enemy's health is equal to or less than 0.
                    if alien.enemy_health <= 0:

                        # Test the enemy's type, add points depending on type.
                        if alien.enemy_type == True:
                            self.stats.score += int(self.settings.alien_points * 1.1)
                        else:
                            self.stats.score += int(self.settings.alien_points)

                        # Increase the number of enemies killed, then remove the enemy
                        self.enemies_destroyed += 1
                        alien.kill()

            # Update the score and check if high score needs updating.
            self.sb.prep_score()
            self.sb.check_high_score()

            # If enough enemies have been destroyed move to the next level.
            if self.enemies_destroyed == self.enemies_per_level:
                self._prep_new_level()

    def _spawn_test(self):
        """Handles enemy spawning"""
        # Function name is a relic. Originally this would only have a chance of causing an enemy to spawn, hence it tests to see if spawning is even possible.

        # Test to see if the proper amount of time has passed and there are still enemies to spawn.
        if pygame.time.get_ticks() - self.time_check >= self.settings.spawn_time and self.enemies_spawned != self.enemies_per_level:
            
            # Reset the clock for the next test
            self.time_check = pygame.time.get_ticks()

            # Create an unused alien just to use their height as a reference later.
            test_alien = Alien(self, False, 0)

            # Randomly determine if enemy should be normal or advanced
            # Create appropriate type of enemy
            if randint(1,100) <= self.settings.type_chance:
                new_alien = Alien(self, True, randint(1, self.settings.screen_height-test_alien.rect.height))
            else:
                new_alien = Alien(self, False, randint(1, self.settings.screen_height-test_alien.rect.height))
            
            # Increase the tracker for how many enemies have been spawned
            self.enemies_spawned += 1
            
            # Add the created alien to the aliens group
            self.aliens.add(new_alien)

    def _update_screen(self):
        """Makes sure that the screen is kept up-to-date"""

        # Fill in the background color
        self.screen.fill(self.settings.bg_color)

        # Draw the player's ship
        self.ship.blitme()

        # Draw each of the player's bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        # Draw any aliens
        self.aliens.draw(self.screen)
            
        # Draw the player's score
        self.sb.show_score()
            
        # If the game is not currently running then draw the play button
        if not self.stats.game_active:
            self.play_button.draw_button()
            
        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _check_play_button(self, mouse_pos):
        """Code for the play button"""

        # Test to see if the button was actually clicked
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        # Test to see if the button has been clicked and if the game is not active
        # If so then reset the game to its initial state for a new game
        if button_clicked and not self.stats.game_active:
            
            # Set dynamic settings
            self.settings.initialize_dynamic_settings()

            # Set game stats to default
            self.stats.reset_stats()
            
            # Game state set to active
            self.stats.game_active = True

            # Redraw the score at 0
            self.sb.prep_score()

            # Redraw the level at 1
            self.sb.prep_level()

            # Redraw the player's extra lives to 3
            self.sb.prep_ships()
            
            # Set the spawning clock
            self.time_check = pygame.time.get_ticks()
            
            # Empty the aliens and bullets group
            self.aliens.empty()
            self.bullets.empty()
            
            # Set the player's ship to its default location
            self.ship.reset_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _update_aliens(self):
        """Update the positions of all aliens and test to see if they have left the screen"""

        # Update the position of all aliens
        self.aliens.update()

        # Iterate through all aliens present
        for alien in self.aliens.sprites():

            # Test to see if the aliens have gone offscreen to the left
            if alien.check_edges():
                # Remove the alien and increase the number of enemies destroyed, but do not give points
                self.enemies_destroyed += 1
                alien.kill()

                # If all enemies in the level have died then start the next level
                if self.enemies_destroyed == self.enemies_per_level:
                    self._prep_new_level()

        # Test to see if the ship has collided with aliens, run the proper code if it has.
        if pygame.sprite.spritecollide(self.ship, self.aliens, True):
            self.enemies_destroyed += 1
            self._ship_hit()

            if self.enemies_destroyed == self.enemies_per_level:
                self._prep_new_level()
        

    def _ship_hit(self):
        """Code for handling health and life loss."""

        # Test to see if the player has more tha 1 health, reduces it if so and updates the health bar
        if self.stats.health_left > 1:
            self.stats.health_left -=1
            self.sb.prep_health()
        
        # If the player doesn't have more than 1 health then instead test if they have lives left.
        # If lives are left then reduce by 1, reset health to max, remove enemies and bullets and reset the level
        elif self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.stats.health_left = self.settings.health_limit
            self.sb.prep_health()
            self.sb.prep_ships()

            for alien in aliens:
                enemies_spawned -= 1
                alien.kill()

            self.bullets.empty()
            self.ship.reset_ship()
            sleep(0.5)
        
        #If the player is out of health and lives then set game state to inactive
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _prep_new_level(self):
        """Code for beginning a new level"""

        # Remove all active bullets
        self.bullets.empty()

        # Reset enemies spawned/destroyed number to 0
        self.enemies_spawned = 0
        self.enemies_destroyed = 0
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()


if __name__ == '__main__':
    ai = ShooterGame()
    ai.run_game()