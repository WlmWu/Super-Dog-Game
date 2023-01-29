from enum import Enum
class GameState():
    NOTSTART = 0
    START = 1
    END = 2

class GameStatus():
    def __init__(self, settings):
        self.reset_status()
        self.settings = settings

    def reset_status(self):
        self.score = 0
        self.level = 1
        self.state = GameState.NOTSTART

    def update_level(self, score):
        self.level = 1
        for th in self.settings.config['basic']['level']['threshold']:
            self.level += 1 if score >= th else 0
    
    def game_start(self):
        self.state = GameState.START
    
    def game_end(self):
        self.state = GameState.END