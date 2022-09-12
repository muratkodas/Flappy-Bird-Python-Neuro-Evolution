import pygame.font

class Scoreboard:
    """ A class to report scroring information."""
    
    def __init__(self, game):
        """ Initialize scorekeeping attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        
        # Font settings for scoring informartion.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

    def prep_image(self, number_tobe_rounded, rect_left_pos, rect_top_pos):
        """ Turn the score into a rendered image."""
        rounded_number = round(number_tobe_rounded, 0)
        str_number = "{:,}".format(rounded_number)
        image = self.font.render(str_number, True,
                                            self.text_color, self.settings.bg_color)
        
        image_rect = image.get_rect()
        image_rect.left = rect_left_pos
        image_rect.top = rect_top_pos
        
        return image, image_rect
        
    def show_score(self):
        """ Draw score, high score and alive birds to the screen."""
        score_image, score_rect = self.prep_image(self.stats.score, self.screen_rect.right - 40, self.screen_rect.top)
        self.screen.blit(score_image, score_rect)
        high_score_image, high_score_rect = self.prep_image(self.stats.high_score, self.screen_rect.centery, self.screen_rect.top)
        self.screen.blit(high_score_image, high_score_rect)
        alive_birds_image, alive_birds_rect = self.prep_image(self.settings.population_lenght_alive, self.screen_rect.left, self.screen_rect.top)
        self.screen.blit(alive_birds_image, alive_birds_rect)
        alive_birds_image, alive_birds_rect = self.prep_image(self.settings.population_lenght_alive, self.screen_rect.left, self.screen_rect.top)
        self.screen.blit(alive_birds_image, alive_birds_rect)