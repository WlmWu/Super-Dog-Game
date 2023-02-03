import time
import random as rd
from pynput.keyboard import Controller
import atexit

class TypingSimulator():
    def __init__(self, output='Bye Bye ~ ~ ~', speed=0.2) -> None:
        self.output = output
        self.speed = speed

    def exit_event(self):
        input('Please press enter here...')
        self.typing_string()

    def typing_string(self):
        keyboard = Controller()
        for c in self.output:
            keyboard.type(c)
            delay = rd.uniform(0.01, self.speed)
            time.sleep(delay)
    
    def typingAtExit(self):
        atexit.register(self.exit_event)
