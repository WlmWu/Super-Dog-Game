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
        self.loadimg()      

        self.originx, self.originy = self.screen.get_rect().midright
        self.originx += self.width

        self.originspeed = self.settings['speed']
        self.point = self.settings['point']
        self.delay = 0  # show up delay
        
        self.speedRange = int(settings.config['item']['speed_variation'])
        self.delayRange = int(settings.config['item']['delay_variation'])

        self.speedup = settings.config['basic']['level']['speed_scale']

        self.game_status = status
        self.reset_pos()
        self.reset()   

    def loadimg(self):
        self.image = pygame.image.load(self.settings['img'][0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()  
    
    def reset(self, inf = False):
        self.delay = rd.randint(0, self.delayRange) if self.delay == 0 else self.delay - 1
        self.x = self.screen.get_rect().left - self.width
        if self.delay > 0 :
            return
        self.reset_pos()

    def reset_pos(self):
        self.speed = self.originspeed * rd.uniform(1., self.speedRange)
        self.levelup()
        self.rect.centerx, self.rect.centery = self.originx, rd.uniform(self.height, self.screen.get_rect().height - self.height)
        self.x = float(self.rect.x)

    def update(self, item_status = True):
        if self.check_edges() or item_status is False:
            self.reset()

        self.x -= self.speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def check_edges(self):
        return self.rect.right <= 0

    def levelup(self):
        for i in range(self.game_status.level - 1):
            self.speed *= self.speedup 

    def freeze(self):
        self.x += self.speed
        self.rect.x = self.x

    def hide(self):
        self.delay = 1000
        self.reset(inf=True)

class Meat(Item):
    def __init__(self, settings, status, screen, item_type='meat'):
        super().__init__(settings, status, screen, item_type)

class Bomb(Item):
    def __init__(self, settings, status, screen, item_type='bomb'):
        super().__init__(settings, status, screen, item_type)

class Cake(Item):
    def __init__(self, settings, status, screen, item_type='cake'):
        super().__init__(settings, status, screen, item_type)
 
    def loadimg(self):
        self.width, self.height = self.screen.get_rect().height * self.settings['scale'], self.screen.get_rect().height * self.settings['scale']
        super().loadimg() 
    
    def levelup(self):
        self.speed = self.originspeed

    def reset_pos(self):
        super().reset_pos()
        self.rect.centery = self.screen.get_rect().centery