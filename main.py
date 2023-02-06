import pygame
import random as rd
import time
from settings import Settings
import game_functions as gf 
from game_status import GameStatus, GameState
from button import Button
from scoreboard import Scoreboard
from dog import Dog
from item import Meat, Bomb, Cake
from word_typing import TypingSimulator

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
        self.exitbutton = Button(self.settings, self.screen, type='exit')
        self.player = Dog(self.settings, self.screen)
        self.generateItems()
        fclk = pygame.time.Clock()
        fps = self.settings.config['basic']['fps']

        while True:
            if self.status.state is GameState.NOT_START:
                gf.check_events(self, self.status, button=self.startbutton)

            elif self.status.state is GameState.END:
                gf.check_events(self, self.status, button=self.restartbutton, player=self.player)

            elif self.status.state is GameState.WIN:
                gf.check_events(self, self.status, button=self.exitbutton, player=self.player)

            elif self.status.state is GameState.START:
                gf.check_events(self, self.status, player=self.player)
                if self.scoreboard.score >= self.settings.config['basic']['full_score']:
                    self.next_stage()
                elif self.scoreboard.score < 0 or self.player.died:
                    self.scoreboard.score = -1
                    self.gameover()

            elif self.scoreboard.score == self.settings.config['basic']['full_score']+self.settings.config['cake']['point']:
                if self.status.state is GameState.NEXT_STAGE:
                    self.status.state = GameState.FINAL_STAGE
                self.gamewin()
                gf.check_events(self, self.status, player=self.player)

            elif self.status.state is GameState.NEXT_STAGE:
                self.player.next_stage()
                gf.check_events(self, self.status, player=self.player)

            self.update()
            fclk.tick(fps)
    
    def update(self):
        self.screen.fill(self.settings.config['screen']['background_color'])
    
        if self.status.state == GameState.NOT_START:
            self.startbutton.draw_button()
        elif self.status.state == GameState.END:
            pygame.mouse.set_visible(True)
            self.restartbutton.draw_button()
        elif self.status.state == GameState.WIN:
            pygame.mouse.set_visible(True)
            self.exitbutton.draw_button()
            self.player.update()
            self.player.blitme()
        else:
            self.player.update()
            gf.checkItemsCollide(self.items)
            for i in self.items:
                i.update(self.status)
                gf.checkGetPoint(self.player, i, self.scoreboard)
            self.scoreboard.showScore()
            for i in self.items:
                i.blitme()
            self.player.blitme()
            self.status.update_level(self.scoreboard.score)

        pygame.display.flip()
    
    def gameover(self):
        for i in self.items:
            i.freeze()
        if self.player.dying():
            time.sleep(1)
            self.status.game_end()

    def reset(self):
        self.scoreboard.reset()
        self.player.reset()
        for i in self.items:
            i.kill()
        self.generateItems()

    def next_stage(self):
        self.status.state = GameState.NEXT_STAGE
        for i in self.items:
            i.hide()
            i.kill()
        self.items = [Cake(self.settings, self.status, self.screen)]

    def gamewin(self):
        for i in self.items:
            i.hide()
            i.kill()
        self.items = []

        if self.status.state is GameState.FINAL_STAGE and self.player.drop_animation():
            self.status.state = GameState.FINISH
            time.sleep(0.5)
            
        elif self.status.state is GameState.FINISH and self.player.jump_animation():
            time.sleep(0.5)
            self.player.win()
            TypingSimulator(output=self.settings.config['basic']['typing']['message'], speed=self.settings.config['basic']['typing']['speed']).typingAtExit()
            self.status.game_end(win=True)

if __name__ == '__main__':
    svr = Server()
    svr.start()