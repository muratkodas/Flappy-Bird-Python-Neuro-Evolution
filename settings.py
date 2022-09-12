class Settings:
    """A class to store all settings for Flappy Bird Neuro Evolution."""
    
    def __init__(self):
        """Initialize the game's static settings."""
        #Screen settings
        self.screen_width  = 640
        self.screen_height = 480
        # Set the background color.
        self.bg_color = (230, 230, 230)      
        
        #Evolution Settings
        self.time_delay = 1
        self.step_number = 60#1000
        self.population_lenght = 50 #100
        
        #Neural Network Attiributes
        self.nn_input_layer_neuron_number = 5
        self.nn_hidden1_layer_neuron_number = 3
        self.nn_output_layer_neuron_number = 1
        self.decision_threshold = 0.9
        
        #Pipe settings        
        self.pipe_width = 40
        self.pipe_height = 15
        self.pipe_color = (60, 60, 60)
        self.pipe_color_next = (200, 200, 0)
        self.pipe_allowed = 3
        self.pipe_hole = self.screen_height/3
        self.pipe_gap = 5*self.pipe_width
        
        self.bird_speed_coef = 5 * (self.screen_height / self.pipe_gap)
        
        # Physical constants
        self.gravity = 9.8 #m/s2 #gravity
        self.cd_sphere = 0.47 #drag coefficient of sphere
        self.ro_air = 1.225 #kg/m^3 #density of air
        
        # Physical properies of the bird
        self.force = 3*self.gravity
        self.acceleration_max = self.force
        self.velocity_max = self.force
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """ Initialize settings that change throughout the game."""
        self.pipe_speed = 1
        self.population_lenght_alive = self.population_lenght
        
    def update_screen_parameters(self, screen):
        self.screen_width = screen.get_rect().width
        self.screen_height = screen.get_rect().height
        self.bird_speed_coef = 5 * self.screen_height / self.pipe_gap