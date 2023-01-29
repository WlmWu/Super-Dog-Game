import pygame
from pygame.sprite import Sprite
import random as rd

class Item(Sprite):
    def __init__(self, settings, status, screen, item_type = 'meat'):
        super().__init__()
        self.screen = screen 
        self.type = item_type

        self.settings = settings.spriteDict[self.type]

        self.width, self.height = self.settings['width'], self.settings['height']
        self.image = pygame.image.load(self.settings['img'][0])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()        
        self.originx, self.originy = self.screen.get_rect().midright
        self.originx += self.width
        self.originspeed = self.settings['speed']
        self.point = self.settings['point']
        self.delay = 0  # show up delay
        
        self.speedRange = int(settings.config['item']['speed_variation'])
        self.delayRange = int(settings.config['item']['delay_variation'])

        self.speedup = settings.config['basic']['level']['speed_scale']

        self.reset_pos(status)
        self.reset(status)

    def reset(self, status):
        self.delay = rd.randint(0, self.delayRange) if self.delay == 0 else self.delay - 1
        self.x = self.screen.get_rect().left - self.width
        if self.delay > 0 :
            return
        self.reset_pos(status)

    def reset_pos(self, status):
        self.speed = self.originspeed * rd.uniform(1., self.speedRange)
        self.levelup(status)
        self.rect.centerx, self.rect.centery = self.originx, rd.uniform(self.height, self.screen.get_rect().height - self.height)
        self.x = float(self.rect.x)

    def update(self, status, item_status = True):
        if self.check_edges() or item_status is False:
            self.reset(status)

        self.x -= self.speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def check_edges(self):
        return self.rect.right <= 0

    def levelup(self, status):
        for i in range(status.level - 1):
            self.speed *= self.speedup 

    def freeze(self):
        self.x += self.speed
        self.rect.x = self.x

class Meat(Item):
    def __init__(self, settings, status, screen, item_type='meat'):
        super().__init__(settings, status, screen, item_type)

class Bomb(Item):
    def __init__(self, settings, status, screen, item_type='bomb'):
        super().__init__(settings, status, screen, item_type)