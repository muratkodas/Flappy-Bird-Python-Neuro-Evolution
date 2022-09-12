import pygame
from pygame.sprite import Sprite
import random 

class Pipe(Sprite):
    """ A class to manage pipes"""
    
    def __init__(self, game, pipe_left):
        """ Create a pipe object"""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.pipe_color
        self.fps = self.game.fps
        
        self.pipe_left = pipe_left
        
        self.passed = False
        
        self.pipe_hole = self.settings.pipe_hole
        self.pipe_top_height = random.randint(self.settings.screen_height/6, (5*self.settings.screen_height)/6)
        
        self.pipe_bottom_start = self.pipe_top_height + self.pipe_hole
        self.pipe_bottom_height = self.settings.screen_height - self.pipe_top_height - self.pipe_hole
        
        
        self.rect_top = pygame.Rect(self.pipe_left, 0, self.settings.pipe_width,
                                self.pipe_top_height)
        self.rect_bottom = pygame.Rect(self.pipe_left, self.pipe_bottom_start, self.settings.pipe_width,
                                self.pipe_bottom_height)
        
        # Store the pipe's position as a decimal value.
        self.x = float(self.rect_top.x)
        
    def update(self):
        """ Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.x -= self.settings.pipe_speed
        # Update the rect position.
        self.rect_top.x = self.x
        self.rect_bottom.x = self.x
        
        
    def draw(self):
        """ Draw the pipe to the screen."""
        if self.game.stats.game_active:
            self.update()
        pygame.draw.rect(self.screen, self.color, self.rect_top)
        pygame.draw.rect(self.screen, self.color, self.rect_bottom)