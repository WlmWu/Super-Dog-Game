import pygame
import random as rd
import time
from settings import Settings
import game_functions as gf 
from game_status import GameStatus, GameState
from button import Button
from scoreboard import Scoreboard
from dog import Dog
from item import Meat, Bomb

class Server():
    def __init__(self):
        self.game = pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.config['screen']['width'], self.settings.config['screen']['height']))

        self.status = GameStatus(self.settings)
        self.scoreboard = Scoreboard(self.settings, self.screen)   

    def generateItems(self):
        self.items = []
        self.itemsComposition = {'meat': self.settings.config['basic']['num_items']['init_meat'], 'bomb': self.settings.config['basic']['num_items']['init_bomb']}

        # choose remain items
        for i in range(self.settings.config['basic']['num_items']['total'] - self.settings.config['basic']['num_items']['init_meat'] - self.settings.config['basic']['num_items']['init_bomb']):
            itemName = list(self.itemsComposition.keys())[rd.randint(0, len(list(self.itemsComposition.keys())) - 1)]
            self.itemsComposition[itemName] += 1

        # generate items
        for k, v in self.itemsComposition.items():
            for i in range(v):
                newitem = Meat(self.settings, self.status, self.screen) if k == 'meat' else Bomb(self.settings, self.status, self.screen)
                self.items.append(newitem)

    def start(self):
        self.startbutton = Button(self.settings, self.screen, type='start')
        self.restartbutton = Button(self.settings, self.screen, type='restart')
        self.player = Dog(self.settings, self.screen)
        self.generateItems()

        while True:
            if self.status.state is GameState.NOTSTART:
                gf.check_events(self, self.status, button=self.startbutton)
            elif self.status.state is GameState.END:
                gf.check_events(self, self.status, button=self.restartbutton)
            elif self.status.state is GameState.START:
                gf.check_events(self, self.status, player=self.player)
                if self.scoreboard.score >= self.settings.config['basic']['full_score']:
                    self.status.game_end()
                elif self.scoreboard.score < 0:
                    self.gameover()
            
            self.update()
    
    def update(self):
        self.screen.fill(self.settings.config['screen']['background_color'])
    
        if self.status.state == GameState.NOTSTART:
            self.startbutton.draw_button()
        elif self.status.state == GameState.END:
            pygame.mouse.set_visible(True)
            self.restartbutton.draw_button()
        else:
            self.player.update()
            gf.checkItemsCollide(self.items, self.status)
            for i in self.items:
                i.update(self.status)
                gf.checkGetPoint(self.player, i, self.scoreboard, self.status)
            self.scoreboard.showScore()
            for i in self.items:
                i.blitme()
            self.player.blitme()
            self.status.update_level(self.scoreboard.score)

        pygame.display.flip()
    
    def gameover(self):
        for i in self.items:
            i.freeze()
        if self.player.died():
            time.sleep(1)
            self.status.game_end()

    def reset(self):
        self.scoreboard.reset()
        self.player.reset()
        for i in self.items:
            i.kill()
        self.generateItems()

if __name__ == '__main__':
    # main()
    svr = Server()
    svr.start()