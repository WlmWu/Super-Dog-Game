import time
import random as rd
import atexit
from tkinter import *
from tkinter import messagebox

class TypingSimulator():
    def __init__(self, output='Bye Bye ~ ~ ~', speed=0.2) -> None:
        self.output = output
        self.speed = speed

    def exit_event(self):
        self.popupWindow()
        input('Please press enter here...')
        self.typing_string()

    def typing_string(self):
        for c in self.output:
            # print(c, end='')
            print(c)
            delay = rd.uniform(0.01, self.speed)
            time.sleep(delay)
        time.sleep(3)
    
    def typingAtExit(self):
        atexit.register(self.exit_event)

    def popupWindow(self):
        Tk().wm_withdraw()
        messagebox.showinfo('Continue', 'Go to CLI window to continue')
