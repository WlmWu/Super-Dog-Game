import sys
import pygame
class Button():
    def __init__(self, settings, screen, type = 'start'):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        img = settings.config['button'][type]['img']
        self.image = pygame.image.load(img).convert_alpha()
        scale = settings.config['button'][type]['scale']
        self.width = self.image.get_width() * scale
        self.height = self.image.get_height() * scale
        self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
    
    def draw_button(self):
        self.screen.blit(self.image, self.rect)