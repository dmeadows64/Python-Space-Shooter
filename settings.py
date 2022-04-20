class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""

        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        
        self.ship_limit = 3
        self.health_limit = 3
        
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        self.speedup_scale = 1.1

        self.score_scale = 1.5

        self.enemies_per_level = 10

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = .75
        self.bullet_speed = 1.5
        self.alien_speed = .25
        self.alien_points = 50
        #self.spawn_rate = 25
        self.spawn_time = 2500
        self.type_chance = 10

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= int(self.score_scale)
        self.spawn_time /= self.speedup_scale

        if self.spawn_time < 1:
            self.spawn_time = 1
        #self.spawn_rate *= self.speedup_scale

        #if self.spawn_rate >= 80:
        #    self.spawn_rate = 80