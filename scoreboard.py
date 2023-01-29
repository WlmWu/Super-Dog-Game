import pygame.font

class Scoreboard():
    def __init__(self, settings, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.score = 0
        self.setup()

    def setup(self):
        score_str = "Score: {:,}".format(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.config['scoreboard']['background_color'])

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def showScore(self):
        self.setup() 
        self.screen.blit(self.score_image, self.score_rect)

    def reset(self):
        self.score = 0
