import pygame
import numpy as np
import neural_network as nn
import random

class Bird():
    """A class to manage the Bird."""
    
    def __init__(self, game, neurons):
        """Initialize the bird, its brain and set its starting position."""
        self.alive = True
        
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()
        self.fps = self.game.fps
        
        self.brain = nn.Neural_Network(neurons)
        self.score = 0
        self.high_score = 0
        
        self.x = self.settings.screen_width/4
        self.y = random.randint(self.settings.screen_height*0.25, self.settings.screen_height*0.75) #self.settings.screen_height/2
        
        
        self.mass = 1
        self.cd_drag = self.settings.cd_sphere
        self.ro = self.settings.ro_air
        self.area = 0.09 #m^2 #cross-sectional area of pigeon
        self.gravity = self.settings.gravity
        self.drag_constant = self.cd_drag*self.ro*self.area*0.5
        self.acceleration = 0
        self.velocity = 0
        
        
        
    def check_negative(self,number):
        if number >= 0:
            return 1
        else:
            return -1
        
    def update(self):
        """Update the ship's position based on the movement flags."""
        if self.acceleration < self.settings.acceleration_max and self.velocity < self.settings.velocity_max:
            force = self.apply_force() # bird uses nn to decide to apply forces(1 or 0)
        else:
            force = 0
            
        self.drag = self.drag_constant*(self.velocity*self.velocity) # drag force, always positive
        self.acceleration = self.gravity - (force/self.mass) # gravity is in +y direction(direction to the bottom) ; bird apply force is in +y
        #apply the drag force
        self.acceleration -= self.check_negative(self.velocity)*(self.drag/self.mass) # drag applys always on the inverse direction of the velocity
        self.velocity += self.acceleration / self.fps
        y_increment = self.velocity / self.fps
        self.y += y_increment * self.settings.bird_speed_coef 
        
        if self.y >= self.settings.screen_height:
            self.y = self.settings.screen_height
            self.velocity = 0
        elif self.y <= 0:
            self.y = 0
            self.velocity = 0
        else:
            pass
        
    def apply_force(self):
        pipe = self.game.pipe_next
        width = self.settings.screen_width
        height = self.settings.screen_height
        
        # input: velocity, acceleration, and to the pipe: x diffrence, top_y difference, bottom_y difference       
        self.input = np.zeros((1,self.settings.nn_input_layer_neuron_number))
        self.input[0,0], self.input[0,1] = self.velocity/self.settings.velocity_max, self.acceleration/self.settings.acceleration_max
        self.input[0,2] = (self.x - pipe.rect_top.bottomleft[0])/width
        self.input[0,3], self.input[0,4] = (self.y - pipe.rect_top.bottomleft[1])/height, (self.y - pipe.rect_bottom.topleft[1])/height
        
        decision = self.brain.NN_loop(self.input, learning = False)
        
        if decision[0,0] > self.settings.decision_threshold:
            return self.settings.force
        else:
            return 0
        
    def collosion_detect(self, pipe):
        #check collosion by only looking at y axis. X axis was checked at update pipes function.
        if self.y <= pipe.pipe_top_height or self.y >= pipe.pipe_top_height + self.settings.pipe_hole :
            if self.score > self.high_score:
                self.high_score = self.score
            self.alive = False   # kill the bird by changing it status 
            self.settings.population_lenght_alive -= 1

    def draw(self):
        """ Draw the bird at its current location."""
        self.color = (200, 0, 200, 50)
        self.center = (int(self.x), int(self.y))
        self.radius = 10
        pygame.draw.circle(self.screen, self.color, self.center, self.radius) 