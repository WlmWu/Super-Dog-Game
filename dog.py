import pygame
from pygame.sprite import Sprite

class Dog(Sprite):
    def __init__(self, settings, screen): 
        super().__init__()
        self.screen = screen
        self.type = 'dog'

        self.settings = settings.spriteDict[self.type]

        self.width, self.height = self.settings['width'], self.settings['height']
        imgs = [pygame.image.load(i) for i in self.settings['img']]
        self.allimages = [pygame.transform.scale(i, (self.width, self.height)) for i in imgs]
        self.images = self.allimages[:2]
        self.images_hurted = self.allimages[2:4]
        self.imgIdx = 0
        self.image = self.images[self.imgIdx]
        self.ishurted = 0

        self.refreshCntr = 0
        self.refreshRate = self.settings['refresh_rate']
        self.hurtedCntr = 0
        self.hurtedRate = self.refreshRate * 5

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.reset()

        # self.rect.centerx, self.rect.bottom = self.screen_rect.bottomleft
        # self.rect.centerx -= self.rect.left
        
        # self.center = float(self.rect.centerx)
        # self.height = float(self.rect.bottom)

        # self.moving_right = False
        # self.moving_left = False
        # self.moving_up = False
        # self.moving_down = False

        # self.rotateDegree = 0
        # self.originalCenter = self.rect.center
        # self.rotate = False
    
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings['speed']
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings['speed']
        if self.moving_up and self.rect.top > 0:
            self.height -= self.settings['speed']
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.height += self.settings['speed']
        self.rect.centerx = self.center
        self.rect.bottom = self.height
        self.updateImg()

    def blitme(self):
        if self.rotate:
            self.image = pygame.transform.rotate(self.image, self.rotateDegree)
            self.rect =  self.image.get_rect()
            self.rect.center = self.originalCenter

        self.screen.blit(self.image, self.rect)

    def updateImg(self):
        if self.ismoving():
            self.refreshCntr += 1
            if self.refreshCntr > self.refreshRate:
                self.refreshCntr = 0
                self.imgIdx = (self.imgIdx + 1) % len(self.images)
        else:
            self.imgIdx = 0

        self.hurtedCntr += 1 if self.ishurted else 0
        if self.hurtedCntr > self.hurtedRate:
            self.hurtedCntr = 0
            self.ishurted = 0

        self.image = self.images[self.imgIdx] if not self.ishurted else self.images_hurted[self.imgIdx]

    def ismoving(self):
        return self.moving_up or self.moving_down or self.moving_left or self.moving_right

    def behurted(self):
        self.ishurted = 1
        self.hurtedCntr = 0
        self.image = self.images_hurted[self.imgIdx]

    def died(self):
        if not self.rotate:
            self.originalCenter = self.rect.center
            self.rotate = True
        self.rotateDegree += self.settings['rotate_speed'] if self.rotateDegree < self.settings['num_rotate']*360 else 0

        return self.rotateDegree >= self.settings['num_rotate']*360

    def reset(self):
        self.rect.centerx, self.rect.bottom = self.screen_rect.bottomleft
        self.rect.centerx -= self.rect.left
        self.center = float(self.rect.centerx)
        self.height = float(self.rect.bottom)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.rotate = False
        self.rotateDegree = 0
        self.image = pygame.transform.rotate(self.image, 0)
