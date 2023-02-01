import pygame
from pygame.sprite import Sprite
from enum import Enum

class Stage(Enum):
    EATTING_MEAT = 0
    MOVING_MIDLEFT = 1
    EATTING_CAKE = 2
    DROPPING = 3
    JUMPING = 4
    LANDING = 5
    WIN = 6

class Rect():
    def __init__(self, screen):
        self.left = screen.get_rect().left
        self.right = screen.get_rect().right
        self.top = screen.get_rect().top
        self.bottom = screen.get_rect().bottom

class Dog(Sprite):
    def __init__(self, settings, screen): 
        super().__init__()
        self.screen = screen
        self.type = 'dog'

        self.settings = settings.spriteDict[self.type]

        self.width, self.height = self.settings['width'], self.settings['height']
        imgs = [pygame.image.load(i).convert_alpha() for i in self.settings['img']]
        self.allimages = [pygame.transform.scale(i, (self.width, self.height)) for i in imgs]
        self.images = self.allimages[:2]
        self.images_hurted = self.allimages[2:4]
        self.imgIdx = 0
        self.image = self.images[self.imgIdx]
        self.ishurted = 0

        self.refreshCntr = 0
        self.refreshRate = self.settings['img_refresh_rate']
        self.hurtedCntr = 0
        self.hurtedRate = self.refreshRate * 5

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.reset()
    
    def update(self):
        moving_screen = Rect(self.screen)
        moving_screen.right /= 2 if self.stage is Stage.EATTING_CAKE else 1

        if self.moving_right and self.rect.right < moving_screen.right:
            self.center += self.settings['speed']
        if self.moving_left and self.rect.left > moving_screen.left:
            self.center -= self.settings['speed']
        if self.moving_up and self.rect.top > moving_screen.top:
            self.height -= self.settings['speed']
        if self.moving_down and self.rect.bottom < moving_screen.bottom:
            self.height += self.settings['speed']
        self.rect.centerx = self.center
        self.rect.bottom = self.height
        self.updateImg()

    def blitme(self):
        if self.died:
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

    def dying(self):
        if not self.died:
            self.originalCenter = self.rect.center
            self.died = True
        self.rotateDegree += self.settings['animation']['rotate_speed'] if self.rotateDegree < self.settings['animation']['num_rotate']*360 else 0

        return self.rotateDegree >= self.settings['animation']['num_rotate']*360

    def reset(self):
        self.rect.centerx, self.rect.bottom = self.screen_rect.bottomleft
        self.rect.centerx -= self.rect.left
        self.center = float(self.rect.centerx)
        self.height = float(self.rect.bottom)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.died = False
        self.rotateDegree = 0
        self.image = pygame.transform.rotate(self.image, 0)

        self.stage = Stage.EATTING_MEAT

    def moving_animation(self, startpoint=None, endpoint=None, setup=False, accelaration=True):
        if setup:
            self.startpoint = startpoint
            self.endpoint = endpoint
            self.accelaration = self.settings['animation']['gravity'] if accelaration else (0, 0)
            lenA = (self.accelaration[0]**2 + self.accelaration[1]**2)**0.5
            deltaS = ((self.endpoint[0]-self.startpoint[0])**2 + (self.endpoint[1]-self.startpoint[1])**2)**0.5
            totaltime = self.settings['animation']['num_moving_step'] if not accelaration else (deltaS/lenA)**0.5
            self.velocity0 = (2 * self.accelaration[0] * (self.endpoint[0]-self.startpoint[0]), 2 * self.accelaration[1]*(self.endpoint[1]-self.startpoint[1])) if accelaration else ((self.endpoint[0]-self.startpoint[0])/totaltime, (self.endpoint[1]-self.startpoint[1])/totaltime)
            self.time = 0
            # print(self.velocity0, self.accelaration)

        else:
            self.rect.centerx = self.startpoint[0] + (self.velocity0[0] * self.time + 0.5 * self.accelaration[0] * (self.time**2))
            self.rect.bottom = self.startpoint[1] + (self.velocity0[1] * self.time + 0.5 * self.accelaration[1] * (self.time**2))
            self.time += 1

            self.center = float(self.rect.centerx)
            self.height = float(self.rect.bottom)


    def next_stage(self):
        if self.stage == Stage.EATTING_MEAT:
            startpoint = (self.rect.centerx, self.rect.bottom)
            endpoint = (self.rect.width/2, self.screen_rect.midleft[1]+self.rect.height/2)
            self.accelaration = 0
            self.moving_animation(startpoint=startpoint, endpoint=endpoint, setup=True, accelaration=False)
            self.stage = Stage.MOVING_MIDLEFT

        if (self.rect.centerx > self.endpoint[0] or (self.rect.centerx == self.endpoint[0] and self.rect.bottom - self.endpoint[1])) and self.stage == Stage.MOVING_MIDLEFT:
            self.moving_animation()

        if self.rect.centerx <= self.endpoint[0] and self.rect.bottom == self.endpoint[1]:
            self.stage = Stage.EATTING_CAKE

    def drop_animation(self):
        if self.stage == Stage.EATTING_CAKE:
            startpoint = (self.rect.centerx, self.rect.bottom)
            endpoint = (self.rect.centerx, self.screen_rect.bottom)
            self.moving_animation(startpoint=startpoint, endpoint=endpoint, setup=True)
            self.velocity0 = (0, 0)
            self.stage = Stage.DROPPING

        elif self.rect.bottom < self.endpoint[1] and self.stage == Stage.DROPPING:
            self.moving_animation()
        
        elif self.rect.bottom >= self.endpoint[1] and self.stage == Stage.DROPPING:
            self.stage = Stage.LANDING
            self.numJump = self.settings['animation']['num_jumping']
            return True
            
        return False

    def jump_animation(self):
        if self.stage == Stage.LANDING:
            startpoint = (self.rect.centerx, self.rect.bottom - self.screen_rect.height/2)
            endpoint = (self.rect.centerx, self.rect.bottom)
            self.moving_animation(startpoint=startpoint, endpoint=endpoint, setup=True)
            self.velocity0 = (-self.velocity0[0], -self.velocity0[1])
            self.startpoint = (self.rect.centerx, self.rect.bottom)
            self.endpoint = (self.rect.centerx, self.rect.bottom)
            self.stage = Stage.JUMPING

        elif self.rect.bottom <= self.endpoint[1] and self.stage == Stage.JUMPING:
            self.moving_animation()

        elif self.rect.bottom > self.endpoint[1] and self.stage == Stage.JUMPING:
            self.height = float(self.rect.bottom-1)
            self.numJump -= 1
            self.stage = Stage.LANDING
        
        return self.numJump == 0

    def win(self):
        self.height = float(self.rect.bottom)
        self.stage = Stage.WIN