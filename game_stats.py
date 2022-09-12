class GameStats:
    """ Track statistics for the Game."""
    
    def __init__(self, game):
        """ Initialize statistics."""
        self.settings = game.settings
        self.reset_stats()
        
        # Start Game in an inactive state.
        self.game_active = False
        self.game_pause = False

        self.high_score = 0
        
    def reset_stats(self):
        """ Initialize statistics that can change during the game."""
        self.score = 0