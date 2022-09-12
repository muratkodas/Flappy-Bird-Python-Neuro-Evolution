import sys
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from pipe import Pipe

import numpy as np
import genetic_algorithm as ge


class Game:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.fps = 60
        
        """
        ###For Fullscreen
        self.screen = pygame.display.set_mode((0, 0 ), pygame.FULLSCREEN)
        self.settings.update_screen_parameters(self.screen)
        """
        ###For Lower resulation
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        
        pygame.display.set_caption("Flappy Bird")
        
        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        # Make the Play button.
        self.play_button = Button(self, "Play")
        
        self.neurons = np.matrix([[self.settings.nn_input_layer_neuron_number, self.settings.nn_hidden1_layer_neuron_number, self.settings.nn_output_layer_neuron_number]])
        
        print(f"self.settings.screen_height / self.settings.pipe_gap :{self.settings.screen_height / self.settings.pipe_gap}")

    def run_game(self):
        """Start the main loop for the game."""
        i=0
        while True:
            self.clock.tick(self.fps) # maximum fps for the game
            # Watch for keyboard and mouse events.
            self._check_events()
            
            if self.stats.game_active:
                self.update_pipes()
                for i in range(len(self.ge_game.population)):
                    if self.ge_game.population[i].alive:
                        self.ge_game.population[i].update()
            
            self._uptade_screen()          
            
                        
    def update_pipes(self):
        #Remove the pipe which is not visiable on the screen
        for pipe in reversed(self.pipes):
            if pipe.x <= -self.settings.pipe_width:
                self.pipes.remove(pipe)
                
        #Add the pipe at the right side of the screen 
        if self.settings.screen_width - self.pipes[-1].x > self.settings.pipe_gap/2:
            #print(f"# of pipes: {len(self.pipes)}")
            self.pipes.append(Pipe(self, self.pipes[-1].x + self.settings.pipe_gap))
            
        
        # Get 1 bird position info for pipe vs birds control
        # Creating bird population list with alive birds
        bird_for_x_pos = None
        bird_population_control_list = []
        for i in range(len(self.ge_game.population)):
                if self.ge_game.population[i].alive:
                    if bird_for_x_pos == None:
                        bird_for_x_pos = self.ge_game.population[i].x
                    bird_population_control_list.append(self.ge_game.population[i])
                      
        #Update the passed pipe color. Collusion detect for each alive birds. Kill the hit ones.
        if bird_for_x_pos != None: 
            # Determine the next pipe and change the color of it.
            for pipe in self.pipes:
                if pipe.x >= bird_for_x_pos - self.settings.pipe_width:
                    self.pipe_next = pipe
                    pipe.color = self.settings.pipe_color_next
                    break
                elif pipe.x <= bird_for_x_pos:
                    #Change the passed pipe's color to standart pipe color
                    if not pipe.passed:
                        pipe.passed = True
                        pipe.color = self.settings.pipe_color
                        self.stats.score += 1
                        
            #Kill the bird if it hits.
            if self.pipe_next.x <= bird_for_x_pos and self.pipe_next.x >= bird_for_x_pos - self.settings.pipe_width:
                for bird in bird_population_control_list:
                    bird.collosion_detect(self.pipe_next) #bird is between the enter and exit of the pipe. collosion_detect function will check crash on the y axis.
                    
        else:
            if self.pipes[0].x + self.settings.pipe_width < self.settings.screen_width/4 :
                self.next_generation()
                
        if self.stats.score >= 15:
            if self.pipes[0].x + self.settings.pipe_width < self.settings.screen_width/4 :
                self.next_generation()
                self.stats.high_score = self.stats.score
                self.stats.score = 0
                
            
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.display.quit():
                        sys.exit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)                                            
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    button_clicked = self.play_button.rect.collidepoint(mouse_pos)
                    self._check_play_button(button_clicked)
                
    
    def _check_play_button(self, button_clicked):
        """ Start a new game when the player clicks Play."""        
        if  button_clicked:
            if not self.stats.game_active:
                # Reset the game settings.
                self.settings.initialize_dynamic_settings()
                self.stats.game_active = True
                
                # Reset the game statistics.
                self.stats.reset_stats()
                
                self.run_ge_initialisation()
                
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            
                        
    def _check_keydown_events(self, event):
        """ Respond to keypresses."""
        if event.key == pygame.K_q:
            if event.type == pygame.display.quit():
                sys.exit()
            sys.exit()
        elif event.key == pygame.K_p:
            self.stats.game_pause = not self.stats.game_pause
            self._check_play_button(not self.stats.game_pause)
        elif event.key == pygame.K_r:
            self.run_ge_initialisation() # Restart can be improved by using the same birds by turning them active and update the positions
        
    
    def _check_keyup_events(self, event):
        """ Respond to keypresses."""
        if event.key == pygame.K_n:
            self.next_generation()
            
            
    def Genetic_Algorithm_Main(self):
        self.ge_game = ge.Genetic_Algorithm(self, self.neurons, self.settings.population_lenght)
        
    def create_pipes(self):
        self.number_of_pipes = int((self.settings.screen_width/2) / self.settings.pipe_gap) + 1
        for i in range(self.number_of_pipes):
            self.pipes.append(Pipe(self, self.settings.screen_width/2 + i*self.settings.pipe_gap))
            
    def run_ge_initialisation(self):
        self.Genetic_Algorithm_Main()
        self.pipes = []
        self.create_pipes()
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score 
    
    def next_generation(self):
        #generate a new bird population by fitness calculation
        self.fitness, self.score_mean = self.fitness_calculation()
        self.ge_game.Pool_Selection(self.fitness, self.score_mean) # GE algortihm will be performed and new population will be created.
        self.settings.initialize_dynamic_settings()

        
    def fitness_calculation(self):        
        # Creates a list for fitness of each bird
        score = np.arange(0,self.settings.population_lenght,1)
        for i in range(len(self.ge_game.population)):
            score[i] =self.ge_game.population[i].score
        
        
        if np.max(score, axis=0) == 0:
            score_mean = 0.0001
            fitness = np.ones((self.settings.population_lenght, 1))/10000
        else:
            score_mean = np.mean(score)
            score = score / np.max(score, axis=0)
            fitness = score.reshape(self.settings.population_lenght,1) 
        
        #print(f"score_mean: {score_mean}\n")
        return fitness, score_mean    
        
    def _uptade_screen(self):
        """Uptade images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active or self.stats.game_pause:
            self.play_button.draw_button()
            pygame.mouse.set_visible(True)
        else:        
            for pipe in self.pipes:
                pipe.draw()
                
            for i in range(len(self.ge_game.population)):
                if self.ge_game.population[i].alive:
                    self.ge_game.population[i].draw()
            # Draw the score information.
            self.sb.show_score()
            
        # Make the most recently drawn screen visible.
        pygame.display.flip()
            
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = Game()
    ai.run_game()
